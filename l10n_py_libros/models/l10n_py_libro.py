# l10n_py_libros/models/l10n_py_libro.py

import calendar
import csv
import io
import zipfile
from datetime import date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

from .l10n_py_libro_serializer import serialize_line

ZERO_BREAKDOWN_CODES = {"101", "104", "105", "112"}
MAX_LINES_PER_FILE = 5000

NC_ND_TABLE = {
    "padrao": {
        ("110", "own"): "compras",
        ("110", "third"): "ventas",
        ("111", "own"): "ventas",
        ("111", "third"): "compras",
    },
    "invertida": {
        ("110", "own"): "ventas",
        ("110", "third"): "compras",
        ("111", "own"): "compras",
        ("111", "third"): "ventas",
    },
}

LOTE_LETRA_MAP = {"ventas": "V", "compras": "C", "ingresos": "I", "egresos": "E"}
# Guaranies: three buckets rounded on their own can differ by up to 1.5
LIBRO_ROUNDING_TOLERANCE = 3


class L10nPyLibro(models.Model):
    _name = "l10n_py.libro"
    _description = "Libro DNIT (RG 90/2021)"
    _inherit = ("mail.thread", "mail.activity.mixin")
    _order = "year desc, month desc, tipo_registro"

    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    tipo_registro = fields.Selection(
        [
            ("ventas", "Ventas"),
            ("compras", "Compras"),
            ("ingresos", "Ingresos"),
            ("egresos", "Egresos"),
        ],
        required=True,
    )
    obligacion = fields.Selection(
        [("955", "955 - Mensual"), ("956", "956 - Anual")],
        required=True,
        default="955",
    )
    year = fields.Integer(required=True, default=lambda self: fields.Date.today().year)
    month = fields.Integer(default=lambda self: fields.Date.today().month)

    date_start = fields.Date(compute="_compute_dates", store=True)
    date_end = fields.Date(compute="_compute_dates", store=True)

    separador = fields.Selection(
        [("coma", "Coma (,)"), ("punto_y_coma", "Punto y coma (;)")],
        default="coma",
    )
    formato_archivo = fields.Selection(
        [("csv", "CSV"), ("txt", "TXT (tabulado)")], default="csv"
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("generated", "Generado"),
            ("confirmed", "Confirmado"),
        ],
        default="draft",
        tracking=True,
    )

    line_ids = fields.One2many("l10n_py.libro.line", "libro_id", string="Líneas")
    error_line_count = fields.Integer(compute="_compute_error_line_count", store=True)

    l10n_py_libro_attachment_ids = fields.Many2many(
        "ir.attachment", string="Archivos generados"
    )

    lote_letra = fields.Char(size=1, default=lambda self: self._default_lote_letra())
    lote_manual_override = fields.Char(size=5)
    lote_generation_seq = fields.Integer(default=0)

    _libro_period_unique = models.Constraint(
        "unique(company_id, tipo_registro, obligacion, year, month)",
        "Ya existe un libro para esta empresa/tipo de registro/obligación/período.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("lote_letra"):
                vals["lote_letra"] = LOTE_LETRA_MAP.get(
                    vals.get("tipo_registro"), False
                )
        return super().create(vals_list)

    def _default_lote_letra(self):
        tipo = self.env.context.get("default_tipo_registro")
        return LOTE_LETRA_MAP.get(tipo, False)

    @api.constrains("obligacion", "month")
    def _check_month(self):
        for libro in self:
            if libro.obligacion == "955":
                if not libro.month or not (1 <= libro.month <= 12):
                    raise ValidationError(
                        self.env._(
                            "El mes es obligatorio (1-12) para la obligación 955."
                        )
                    )
            elif libro.obligacion == "956" and libro.month not in (0, False):
                raise ValidationError(
                    self.env._("La obligación 956 (anual) no usa el mes: déjelo en 0.")
                )

    @api.constrains("lote_manual_override")
    def _check_lote_manual_override(self):
        for libro in self:
            value = libro.lote_manual_override
            if value and (len(value) > 5 or not value.isalnum()):
                raise ValidationError(
                    self.env._(
                        "El lote manual debe tener hasta 5 caracteres alfanuméricos."
                    )
                )

    @api.depends("year", "month", "obligacion")
    def _compute_dates(self):
        for libro in self:
            if libro.obligacion == "955" and libro.year and libro.month:
                last_day = calendar.monthrange(libro.year, libro.month)[1]
                libro.date_start = date(libro.year, libro.month, 1)
                libro.date_end = date(libro.year, libro.month, last_day)
            elif libro.obligacion == "956" and libro.year:
                libro.date_start = date(libro.year, 1, 1)
                libro.date_end = date(libro.year, 12, 31)
            else:
                libro.date_start = False
                libro.date_end = False

    @api.depends("line_ids.state")
    def _compute_error_line_count(self):
        for libro in self:
            libro.error_line_count = len(
                libro.line_ids.filtered(lambda line: line.state == "erro")
            )

    # ============== HELPERS DE GENERACIÓN (Ventas/Compras) ==============

    def _get_associated_move(self, move):
        if move.reversed_entry_id:
            return move.reversed_entry_id
        if "debit_origin_id" in move._fields and move.debit_origin_id:
            return move.debit_origin_id
        assoc = move.l10n_py_associated_document_ids[:1]
        if assoc and assoc.cdc:
            original = self.env["account.move"].search(
                [
                    ("l10n_py_cdc", "=", assoc.cdc),
                    ("company_id", "=", move.company_id.id),
                ],
                limit=1,
            )
            if original:
                return original
        return self.env["account.move"]

    def _get_move_target_tipo_registro(self, move):
        doc_code = move.l10n_latam_document_type_id.code
        if doc_code not in ("5", "6"):
            if move.move_type in ("out_invoice", "out_refund"):
                return "ventas"
            if move.move_type in ("in_invoice", "in_refund"):
                return "compras"
            return False
        original = self._get_associated_move(move)
        original_side = (
            "own"
            if original and original.move_type in ("out_invoice", "out_refund")
            else "third"
        )
        tipo_nc_nd = "110" if doc_code == "5" else "111"
        direction = move.company_id.l10n_py_libro_nc_nd_direction
        return NC_ND_TABLE[direction][(tipo_nc_nd, original_side)]

    def _get_codigo_tabla4(self, move):
        doc_type = move.l10n_latam_document_type_id
        if not doc_type:
            return False
        mapping = (
            self.env["l10n_py.libro.document.type.map"]
            .with_context(active_test=False)
            .search([("l10n_latam_document_type_id", "=", doc_type.id)], limit=1)
        )
        return mapping.codigo_tabla4 if mapping else False

    def _convert_amount_to_pyg(self, move, value):
        company = move.company_id
        if move.currency_id == company.currency_id:
            return value
        if move.l10n_py_exchange_rate and move.l10n_py_exchange_rate > 0:
            return value * move.l10n_py_exchange_rate
        return move.currency_id._convert(
            value,
            company.currency_id,
            company,
            move.invoice_date or fields.Date.today(),
        )

    def _get_amounts_in_pyg(self, move):
        b10 = round(
            self._convert_amount_to_pyg(move, move.l10n_py_amount_subtotal_10 or 0)
        )
        b5 = round(
            self._convert_amount_to_pyg(move, move.l10n_py_amount_subtotal_5 or 0)
        )
        # Field 11 of the DNIT spec is "no gravado o exento": the exonerated
        # amount (l10n_py_account) belongs there together with the exempt one.
        exento = round(
            self._convert_amount_to_pyg(
                move,
                (move.l10n_py_amount_exempt or 0)
                + (move.l10n_py_amount_exonerado or 0),
            )
        )
        # Each bucket is converted and rounded on its own. Only a rounding
        # residue is absorbed by the largest bucket; a bigger gap is left in
        # place so the line check against the invoice total reports it.
        target_total = self._get_total_in_pyg(move)
        residue = target_total - (b10 + b5 + exento)
        if residue and abs(residue) <= LIBRO_ROUNDING_TOLERANCE:
            buckets = {"b10": b10, "b5": b5, "exento": exento}
            nonzero = {key: value for key, value in buckets.items() if value}
            if nonzero:
                largest_key = max(nonzero, key=nonzero.get)
                buckets[largest_key] += residue
                b10, b5, exento = buckets["b10"], buckets["b5"], buckets["exento"]
        return b10, b5, exento

    def _get_total_in_pyg(self, move):
        return round(self._convert_amount_to_pyg(move, move.amount_total or 0))

    def _build_line_vals(self, move, target_tipo):
        is_own = move.move_type in ("out_invoice", "out_refund")
        partner = move.partner_id
        codigo_tabla4 = self._get_codigo_tabla4(move)
        company = move.company_id

        id_map = self.env["l10n_py.libro.identification.type.map"]
        tipo_ident = id_map._get_codigo(partner)

        vals = {
            "f_tipo_comprobante": codigo_tabla4,
            "f_fecha_emision": move.invoice_date or move.date,
            "f_nombre_razon_social": partner.name,
            "f_tipo_identificacion": tipo_ident or "11",
            "f_numero_identificacion": partner.l10n_py_ruc or (partner.vat or ""),
            "f_moneda_extranjera": (
                "S" if move.currency_id != company.currency_id else "N"
            ),
            "f_condicion": move.l10n_py_condicion_venta or "1",
            "f_imputa_iva": "S" if company.l10n_py_libro_iva_activo else "N",
            "f_imputa_ire": "S" if company.l10n_py_libro_ire_activo else "N",
            "f_imputa_irp_rsp": "S" if company.l10n_py_libro_irp_rsp_activo else "N",
            "f_no_imputa": "N",
        }

        if is_own:
            vals["f_timbrado"] = move.l10n_py_authorization_id.name or False
            vals["f_numero_comprobante"] = move.l10n_py_full_invoice_number or False
        else:
            vals["f_timbrado"] = move.l10n_py_libro_supplier_timbrado or False
            vals["f_numero_comprobante"] = move.l10n_py_libro_supplier_number or False
        if codigo_tabla4 == "107":
            vals["f_timbrado"] = "0"

        if target_tipo == "compras" and codigo_tabla4 in ZERO_BREAKDOWN_CODES:
            vals.update(
                {
                    "f_monto_gravado_10": 0,
                    "f_monto_gravado_5": 0,
                    "f_monto_exento": 0,
                    "f_monto_total": self._get_total_in_pyg(move),
                }
            )
        else:
            b10, b5, exento = self._get_amounts_in_pyg(move)
            vals.update(
                {
                    "f_monto_gravado_10": b10,
                    "f_monto_gravado_5": b5,
                    "f_monto_exento": exento,
                    "f_monto_total": self._get_total_in_pyg(move),
                }
            )

        if codigo_tabla4 in ("110", "111"):
            original = self._get_associated_move(move)
            if original:
                orig_own = original.move_type in ("out_invoice", "out_refund")
                if orig_own:
                    vals["f_comprobante_asociado_numero"] = (
                        original.l10n_py_full_invoice_number or False
                    )
                    vals["f_comprobante_asociado_timbrado"] = (
                        original.l10n_py_authorization_id.name or False
                    )
                else:
                    vals["f_comprobante_asociado_numero"] = (
                        original.l10n_py_libro_supplier_number or False
                    )
                    vals["f_comprobante_asociado_timbrado"] = (
                        original.l10n_py_libro_supplier_timbrado or False
                    )
        return vals

    def action_generate_lines(self, line_ids=None):
        Line = self.env["l10n_py.libro.line"]
        for libro in self:
            if libro.state not in ("draft", "generated"):
                continue
            if libro.tipo_registro not in ("ventas", "compras"):
                # Ingresos/Egresos son 100% manuales (D6): sin regeneración.
                continue

            candidate_lines = libro.line_ids.filtered(
                lambda line: line.move_id and not line.manual_override
            )
            if line_ids:
                candidate_lines = candidate_lines & line_ids
                moves = candidate_lines.mapped("move_id")
            else:
                domain = [
                    ("company_id", "=", libro.company_id.id),
                    ("state", "=", "posted"),
                    (
                        "move_type",
                        "in",
                        ("out_invoice", "out_refund", "in_invoice", "in_refund"),
                    ),
                ]
                if libro.date_start:
                    domain.append(("invoice_date", ">=", libro.date_start))
                if libro.date_end:
                    domain.append(("invoice_date", "<=", libro.date_end))
                moves = self.env["account.move"].search(domain)

            existing_by_move = {line.move_id.id: line for line in candidate_lines}
            keep_move_ids = set()
            for move in moves:
                target = libro._get_move_target_tipo_registro(move)
                if target != libro.tipo_registro:
                    continue
                if target == "ventas" and move.l10n_py_edi_status == "accepted":
                    continue
                if target == "compras" and move.l10n_py_libro_electronic:
                    continue
                vals = libro._build_line_vals(move, target)
                keep_move_ids.add(move.id)
                if move.id in existing_by_move:
                    existing_by_move[move.id].with_context(
                        l10n_py_libro_regenerating=True
                    ).write(vals)
                else:
                    Line.with_context(l10n_py_libro_regenerating=True).create(
                        dict(vals, libro_id=libro.id, move_id=move.id)
                    )

            stale = candidate_lines.filtered(
                lambda line, keep=keep_move_ids: line.move_id.id not in keep
            )
            stale.unlink()

            if libro.state == "draft":
                libro.state = "generated"
        return True

    def action_reopen(self):
        for libro in self:
            libro.message_post(body=self.env._("Libro reaberto para edição."))
            libro.state = "generated"

    def action_confirm(self):
        for libro in self:
            libro.line_ids._compute_state()
            if libro.error_line_count:
                raise UserError(
                    self.env._(
                        "Existem %(count)s línea(s) en estado erro. Corríjalas "
                        "antes de confirmar el libro.",
                        count=libro.error_line_count,
                    )
                )
            if not libro.line_ids:
                libro.message_post(
                    body=self.env._("Confirmado sin líneas (período vacío).")
                )
            libro.state = "confirmed"

    # ============== SERIALIZACIÓN / ZIP ==============

    def _get_file_basename(self, xxxxx):
        self.ensure_one()
        ruc = self.company_id.l10n_py_ruc or ""
        if self.obligacion == "955":
            periodo = f"{self.month:02d}{self.year}"
        else:
            periodo = str(self.year)
        return f"{ruc}_REG_{periodo}_{xxxxx}"

    def _get_delimiter(self):
        self.ensure_one()
        if self.formato_archivo == "txt":
            return "\t"
        return ";" if self.separador == "punto_y_coma" else ","

    def _serialize_chunk(self, lines):
        delimiter = self._get_delimiter()
        output = io.StringIO()
        writer = csv.writer(output, delimiter=delimiter, lineterminator="\r\n")
        for line in lines:
            writer.writerow(serialize_line(line))
        return output.getvalue().encode("utf-8")

    def action_download_zip(self):
        for libro in self:
            libro.line_ids._compute_state()
            if libro.error_line_count:
                raise UserError(
                    self.env._(
                        "Existem %(count)s línea(s) en estado erro. Corríjalas "
                        "antes de descargar el archivo.",
                        count=libro.error_line_count,
                    )
                )
            if not libro.line_ids:
                continue
            lines = libro.line_ids
            if libro.lote_manual_override and len(lines) > MAX_LINES_PER_FILE:
                raise UserError(
                    self.env._(
                        "XXXXX manual não suporta múltiplos sub-lotes neste "
                        "período; limpe o override ou gere um valor por "
                        "sub-lote manualmente depois."
                    )
                )
            chunks = [
                lines[i : i + MAX_LINES_PER_FILE]
                for i in range(0, len(lines), MAX_LINES_PER_FILE)
            ]
            seq = libro.lote_generation_seq
            if not libro.lote_manual_override:
                if seq > 99:
                    raise UserError(
                        self.env._("Se agotó la secuencia de generación (00-99).")
                    )
                libro.lote_generation_seq = seq + 1
            ext = "csv" if libro.formato_archivo == "csv" else "txt"
            for idx, chunk in enumerate(chunks):
                if idx > 99:
                    raise UserError(
                        self.env._("Se agotó el número de sub-lotes (00-99).")
                    )
                if libro.lote_manual_override:
                    xxxxx = libro.lote_manual_override
                else:
                    xxxxx = "{}{:02d}{:02d}".format(libro.lote_letra or "X", seq, idx)
                basename = libro._get_file_basename(xxxxx)
                filename = f"{basename}.{ext}"
                content = libro._serialize_chunk(chunk)
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.writestr(filename, content)
                zip_name = f"{basename}.zip"
                attachment = self.env["ir.attachment"].create(
                    {
                        "name": zip_name,
                        "raw": buf.getvalue(),
                        "res_model": "l10n_py.libro",
                        "res_id": libro.id,
                    }
                )
                libro.l10n_py_libro_attachment_ids = [(4, attachment.id)]
        return True
