# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import logging
import time
from datetime import datetime, timedelta

from odoo import SUPERUSER_ID, api, fields, models
from odoo.exceptions import UserError

from ..services.client import SifendeTransportError
from .edi_connector import APPROVED_STATES, KUDE_MAX_WAIT

_logger = logging.getLogger(__name__)

CRON_BATCH_SIZE = 200
CRON_TIME_BUDGET = 45
# la cancelación vence a los 7 días de la emisión (OCA) y sobra un margen
CANCEL_WATCH_DAYS = 10
CANCEL_RECHECK_HOURS = 1
FAILED_RECHECK_HOURS = 1
PAYMENT_CHEQUE = "2"
PAYMENT_CARDS = ("3", "4")
CHEQUE_NUMBER_MAX = 8
CHEQUE_BANK_RANGE = (4, 20)
DOC_INVOICE = "1"
DOC_SELF_INVOICE = "4"
DOC_CREDIT_NOTE = "5"
DOC_DEBIT_NOTE = "6"
DOC_DELIVERY_NOTE = "7"
CAPITAL_DEPARTMENT_CODE = 1
RESUBMITTED_STATES = ("PENDIENTE", "EN_LOTE", "ENVIADO")
FROZEN_PAYMENT_FIELDS = (
    "l10n_py_payment_type",
    "l10n_py_sifende_cheque_numero",
    "l10n_py_sifende_cheque_banco",
    "l10n_py_sifende_tarjeta_marca",
    "invoice_payment_term_id",
)
FROZEN_FISCAL_FIELDS = (
    "l10n_py_emission_type",
    "l10n_py_transaction_type",
    "l10n_py_presence_type",
    "l10n_py_exchange_rate_condition",
    "l10n_py_receipt_id",
    "l10n_py_contingency_motive",
    "l10n_py_nre_motive",
    "l10n_py_nre_estimated_invoice_date",
    "l10n_py_transport_id",
    "l10n_py_sifende_motivo_emision",
    "l10n_py_sifende_responsable_emision",
    "l10n_py_sifende_km_recorrido",
    "l10n_py_afe_constancia_type",
    "l10n_py_afe_constancia_number",
    "l10n_py_afe_constancia_control",
    "l10n_py_afe_vendor_doc_type",
    "l10n_py_afe_vendor_doc_number",
    "l10n_py_afe_vendor_name",
    "l10n_py_afe_vendor_address",
    "l10n_py_afe_vendor_house",
    "l10n_py_afe_vendor_department",
    "l10n_py_afe_vendor_district",
    "l10n_py_afe_vendor_city",
    "l10n_py_afe_provision_address",
    "l10n_py_afe_provision_department",
    "l10n_py_afe_provision_district",
    "l10n_py_afe_provision_city",
)
WEBHOOK_STATES = {
    "documento.aprobado": "APROBADO",
    "documento.rechazado": "RECHAZADO",
    "documento.cancelado": "CANCELADO",
}


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_py_authorization_id = fields.Many2one(
        compute="_compute_l10n_py_authorization_id", store=True, readonly=False
    )
    l10n_py_receipt_id = fields.Char(string="ID de recibo")
    l10n_py_sifende_enabled = fields.Boolean(compute="_compute_l10n_py_sifende_enabled")
    l10n_py_sifende_sandbox = fields.Boolean(compute="_compute_l10n_py_sifende_sandbox")
    l10n_py_sifende_intento = fields.Integer(
        string="Intento de envío a Sifende",
        default=0,
        copy=False,
        readonly=True,
    )
    l10n_py_sifende_reintento_misma_clave = fields.Boolean(copy=False)
    l10n_py_sifende_frozen = fields.Boolean(compute="_compute_l10n_py_sifende_frozen")
    l10n_py_sifende_envio_fallido = fields.Boolean(copy=False)
    l10n_py_sifende_numero_ocupado = fields.Boolean(copy=False, readonly=True)
    l10n_py_sifende_cdc_existente = fields.Char(copy=False, readonly=True)
    l10n_py_sifende_archivos_pendientes = fields.Boolean(copy=False)
    l10n_py_sifende_ultima_consulta = fields.Datetime(copy=False, readonly=True)
    l10n_py_sifende_event_key = fields.Char(copy=False, readonly=True)
    l10n_py_sifende_motivo_emision = fields.Selection(
        [
            ("1", "Devolución y ajuste de precios"),
            ("2", "Devolución"),
            ("3", "Descuento"),
            ("4", "Bonificación"),
            ("5", "Crédito incobrable"),
            ("6", "Recupero de costo"),
            ("7", "Recupero de gasto"),
            ("8", "Ajuste de precio"),
        ],
        string="Motivo de emisión (SIFEN)",
        compute="_compute_l10n_py_sifende_motivo_emision",
        store=True,
        readonly=False,
        copy=False,
    )
    l10n_py_sifende_responsable_emision = fields.Selection(
        [
            ("1", "Emisor de la factura"),
            ("2", "Poseedor de la factura y bienes"),
            ("3", "Empresa transportista"),
            ("4", "Despachante de aduanas"),
            ("5", "Agente de transporte o intermediario"),
        ],
        string="Responsable de la emisión de la NRE",
        default="1",
    )
    l10n_py_sifende_km_recorrido = fields.Integer(
        string="Kilómetros del recorrido (NRE)"
    )
    l10n_py_sifende_cheque_numero = fields.Char(
        string="Número del cheque (SIFEN)", copy=False
    )
    l10n_py_sifende_cheque_banco = fields.Char(
        string="Banco del cheque (SIFEN)", copy=False
    )
    l10n_py_sifende_tarjeta_marca = fields.Selection(
        [
            ("1", "Visa"),
            ("2", "Mastercard"),
            ("3", "American Express"),
            ("4", "Maestro"),
            ("5", "Panal"),
            ("6", "Cabal"),
            ("99", "Otra"),
        ],
        string="Marca de la tarjeta (SIFEN)",
        copy=False,
    )

    def _compute_l10n_py_sifende_enabled(self):
        for move in self:
            move.l10n_py_sifende_enabled = bool(move._l10n_py_sifende_connector())

    def _compute_l10n_py_sifende_sandbox(self):
        for move in self:
            connector = move._l10n_py_sifende_connector()
            move.l10n_py_sifende_sandbox = bool(
                connector and connector._sifende_is_sandbox()
            )

    @api.depends("reversed_entry_id", "l10n_latam_document_type_id")
    def _compute_l10n_py_sifende_motivo_emision(self):
        for move in self:
            code = move.l10n_latam_document_type_id.code
            if code == DOC_CREDIT_NOTE:
                move.l10n_py_sifende_motivo_emision = (
                    "2" if move.reversed_entry_id else "1"
                )
            elif code == DOC_DEBIT_NOTE:
                move.l10n_py_sifende_motivo_emision = "8"
            else:
                move.l10n_py_sifende_motivo_emision = False

    # === Timbrado y documento asociado por defecto ===

    def _l10n_py_sifende_uses_documents(self):
        self.ensure_one()
        return bool(
            self.move_type in ("out_invoice", "out_refund")
            and self.company_id.country_id.code == "PY"
            and self.journal_id.l10n_latam_use_documents
            and self.l10n_latam_document_type_id
        )

    def _l10n_py_sifende_default_authorization(self):
        """Timbrado del diario para el tipo de documento: uno por tipo, mismo número."""
        self.ensure_one()
        base = self.journal_id.l10n_py_authorization_id
        if not (base and self._l10n_py_sifende_uses_documents()):
            return base.browse()
        candidates = self.env["account.authorization"].search(
            [
                ("company_id", "=", self.company_id.id),
                ("active", "=", True),
                ("state", "!=", "expired"),
                ("name", "=", base.name),
                ("establishment", "=", self.journal_id.l10n_py_establishment),
                ("expedition_point", "=", self.journal_id.l10n_py_point),
                (
                    "l10n_latam_document_type_id",
                    "=",
                    self.l10n_latam_document_type_id.id,
                ),
            ]
        )
        return base if base in candidates else candidates[:1]

    @api.depends("journal_id", "l10n_latam_document_type_id")
    def _compute_l10n_py_authorization_id(self):
        for move in self:
            current = move.l10n_py_authorization_id
            doc_type = move.l10n_latam_document_type_id
            if move.state == "draft" and not (
                current and current.l10n_latam_document_type_id == doc_type
            ):
                current = move._l10n_py_sifende_default_authorization()
            move.l10n_py_authorization_id = current

    def action_post(self):
        for move in self:
            if (
                move.l10n_py_edi_status == "cancelled"
                and move.l10n_py_cdc
                and move._l10n_py_sifende_connector()
            ):
                raise UserError(
                    self.env._(
                        "El documento %(name)s fue cancelado en SIFEN y su número "
                        "no se reutiliza. Cancele este asiento en Odoo y emita un "
                        "documento nuevo.",
                        name=move.l10n_py_cdc,
                    )
                )
        self._l10n_py_sifende_assign_number()
        res = super().action_post()
        self._l10n_py_sifende_link_origin_document()
        return res

    def _l10n_py_sifende_assign_number(self):
        # como OCA, pero sin bajar de «Número Desde» ni de los números ocupados
        for move in self:
            authorization = move.l10n_py_authorization_id
            if (
                move.l10n_py_invoice_number
                or not authorization
                or not self.env.registry.ready
                or not move._l10n_py_sifende_connector()
                or not move._l10n_py_sifende_uses_documents()
            ):
                continue
            authorization.check_validity()
            move.l10n_py_invoice_number = move._l10n_py_sifende_free_number()

    def _l10n_py_sifende_free_number(self):
        self.ensure_one()
        authorization = self.l10n_py_authorization_id
        number = authorization._l10n_py_sifende_next_number(exclude_move=self)
        if number > authorization.invoice_number_to:
            raise UserError(
                self.env._(
                    "La faja de numeración está agotada para el timbrado %(timbrado)s.",
                    timbrado=authorization.name,
                )
            )
        authorization.check_number_available(number, exclude_move_id=self.id)
        return number

    def _l10n_py_sifende_origin(self):
        self.ensure_one()
        code = self.l10n_latam_document_type_id.code
        if code == DOC_CREDIT_NOTE:
            return self.reversed_entry_id
        if code == DOC_DEBIT_NOTE and "debit_origin_id" in self._fields:
            return self.debit_origin_id
        return self.browse()

    def _l10n_py_sifende_link_origin_document(self):
        for move in self:
            origin = move._l10n_py_sifende_origin()
            if (
                origin.l10n_py_cdc
                and not move.l10n_py_associated_document_ids
                and not move._l10n_py_sifende_frozen()
            ):
                self.env["l10n_py.associated.document"].sudo().create(
                    {
                        "move_id": move.id,
                        "association_type": "1",
                        "cdc": origin.l10n_py_cdc,
                    }
                )

    def _l10n_py_sifende_connector(self):
        self.ensure_one()
        return (
            self.env["l10n_py.edi.connector"]
            .sudo()
            .search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("provider_type", "=", "sifende"),
                ],
                limit=1,
            )
        )

    def _l10n_py_sifende_idempotency_key(self):
        self.ensure_one()
        database = self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        return f"odoo:{database}:{self.id}:{self.l10n_py_sifende_intento}"

    # === Datos de pago congelados ===

    def _l10n_py_sifende_frozen(self):
        self.ensure_one()
        sent = self.l10n_py_cdc or self.l10n_py_edi_status in (
            "sent",
            "processing",
            "accepted",
        )
        if sent and self._l10n_py_sifende_connector():
            return True
        return self._l10n_py_sifende_pending_send()

    # sin CDC no se sabe si Sifende registró el original: el reintento reusa la clave
    def _l10n_py_sifende_pending_send(self):
        self.ensure_one()
        return bool(
            self.l10n_py_edi_status == "error"
            and self.l10n_py_sifende_reintento_misma_clave
            and self._l10n_py_sifende_connector()
        )

    @api.depends(
        "company_id",
        "l10n_py_cdc",
        "l10n_py_edi_status",
        "l10n_py_sifende_reintento_misma_clave",
    )
    def _compute_l10n_py_sifende_frozen(self):
        for move in self:
            move.l10n_py_sifende_frozen = move._l10n_py_sifende_frozen()

    def _l10n_py_sifende_frozen_error(self, fiscal=False, amounts=False):
        if amounts:
            what = self.env._("Los importes y los datos de pago")
        elif fiscal:
            what = self.env._("Los datos fiscales")
        else:
            what = self.env._("Los datos de pago")
        if self._l10n_py_sifende_pending_send() and not self.l10n_py_cdc:
            return UserError(
                self.env._(
                    "%(what)s de un documento con el envío a Sifende pendiente de "
                    "confirmación no se pueden modificar: reintente el envío con "
                    "«Reintentar».",
                    what=what,
                )
            )
        return UserError(
            self.env._(
                "%(what)s de un documento enviado a Sifende no se pueden modificar: "
                "SIFEN ya tiene los del documento %(name)s.",
                what=what,
                name=self.l10n_py_cdc or self.name,
            )
        )

    def _l10n_py_sifende_with_sifen(self):
        self.ensure_one()
        return bool(
            self.l10n_py_edi_status in ("sent", "processing", "accepted")
            and self._l10n_py_sifende_connector()
        )

    @api.depends("l10n_py_edi_status", "l10n_py_sifende_reintento_misma_clave")
    def _compute_show_reset_to_draft_button(self):
        res = super()._compute_show_reset_to_draft_button()
        for move in self:
            if move.show_reset_to_draft_button and (
                move._l10n_py_sifende_with_sifen()
                or move._l10n_py_sifende_pending_send()
            ):
                move.show_reset_to_draft_button = False
        return res

    def button_draft(self):
        for move in self:
            if move._l10n_py_sifende_pending_send():
                raise move._l10n_py_sifende_frozen_error()
            if move._l10n_py_sifende_with_sifen():
                raise UserError(
                    self.env._(
                        "El documento %(name)s ya fue enviado a Sifende y no se "
                        "puede restablecer a borrador. Cancélelo con «Cancelar EDI» "
                        "o anúlelo con una nota de crédito.",
                        name=move.l10n_py_cdc or move.name,
                    )
                )
        return super().button_draft()

    def write(self, vals):
        changed = [
            name
            for name in FROZEN_PAYMENT_FIELDS + FROZEN_FISCAL_FIELDS
            if name in vals
        ]
        if changed:
            for move in self:
                if not move._l10n_py_sifende_frozen():
                    continue
                for name in changed:
                    if move._l10n_py_sifende_changes(name, vals[name]):
                        raise move._l10n_py_sifende_frozen_error(
                            name in FROZEN_FISCAL_FIELDS
                        )
        return super().write(vals)

    def _l10n_py_sifende_changes(self, name, value):
        field = self._fields[name]
        if field.type == "date":
            value = fields.Date.to_date(value)
        return field.convert_to_write(self[name], self) != (value or False)

    # === Datos adicionales para Sifende ===

    def _prepare_edi_document_data(self):
        data = super()._prepare_edi_document_data()
        if self._l10n_py_sifende_connector():
            data["sifende"] = self._l10n_py_sifende_extra_data()
        return data

    def _prepare_invoice_lines(self):
        items = super()._prepare_invoice_lines()
        if self._l10n_py_sifende_connector():
            lines = self.invoice_line_ids.filtered(
                lambda line: line.display_type not in ("line_section", "line_note")
            )
            for item, line in zip(items, lines, strict=True):
                item["sifende"] = self._l10n_py_sifende_item_data(line)
        return items

    def _l10n_py_sifende_extra_data(self):
        self.ensure_one()
        code = self.l10n_latam_document_type_id.code
        extra = {
            "moveId": self.id,
            "idempotencyKey": self._l10n_py_sifende_idempotency_key(),
            "montoTotal": self.amount_total,
            "totalOperacion": self._l10n_py_sifende_operation_total(),
            "decimales": self.currency_id.decimal_places,
            "cliente": {
                "email": self.partner_id.email or None,
                "codigoCliente": self.partner_id.ref or None,
            },
        }
        if self.l10n_py_payment_type in PAYMENT_CARDS and (
            self.l10n_py_sifende_tarjeta_marca
        ):
            extra["tarjeta"] = {"tipoTarjeta": int(self.l10n_py_sifende_tarjeta_marca)}
        if code in (DOC_CREDIT_NOTE, DOC_DEBIT_NOTE):
            extra["motivoEmision"] = (
                int(self.l10n_py_sifende_motivo_emision or 0) or None
            )
        if code == DOC_DELIVERY_NOTE:
            extra["remision"] = {
                "responsableEmision": int(
                    self.l10n_py_sifende_responsable_emision or 1
                ),
                "kilometrosRecorrido": self.l10n_py_sifende_km_recorrido,
            }
        return extra

    def _l10n_py_sifende_operation_total(self):
        # sin la línea de redondeo de efectivo: es lo que Sifende redondea
        self.ensure_one()
        return self.currency_id.round(
            sum(
                line.price_total
                for line in self.invoice_line_ids
                if line.display_type == "product"
            )
        )

    def _l10n_py_sifende_city_name(self):
        partner = self.partner_id
        # res.city de OCA no usa los códigos de SIFEN; Capital tiene una sola ciudad
        if partner.l10n_py_department_code == CAPITAL_DEPARTMENT_CODE:
            return "Asunción"
        return partner.city_id.name or partner.city

    @api.model
    def _l10n_py_sifende_item_data(self, line):
        uom = line.product_uom_id or line.product_id.uom_id
        untaxed_rate = sum(
            tax.amount
            for tax in line.tax_ids
            if tax.amount_type == "percent" and not tax.price_include
        )
        item = {
            "unidadMedida": uom.l10n_py_sifende_unidad_medida or 77,
            "precioUnitario": round(line.price_unit * (1 + untaxed_rate / 100), 8),
        }
        if line.discount:
            item["descuentoParticularPorcentaje"] = line.discount
        return item

    def _l10n_py_sifende_is_cash(self):
        self.ensure_one()
        due_dates = [due for due, _amount in self._l10n_py_sifende_installments()]
        return not due_dates or due_dates == [self.invoice_date]

    def _prepare_payment_condition(self):
        if not self._l10n_py_sifende_connector():
            return super()._prepare_payment_condition()
        self.ensure_one()
        if self._l10n_py_sifende_is_cash():
            payment = {
                "tipo": int(self.l10n_py_payment_type or "1"),
                "monto": str(self.amount_total),
                "moneda": self.currency_id.name,
                "cambio": 0,
            }
            if self.l10n_py_payment_type == PAYMENT_CHEQUE:
                payment["cheque"] = {
                    "numeroCheque": self.l10n_py_sifende_cheque_numero,
                    "bancoCheque": self.l10n_py_sifende_cheque_banco,
                }
            return {"tipo": 1, "entregas": [payment]}
        installments = self._l10n_py_sifende_installments()
        term_days = (installments[0][0] - self.invoice_date).days
        return {
            "tipo": 2,
            "credito": {
                "tipo": 1,
                "plazo": f"{term_days} días",
                "cuotas": len(installments),
                "infoCuotas": [
                    {
                        "moneda": self.currency_id.name,
                        "monto": amount,
                        "vencimiento": due.strftime("%Y-%m-%d"),
                    }
                    for due, amount in installments
                ],
            },
        }

    def _l10n_py_sifende_installments(self):
        """Vencimientos y montos que Odoo calculó para las cuentas por cobrar."""
        self.ensure_one()
        if not self.invoice_payment_term_id:
            return []
        amounts = {}
        for line in self.line_ids:
            if line.display_type == "payment_term" and line.date_maturity:
                amounts[line.date_maturity] = (
                    amounts.get(line.date_maturity, 0.0) + line.amount_currency
                )
        return [
            (due, self.currency_id.round(amount))
            for due, amount in sorted(amounts.items())
        ]

    def _validate_edi_document_type(self):
        errors = super()._validate_edi_document_type()
        if not self._l10n_py_sifende_connector():
            return errors
        code = self.l10n_latam_document_type_id.code
        if not self.invoice_date:
            errors.append(self.env._("Indique la fecha de la factura."))
        if not (self.journal_id.l10n_py_authorization_id.name or "").strip().isdigit():
            errors.append(
                self.env._("El número de timbrado debe ser numérico para Sifende.")
            )
        if (
            code in (DOC_INVOICE, DOC_SELF_INVOICE)
            and self.l10n_py_payment_type == PAYMENT_CHEQUE
            and self._l10n_py_sifende_is_cash()
        ):
            errors.extend(self._l10n_py_sifende_cheque_errors())
        if (
            code == DOC_INVOICE
            and self.l10n_py_payment_type in PAYMENT_CARDS
            and not self.l10n_py_sifende_tarjeta_marca
            and self._l10n_py_sifende_is_cash()
        ):
            errors.append(self.env._("Pago con tarjeta: elija la marca de la tarjeta."))
        if code in (DOC_CREDIT_NOTE, DOC_DEBIT_NOTE):
            if not self.l10n_py_sifende_motivo_emision:
                errors.append(self.env._("Indique el motivo de emisión de la nota."))
            if not self.l10n_py_associated_document_ids:
                errors.append(
                    self.env._(
                        "Indique el documento asociado (Grupo H) de la nota: no hay "
                        "una factura de origen con CDC de la que tomarlo."
                    )
                )
        if code == DOC_DELIVERY_NOTE:
            if self.l10n_py_sifende_km_recorrido < 1:
                errors.append(
                    self.env._(
                        "Nota de Remisión: indique los kilómetros del recorrido."
                    )
                )
            if not self.l10n_py_transport_id:
                errors.append(
                    self.env._(
                        "Nota de Remisión: los datos de transporte son obligatorios."
                    )
                )
        return errors

    def _validate_edi_data(self):
        if self._l10n_py_sifende_connector():
            self._l10n_py_sifende_check_products()
        return super()._validate_edi_data()

    def _l10n_py_sifende_check_products(self):
        self.ensure_one()
        product_lines = self.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        )
        missing = [
            (position, line)
            for position, line in enumerate(product_lines, 1)
            if not line.product_id
        ]
        if missing:
            raise UserError(
                "\n".join(
                    self.env._(
                        "La línea %(line)s no tiene producto: elija uno, de él se "
                        "toman el código y el NCM que SIFEN exige.",
                        line=f'"{line.name}"'
                        if line.name
                        else self.env._("n.º %(position)s", position=position),
                    )
                    for position, line in missing
                )
            )

    def _l10n_py_sifende_cheque_errors(self):
        number = self.l10n_py_sifende_cheque_numero or ""
        bank = (self.l10n_py_sifende_cheque_banco or "").strip()
        errors = []
        if not (
            number.isascii() and number.isdigit() and len(number) <= CHEQUE_NUMBER_MAX
        ):
            errors.append(
                self.env._(
                    "Pago con cheque: indique el número del cheque (solo dígitos, "
                    "hasta %(max)s).",
                    max=CHEQUE_NUMBER_MAX,
                )
            )
        if not CHEQUE_BANK_RANGE[0] <= len(bank) <= CHEQUE_BANK_RANGE[1]:
            errors.append(
                self.env._(
                    "Pago con cheque: indique el banco (de %(min)s a %(max)s "
                    "caracteres).",
                    min=CHEQUE_BANK_RANGE[0],
                    max=CHEQUE_BANK_RANGE[1],
                )
            )
        return errors

    # === Envío y respuesta ===

    def _l10n_py_sifende_check_posted(self):
        self.ensure_one()
        if self.state != "posted":
            raise UserError(
                self.env._(
                    "Confirme la factura antes de enviarla a SIFENDE: solo se emiten "
                    "documentos publicados."
                )
            )

    def action_send_edi(self):
        self.ensure_one()
        connector = self._l10n_py_sifende_connector()
        if not connector:
            return super().action_send_edi()
        self._l10n_py_sifende_check_posted()
        connector._sifende_check_environment()
        if self._l10n_py_sifende_is_failed():
            raise UserError(self._l10n_py_sifende_failed_steps())
        self._l10n_py_sifende_link_origin_document()
        self._validate_edi_data()
        document_data = self._prepare_edi_document_data()
        self.l10n_py_edi_status = "sent"
        try:
            response = connector.send_document(document_data)
        except UserError as e:
            response = {"success": False, "edi_status": "error", "error": str(e)}
        if response.get("success"):
            self.l10n_py_sifende_reintento_misma_clave = False
            self._process_edi_response(response)
            return
        self.write(
            {
                "l10n_py_edi_status": response.get("edi_status") or "error",
                "l10n_py_edi_message": response.get("error"),
                "l10n_py_sifende_reintento_misma_clave": bool(
                    response.get("transient")
                ),
                "l10n_py_sifende_envio_fallido": False,
            }
        )
        if response.get("number_conflict"):
            self._l10n_py_sifende_register_number_conflict(response.get("existing_cdc"))

    def _l10n_py_sifende_is_same_document(self, cdc):
        self.ensure_one()
        number = str(self.l10n_py_invoice_number).zfill(7)
        return bool(
            cdc
            and len(cdc) == 44
            and cdc[17:24] == number
            and cdc[34:43] == self.l10n_py_security_code
        )

    def _l10n_py_sifende_register_number_conflict(self, cdc):
        self.ensure_one()
        values = {
            "l10n_py_sifende_numero_ocupado": True,
            "l10n_py_sifende_cdc_existente": cdc,
        }
        if self._l10n_py_sifende_is_same_document(cdc):
            self.write(values)
            return
        authorization = self.l10n_py_authorization_id.sudo()
        authorization.l10n_py_sifende_ultimo_numero_en_uso = max(
            authorization.l10n_py_sifende_ultimo_numero_en_uso,
            self.l10n_py_invoice_number,
        )
        self.write(values)

    def action_l10n_py_sifende_renumber(self):
        self.ensure_one()
        self.check_access("write")
        if not (
            self.state == "posted"
            and self.l10n_py_sifende_numero_ocupado
            and self._l10n_py_sifende_connector()
        ):
            raise UserError(
                self.env._(
                    "Solo se renumera un documento publicado cuyo número Sifende "
                    "informó como ya usado."
                )
            )
        if self.l10n_py_cdc or self._l10n_py_sifende_is_same_document(
            self.l10n_py_sifende_cdc_existente
        ):
            raise UserError(
                self.env._(
                    "El CDC %(cdc)s corresponde a este mismo documento: Sifende ya lo "
                    "emitió y su número no se cambia. Consulte su estado en el panel "
                    "de Sifende.",
                    cdc=self.l10n_py_cdc or self.l10n_py_sifende_cdc_existente,
                )
            )
        old_number = self.l10n_py_invoice_number
        number = self._l10n_py_sifende_free_number()
        self.write(
            {
                "l10n_py_invoice_number": number,
                "l10n_py_sifende_numero_ocupado": False,
                "l10n_py_sifende_cdc_existente": False,
                "l10n_py_sifende_intento": self.l10n_py_sifende_intento + 1,
                "l10n_py_sifende_reintento_misma_clave": False,
                "l10n_py_edi_status": "to_send",
                "l10n_py_edi_message": self.env._(
                    "Renumerado: el número %(old)s ya estaba en uso en Sifende y "
                    "ahora le corresponde el %(new)s. Pulse «Enviar a EDI».",
                    old=old_number,
                    new=number,
                ),
            }
        )

    def _process_edi_response(self, response):
        self.ensure_one()
        if not self._l10n_py_sifende_connector():
            return super()._process_edi_response(response)
        result = response.get("result") or {}
        cdc = result.get("cdc")
        self.write(
            {
                "l10n_py_cdc": cdc,
                "l10n_py_qr_string": result.get("qr"),
                "l10n_py_edi_status": "processing",
                "l10n_py_sifende_envio_fallido": False,
                "l10n_py_edi_message": self.env._(
                    "Enviado a Sifende; esperando la respuesta de SIFEN."
                ),
            }
        )
        self._l10n_py_generate_qr_image()

    def action_cancel_edi(self):
        self.ensure_one()
        connector = self._l10n_py_sifende_connector()
        if connector:
            self.check_access("write")
            connector._sifende_check_environment()
            if connector._sifende_is_sandbox():
                raise UserError(
                    self.env._(
                        "La cancelación no está disponible en SANDBOX: Sifende solo "
                        "cancela documentos emitidos en producción."
                    )
                )
        return super().action_cancel_edi()

    def action_retry_edi(self):
        self.ensure_one()
        if self._l10n_py_sifende_connector():
            self._l10n_py_sifende_check_posted()
            if self.l10n_py_sifende_numero_ocupado:
                raise UserError(self._l10n_py_sifende_number_steps())
            if self.l10n_py_edi_status == "rejected" and self.l10n_py_cdc:
                raise UserError(self._l10n_py_sifende_rejection_steps())
            if self._l10n_py_sifende_is_failed():
                raise UserError(self._l10n_py_sifende_failed_steps())
            if (
                self.l10n_py_edi_status in ("error", "rejected")
                and not self.l10n_py_sifende_reintento_misma_clave
            ):
                self.l10n_py_sifende_intento += 1
        return super().action_retry_edi()

    def _l10n_py_sifende_is_failed(self):
        self.ensure_one()
        return self.l10n_py_edi_status == "error" and self.l10n_py_sifende_envio_fallido

    def _l10n_py_sifende_number_steps(self):
        return self.env._(
            "Sifende ya tiene el número %(number)s de este documento y reenviarlo "
            "repite el error. Pulse «Renumerar»; si conoce el siguiente número libre "
            "del punto (panel de Sifende > Numeración), suba antes «Número Desde» "
            "del timbrado.",
            number=self.l10n_py_invoice_number,
        )

    def _l10n_py_sifende_failed_steps(self):
        return self.env._(
            "El envío a SIFEN de este documento falló y Odoo no lo reemite: el "
            "número y el CDC ya están tomados en Sifende. Reintente el lote desde "
            "el panel de Sifende o pídalo a soporte. Odoo actualiza el estado solo "
            "cuando el documento vuelva a procesarse (mismo CDC)."
        )

    def _l10n_py_sifende_rejection_steps(self):
        return self.env._(
            "SIFEN rechazó este documento y su número no se puede reenviar. "
            "Inutilice el número desde Facturación Electrónica > Inutilización de "
            "números, pulse Restablecer a borrador y Cancelar en este documento y "
            "emita uno nuevo."
        )

    def _generate_kude(self):
        self.ensure_one()
        connector = self._l10n_py_sifende_connector()
        if not connector:
            return super()._generate_kude()
        if not self.l10n_py_cdc:
            return
        self.check_access("write")
        pdf = connector._sifende_fetch_kude(
            self.l10n_py_cdc,
            document=self,
            max_wait=self.env.context.get("l10n_py_sifende_kude_wait", KUDE_MAX_WAIT),
        )
        self.write(
            {
                "l10n_py_kude_pdf": base64.b64encode(pdf),
                "l10n_py_kude_filename": f"KUDE_{self.l10n_py_cdc}.pdf",
            }
        )
        self._l10n_py_sifende_attach(
            f"KUDE_{self.l10n_py_cdc}.pdf", pdf, "application/pdf"
        )

    def _l10n_py_sifende_attach(self, name, content, mimetype):
        # los binarios de OCA no salen en el chatter: se adjuntan también como archivos
        self.ensure_one()
        attachments = self.env["ir.attachment"].with_user(SUPERUSER_ID)
        domain = [
            ("res_model", "=", "account.move"),
            ("res_id", "=", self.id),
            ("res_field", "=", False),
            ("name", "=", name),
        ]
        if not attachments.search_count(domain):
            attachments.create(
                {
                    "name": name,
                    "raw": content,
                    "mimetype": mimetype,
                    "res_model": "account.move",
                    "res_id": self.id,
                }
            )

    # === Cron ===

    @api.model
    def _cron_sifende_check_status(self):
        deadline = time.monotonic() + CRON_TIME_BUDGET
        connectors = (
            self.env["l10n_py.edi.connector"]
            .sudo()
            .search([("provider_type", "=", "sifende")])
        )
        # una sola cola: primero los documentos en curso de todos los conectores y
        # después los aceptados que se vigilan; dentro de cada grupo, por antigüedad,
        # así un conector con mucho trabajo no agota el presupuesto de los demás
        pending = [
            (group, move, connector)
            for connector in connectors
            for group, moves in enumerate(self._l10n_py_sifende_to_sync(connector))
            for move in moves
        ]
        pending.sort(
            key=lambda item: (
                item[0],
                item[1].l10n_py_sifende_ultima_consulta or datetime.min,
                item[1].id,
            )
        )
        for _group, move, connector in pending:
            if time.monotonic() > deadline:
                return
            try:
                with self.env.cr.savepoint():
                    move._l10n_py_sifende_sync(connector, kude_wait=0)
            except Exception:
                _logger.exception(
                    "Error consultando el estado en Sifende del documento %s",
                    move.name,
                )
            move.l10n_py_sifende_ultima_consulta = fields.Datetime.now()

    @api.model
    def _l10n_py_sifende_to_sync(self, connector):
        """Devuelve dos grupos: los documentos que esperan la respuesta de SIFEN
        o sus archivos, y los aceptados que se vigilan por si se cancelan. Los
        aceptados solo ocupan el lugar que los primeros dejan libre en el lote."""
        now = fields.Datetime.now()
        recheck = now - timedelta(hours=CANCEL_RECHECK_HOURS)
        failed_recheck = now - timedelta(hours=FAILED_RECHECK_HOURS)
        watch_from = fields.Date.context_today(self) - timedelta(days=CANCEL_WATCH_DAYS)
        moves = self.sudo()
        base = [
            ("company_id", "=", connector.company_id.id),
            ("l10n_py_cdc", "!=", False),
        ]
        # primero los que nunca se consultaron o hace más que se consultaron: así el
        # límite del lote rota por todos en lugar de repetir siempre los mismos
        order = "l10n_py_sifende_ultima_consulta asc nulls first, id"
        in_flight = moves.search(
            base
            + [
                "|",
                "|",
                ("l10n_py_edi_status", "=", "processing"),
                # el aviso de archivos pendientes puede quedar puesto en un
                # documento que se canceló antes de recibirlos
                "&",
                ("l10n_py_edi_status", "=", "accepted"),
                ("l10n_py_sifende_archivos_pendientes", "=", True),
                "&",
                "&",
                ("l10n_py_edi_status", "=", "error"),
                ("l10n_py_sifende_envio_fallido", "=", True),
                "|",
                ("l10n_py_sifende_ultima_consulta", "=", False),
                ("l10n_py_sifende_ultima_consulta", "<", failed_recheck),
            ],
            limit=CRON_BATCH_SIZE,
            order=order,
        )
        room = CRON_BATCH_SIZE - len(in_flight)
        if room <= 0:
            return in_flight, moves.browse()
        watched = moves.search(
            base
            + [
                ("l10n_py_edi_status", "=", "accepted"),
                ("l10n_py_sifende_archivos_pendientes", "=", False),
                ("invoice_date", ">=", watch_from),
                "|",
                ("l10n_py_sifende_ultima_consulta", "=", False),
                ("l10n_py_sifende_ultima_consulta", "<", recheck),
            ],
            limit=room,
            order=order,
        )
        return in_flight, watched

    def _l10n_py_sifende_sync(self, connector, kude_wait=KUDE_MAX_WAIT):
        self.ensure_one()
        if (
            self.l10n_py_edi_status in ("processing", "accepted")
            or self._l10n_py_sifende_is_failed()
        ):
            self._l10n_py_sifende_refresh_state(connector)
        if self.l10n_py_edi_status == "accepted":
            self._l10n_py_sifende_fetch_files(connector, kude_wait)

    def _l10n_py_sifende_refresh_state(self, connector, announced=None, message=None):
        self.ensure_one()
        # una consulta que no cambia el estado no se registra en el log EDI: el
        # cron vigila cada hora los documentos aceptados de los últimos días
        result = (
            connector._sifende_check_status(
                self.l10n_py_cdc, log=self._l10n_py_sifende_status_changes
            ).get("result")
            or {}
        )
        state = result.get("estado")
        if not (announced and message and self._sifende_same_outcome(announced, state)):
            message = result.get("mensajeRechazo")
        self._l10n_py_sifende_apply_state(state, message)

    @staticmethod
    def _sifende_same_outcome(announced, state):
        if announced == "APROBADO":
            return state in APPROVED_STATES
        return state == announced

    def _l10n_py_sifende_status_changes(self, response):
        body = response.body
        # una respuesta sin estado no es una consulta normal: se registra
        if not isinstance(body, dict) or not body.get("estado"):
            return True
        return bool(self._l10n_py_sifende_state_values(body["estado"]))

    def _l10n_py_sifende_apply_state(self, state, message=None):
        self.ensure_one()
        values = self._l10n_py_sifende_state_values(state, message)
        if values:
            self.write(values)

    def _l10n_py_sifende_state_values(self, state, message=None):
        self.ensure_one()
        status = self.l10n_py_edi_status
        failed = self._l10n_py_sifende_is_failed()
        in_flight = status == "processing" or failed
        if state in APPROVED_STATES and in_flight:
            return {
                "l10n_py_edi_status": "accepted",
                "l10n_py_sifende_envio_fallido": False,
                "l10n_py_edi_message": message
                or self.env._("Documento aprobado por SIFEN."),
            }
        if state == "RECHAZADO" and in_flight:
            return {
                "l10n_py_edi_status": "rejected",
                "l10n_py_edi_message": "\n\n".join(
                    (
                        message or self.env._("SIFEN rechazó el documento."),
                        self._l10n_py_sifende_rejection_steps(),
                    )
                ),
                "l10n_py_sifende_reintento_misma_clave": False,
                "l10n_py_sifende_envio_fallido": False,
            }
        if state == "ERROR" and status == "processing":
            return {
                "l10n_py_edi_status": "error",
                "l10n_py_sifende_envio_fallido": True,
                "l10n_py_sifende_reintento_misma_clave": False,
                "l10n_py_edi_message": "\n\n".join(
                    filter(None, (message, self._l10n_py_sifende_failed_steps()))
                ),
            }
        if state in RESUBMITTED_STATES and failed:
            return {
                "l10n_py_edi_status": "processing",
                "l10n_py_sifende_envio_fallido": False,
                "l10n_py_edi_message": self.env._(
                    "Sifende reintentó el envío; esperando la respuesta de SIFEN."
                ),
            }
        if state == "CANCELADO" and status in ("processing", "accepted"):
            return {"l10n_py_edi_status": "cancelled"}
        return {}

    def _l10n_py_sifende_apply_webhook(self, connector, event_type, data):
        self.ensure_one()
        announced = WEBHOOK_STATES[event_type]
        status = self.l10n_py_edi_status
        # los avisos pueden llegar desordenados: el estado vigente lo dice la consulta
        if (
            status == "processing"
            or self._l10n_py_sifende_is_failed()
            or (announced == "CANCELADO" and status == "accepted")
        ):
            results = data.get("resultados")
            message = "\n".join(
                f"{result.get('codigo')}: {result['mensaje']}"
                for result in results or []
                if isinstance(result, dict) and result.get("mensaje")
            )
            self._l10n_py_sifende_refresh_state(connector, announced, message or None)
        if self.l10n_py_edi_status == "accepted":
            self._l10n_py_sifende_fetch_files(connector, kude_wait=0)

    def _l10n_py_sifende_fetch_files(self, connector, kude_wait=KUDE_MAX_WAIT):
        self.ensure_one()
        pending = False
        if not self.l10n_py_edi_xml:
            try:
                xml = connector._sifende_fetch_xml(self.l10n_py_cdc, document=self)
                self.write(
                    {
                        "l10n_py_edi_xml": base64.b64encode(xml),
                        "l10n_py_edi_xml_filename": f"{self.l10n_py_cdc}.xml",
                    }
                )
                self._l10n_py_sifende_attach(
                    f"{self.l10n_py_cdc}.xml", xml, "application/xml"
                )
            except (UserError, SifendeTransportError) as e:
                pending = True
                _logger.info("XML de %s pendiente: %s", self.l10n_py_cdc, e)
        if not self.l10n_py_kude_pdf:
            try:
                self.with_context(l10n_py_sifende_kude_wait=kude_wait)._generate_kude()
            except (UserError, SifendeTransportError) as e:
                pending = True
                _logger.info("KuDE de %s pendiente: %s", self.l10n_py_cdc, e)
        self.l10n_py_sifende_archivos_pendientes = pending
