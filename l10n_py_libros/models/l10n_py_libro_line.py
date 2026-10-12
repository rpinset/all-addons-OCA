# l10n_py_libros/models/l10n_py_libro_line.py

from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError

FECHA_MINIMA_DNIT = date(2021, 1, 1)

# D4 - name-required exceptions (identificación exenta de exigir nombre/razón
# social), especificacao_tecnica_marangatu.txt:148-152 (Ventas), :250-254
# (Compras), :494-498 (Egresos, o tipo 206).
VENTAS_NOMBRE_EXEMPT_IDENT = {"11", "12", "15"}
COMPRAS_NOMBRE_EXEMPT_IDENT = {"11", "12"}
EGRESOS_NOMBRE_EXEMPT_IDENT = {"11", "12"}

# D4 - número de comprobante não requerido, :164-167 (Ventas), :268-274
# (Compras).
VENTAS_NUMERO_EXEMPT = {"112", "106"}
COMPRAS_NUMERO_EXEMPT = {"112", "106", "107"}

# D4 - Compras: tipo identificación = 11 (RUC) geral, exceto 101/107,
# :242-246.
COMPRAS_IDENT_LIBRE = {"101", "107"}

# D4 - Egresos: campo 5 tipo identificación, :468-486. Não requerido
# (nem campo 6) para 206/207/211; fixo 11 para 204/205; fixo 17 para 202.
EGRESOS_IDENT_EXEMPT = {"206", "207", "211"}
EGRESOS_IDENT_FIXED = {"204": "11", "205": "11", "202": "17"}

# D4 - Ingresos: campo 5 tipo identificación, :383-389. 210 restrito a
# 11/12/13; 208 fixo 11.
INGRESOS_IDENT_210_ALLOWED = {"11", "12", "13"}
INGRESOS_IDENT_FIXED = {"208": "11"}

TIPO_COMPROBANTE_SELECTION = [
    ("101", "101 - Autofactura"),
    ("102", "102 - Boleta Transporte Público"),
    ("103", "103 - Boleta de Venta"),
    ("104", "104 - Boleta Resimple"),
    ("105", "105 - Boletos de Loterías/Juegos de Azar"),
    ("106", "106 - Boleto/Ticket Transporte Aéreo"),
    ("107", "107 - Despacho de Importación"),
    ("108", "108 - Entrada Espectáculos Públicos"),
    ("109", "109 - Factura"),
    ("110", "110 - Nota de Crédito"),
    ("111", "111 - Nota de Débito"),
    ("112", "112 - Ticket Máquina Registradora"),
    ("201", "201 - Comprobante de Egresos por Compras a Crédito"),
    ("202", "202 - Comprobante del Exterior Legalizado"),
    ("203", "203 - Comprobante de Ingreso por Ventas a Crédito"),
    ("204", "204 - Comprobante Ingresos Entidades Públicas/Religiosas"),
    ("205", "205 - Extracto de Cuenta - Billetaje Electrónico"),
    ("206", "206 - Extracto de Cuenta de IPS"),
    ("207", "207 - Extracto de Cuenta TC/TD"),
    ("208", "208 - Liquidación de Salario"),
    ("209", "209 - Otros Comprobantes de Egresos"),
    ("210", "210 - Otros Comprobantes de Ingresos"),
    ("211", "211 - Transferencias o Giros Bancarios/Boleta de Depósito"),
]

ZERO_BREAKDOWN_CODES = {"101", "104", "105", "112"}


class L10nPyLibroLine(models.Model):
    _name = "l10n_py.libro.line"
    _description = "Línea de Libro DNIT"
    _order = "id"

    libro_id = fields.Many2one(
        "l10n_py.libro", required=True, ondelete="cascade", index=True
    )
    tipo_registro = fields.Selection(
        related="libro_id.tipo_registro", store=True, string="Tipo de Registro"
    )
    move_id = fields.Many2one("account.move", string="Comprobante de Origen")
    payment_id = fields.Many2one("account.payment", string="Pago de Origen")

    manual_override = fields.Boolean(
        string="Editado manualmente",
        default=False,
        help="Marcado automáticamente quando o usuário edita um campo f_* "
        "de uma linha derivada de account.move: impede que "
        "action_generate_lines sobrescreva o valor na regeneração.",
    )

    state = fields.Selection(
        [("ok", "Ok"), ("erro", "Error")],
        compute="_compute_state",
        store=True,
        default="ok",
    )
    error_message = fields.Text(compute="_compute_state", store=True)

    # Campos comunes
    f_tipo_identificacion = fields.Char(size=2)
    f_numero_identificacion = fields.Char(size=20)
    f_nombre_razon_social = fields.Char(size=250)
    f_tipo_comprobante = fields.Selection(TIPO_COMPROBANTE_SELECTION)
    f_fecha_emision = fields.Date()
    f_periodo_mm_aaaa = fields.Char(size=7)
    f_timbrado = fields.Char(size=8)
    f_numero_comprobante = fields.Char(size=20)
    f_monto_total = fields.Integer()
    f_condicion = fields.Selection([("1", "Contado"), ("2", "Crédito")])
    f_moneda_extranjera = fields.Selection([("S", "Sí"), ("N", "No")], default="N")
    f_imputa_ire = fields.Selection([("S", "Sí"), ("N", "No")], default="N")
    f_imputa_irp_rsp = fields.Selection([("S", "Sí"), ("N", "No")], default="N")
    f_especificar_tipo_documento = fields.Char(size=50)

    # Ventas/Compras
    f_monto_gravado_10 = fields.Integer()
    f_monto_gravado_5 = fields.Integer()
    f_monto_exento = fields.Integer()
    f_imputa_iva = fields.Selection([("S", "Sí"), ("N", "No")], default="N")
    f_comprobante_asociado_numero = fields.Char(size=20)
    f_comprobante_asociado_timbrado = fields.Char(size=8)

    # Compras/Egresos
    f_no_imputa = fields.Selection([("S", "Sí"), ("N", "No")], default="N")

    # Ingresos
    f_monto_gravado = fields.Integer()
    f_monto_no_gravado_exonerado = fields.Integer()

    # Egresos
    f_numero_cuenta = fields.Char(size=30)
    f_banco = fields.Char(size=250)
    f_empleador_ips = fields.Char(size=30)

    @api.constrains(
        "f_monto_total",
        "f_monto_gravado_10",
        "f_monto_gravado_5",
        "f_monto_exento",
        "f_monto_gravado",
        "f_monto_no_gravado_exonerado",
    )
    def _check_montos_no_negativos(self):
        for line in self:
            for field_name in (
                "f_monto_total",
                "f_monto_gravado_10",
                "f_monto_gravado_5",
                "f_monto_exento",
                "f_monto_gravado",
                "f_monto_no_gravado_exonerado",
            ):
                value = line[field_name]
                if value and value < 0:
                    raise ValidationError(
                        self.env._(
                            "Los montos de la línea del libro no pueden ser negativos."
                        )
                    )

    def write(self, vals):
        f_fields = [k for k in vals if k.startswith("f_")]
        if f_fields and not self.env.context.get("l10n_py_libro_regenerating"):
            for line in self:
                if line.move_id:
                    super(L10nPyLibroLine, line).write(dict(vals, manual_override=True))
                else:
                    super(L10nPyLibroLine, line).write(vals)
            return True
        return super().write(vals)

    def action_view_source_document(self):
        self.ensure_one()
        if self.move_id:
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_mode": "form",
                "res_id": self.move_id.id,
            }
        if self.payment_id:
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.payment",
                "view_mode": "form",
                "res_id": self.payment_id.id,
            }
        return False

    def action_restore_generated_values(self):
        for line in self:
            line.with_context(l10n_py_libro_regenerating=True).write(
                {"manual_override": False}
            )
            line.libro_id.action_generate_lines(line_ids=line)

    def action_fill_from_source(self):
        for line in self:
            source = line.move_id or (
                line.payment_id.move_id if line.payment_id else False
            )
            if not source:
                continue
            line.with_context(l10n_py_libro_regenerating=True).write(
                {
                    "f_monto_total": abs(int(round(source.amount_total or 0))),
                    "f_fecha_emision": source.invoice_date or source.date,
                    "f_nombre_razon_social": source.partner_id.name,
                }
            )

    # ============== VALIDATION MATRIX (D4) ==============

    @api.depends(
        "f_tipo_comprobante",
        "f_monto_total",
        "f_monto_gravado_10",
        "f_monto_gravado_5",
        "f_monto_exento",
        "f_monto_gravado",
        "f_monto_no_gravado_exonerado",
        "f_tipo_identificacion",
        "f_numero_identificacion",
        "f_timbrado",
        "f_numero_comprobante",
        "f_periodo_mm_aaaa",
        "f_especificar_tipo_documento",
        "f_comprobante_asociado_numero",
        "f_comprobante_asociado_timbrado",
        "f_imputa_iva",
        "f_imputa_ire",
        "f_imputa_irp_rsp",
        "f_no_imputa",
        "manual_override",
        "move_id.amount_total",
        "move_id.reversed_entry_id",
        "move_id.l10n_py_libro_supplier_timbrado",
        "move_id.l10n_py_libro_supplier_number",
        "move_id.l10n_py_authorization_id",
        "move_id.l10n_py_edi_status",
        "move_id.l10n_py_cdc",
        "move_id.l10n_py_associated_document_ids.cdc",
        "libro_id.tipo_registro",
        "libro_id.company_id.l10n_py_libro_nc_nd_direction",
    )
    def _compute_state(self):
        for line in self:
            problems = []
            tipo = line.tipo_registro
            if tipo in ("ventas", "compras"):
                problems += line._check_state_ventas_compras()
            if tipo == "ingresos":
                problems += line._check_state_ingresos()
            if tipo == "egresos":
                problems += line._check_state_egresos()
            problems += line._check_state_obligacion_imputada()

            line.error_message = "; ".join(problems) if problems else False
            line.state = "erro" if problems else "ok"

    def _check_identificacion_ventas_compras(self, tipo, codigo):
        # D4 - identificación siempre requerida, excepto tipo identificación
        # libre en Compras 101/107 (especificacao:242-246): la exigencia de
        # *presencia* se mantiene, sólo el valor "11" deja de ser forzado.
        if not self.f_tipo_identificacion or not self.f_numero_identificacion:
            return [self.env._("Identificación es obligatoria.")]
        if (
            tipo == "compras"
            and codigo not in COMPRAS_IDENT_LIBRE
            and self.f_tipo_identificacion != "11"
        ):
            return [
                self.env._(
                    "Tipo de identificación debe ser 11 (RUC), excepto para "
                    "los tipos 101/107 (%(codigo)s).",
                    codigo=codigo,
                )
            ]
        return []

    def _check_nombre_numero_ventas_compras(self, tipo, codigo):
        problems = []
        # D4 - nombre/razón social requerido excepto identificación 11/12
        # (Compras, :250-254) o 11/12/15 (Ventas, :148-152).
        nombre_exempt = (
            VENTAS_NOMBRE_EXEMPT_IDENT
            if tipo == "ventas"
            else COMPRAS_NOMBRE_EXEMPT_IDENT
        )
        if (
            self.f_tipo_identificacion not in nombre_exempt
            and not self.f_nombre_razon_social
        ):
            problems.append(self.env._("Nombre/razón social es obligatorio."))

        # D4 - número de comprobante requerido excepto 112/106 (Ventas,
        # :164-167) o 112/106/107 (Compras, :268-274).
        numero_exempt = (
            VENTAS_NUMERO_EXEMPT if tipo == "ventas" else COMPRAS_NUMERO_EXEMPT
        )
        if codigo not in numero_exempt and not self.f_numero_comprobante:
            problems.append(self.env._("Número de comprobante es obligatorio."))

        # D4 - timbrado fijo "0" obligatorio para Compras 107, :263-267.
        if tipo == "compras" and codigo == "107" and self.f_timbrado != "0":
            problems.append(self.env._("El timbrado debe ser '0' para el tipo 107."))
        return problems

    def _check_fecha_ventas_compras(self):
        # D4 - fecha de emisión no anterior a 01/01/2021, excepto condición
        # de crédito (Ventas :156-160, Compras :259-262).
        if (
            self.f_fecha_emision
            and self.f_fecha_emision < FECHA_MINIMA_DNIT
            and self.f_condicion != "2"
        ):
            return [
                self.env._("La fecha de emisión no puede ser anterior al 01/01/2021.")
            ]
        return []

    def _check_montos_ventas_compras(self, tipo, codigo):
        problems = []
        # D1/D4 - zeramento de baldes 9/10/11 para Compras 101/104/105/112:
        # exento del check de divergencia contra el total (correção OBJ-02).
        if tipo == "compras" and codigo in ZERO_BREAKDOWN_CODES:
            if any(
                [self.f_monto_gravado_10, self.f_monto_gravado_5, self.f_monto_exento]
            ):
                problems.append(
                    self.env._(
                        "Para el tipo %(codigo)s los montos gravados "
                        "10/5/exento deben estar en cero.",
                        codigo=codigo,
                    )
                )
        else:
            problems += self._check_monto_total_vs_move()
        if not self.f_monto_total or self.f_monto_total <= 0:
            problems.append(self.env._("El monto total debe ser mayor a 0."))
        return problems

    def _check_monto_total_vs_move(self):
        # O1 - caso general: comparar tanto la suma de los baldes como
        # f_monto_total contra move_id.amount_total convertido a PYG por el
        # mismo camino usado en la generación (design D1), tolerancia de 1
        # guaraní. Sin move_id (línea manual), sólo se verifica la
        # consistencia interna suma-de-baldes == f_monto_total.
        problems = []
        suma = (
            (self.f_monto_gravado_10 or 0)
            + (self.f_monto_gravado_5 or 0)
            + (self.f_monto_exento or 0)
        )
        if self.move_id:
            target = self.libro_id._get_total_in_pyg(self.move_id)
            if abs(suma - target) > 1:
                problems.append(
                    self.env._(
                        "La suma de los montos gravados (10%%/5%%/exento) "
                        "no coincide con el monto total del comprobante "
                        "de origen."
                    )
                )
            if abs((self.f_monto_total or 0) - target) > 1:
                problems.append(
                    self.env._(
                        "El monto total no coincide con el monto total "
                        "del comprobante de origen."
                    )
                )
        elif abs(suma - (self.f_monto_total or 0)) > 1:
            problems.append(
                self.env._(
                    "El monto total no coincide con la suma de los "
                    "montos gravados (10%%/5%%/exento)."
                )
            )
        return problems

    def _check_asociado_nc_nd(self, codigo):
        # D4 - campos 18/19 (comprobante asociado) requeridos sólo p/110,111
        # (Ventas :214-223, Compras :342-354); si hay move_id, además se
        # verifica que la resolución actual del documento original (D3,
        # reversed_entry_id/debit_origin_id/l10n_py.associated.document/cdc)
        # no diverja de los valores ya guardados en la línea (D2 item 2).
        if codigo not in ("110", "111"):
            return []
        if not (
            self.f_comprobante_asociado_numero and self.f_comprobante_asociado_timbrado
        ):
            return [
                self.env._(
                    "Número y timbrado del comprobante asociado son "
                    "obligatorios para Notas de Crédito/Débito."
                )
            ]
        if not self.move_id:
            return []
        current_original = self.libro_id._get_associated_move(self.move_id)
        if not current_original:
            return []
        if current_original.move_type in ("out_invoice", "out_refund"):
            current_numero = current_original.l10n_py_full_invoice_number or False
            current_timbrado = current_original.l10n_py_authorization_id.name or False
        else:
            current_numero = current_original.l10n_py_libro_supplier_number or False
            current_timbrado = current_original.l10n_py_libro_supplier_timbrado or False
        if (
            current_numero != self.f_comprobante_asociado_numero
            or current_timbrado != self.f_comprobante_asociado_timbrado
        ):
            return [
                self.env._(
                    "El comprobante asociado difiere del documento de "
                    "origen actual; regenere la línea."
                )
            ]
        return []

    def _check_documento_origen_vivo(self, tipo):
        problems = []
        # D2 - timbrado/número de terceiro (Compras, documento in_invoice/
        # in_refund) leídos en vivo desde move_id, no desde el snapshot de
        # la línea: garantiza que el state se marca erro si el documento de
        # origen pierde estos datos después de la generación (correção O2).
        if (
            tipo == "compras"
            and self.move_id
            and self.move_id.move_type in ("in_invoice", "in_refund")
            and not (
                self.move_id.l10n_py_libro_supplier_timbrado
                and self.move_id.l10n_py_libro_supplier_number
            )
        ):
            problems.append(
                self.env._("Timbrado/número del proveedor ausente o inconsistente.")
            )

        # D2 - "Onde entra": timbrado propio (autorización) obligatorio para
        # documentos propios de Ventas; si se retira después de generado, el
        # state se marca erro (correção O2).
        if (
            tipo == "ventas"
            and self.move_id
            and self.move_id.move_type in ("out_invoice", "out_refund")
            and not self.move_id.l10n_py_authorization_id
        ):
            problems.append(
                self.env._("Autorización (timbrado) del comprobante propio ausente.")
            )
        return problems

    def _check_state_ventas_compras(self):
        self.ensure_one()
        tipo = self.tipo_registro
        codigo = self.f_tipo_comprobante
        problems = []
        problems += self._check_identificacion_ventas_compras(tipo, codigo)
        problems += self._check_nombre_numero_ventas_compras(tipo, codigo)
        problems += self._check_fecha_ventas_compras()
        problems += self._check_montos_ventas_compras(tipo, codigo)
        problems += self._check_asociado_nc_nd(codigo)
        problems += self._check_documento_origen_vivo(tipo)
        return problems

    def _check_state_ingresos(self):
        self.ensure_one()
        problems = []
        codigo = self.f_tipo_comprobante
        if codigo != "203":
            suma = (self.f_monto_gravado or 0) + (
                self.f_monto_no_gravado_exonerado or 0
            )
            if abs(suma - (self.f_monto_total or 0)) > 1:
                problems.append(
                    self.env._(
                        "El monto total no coincide con la suma de monto "
                        "gravado + no gravado/exonerado."
                    )
                )
        if not self.f_monto_total or self.f_monto_total <= 0:
            problems.append(self.env._("El monto total debe ser mayor a 0."))

        # D4 - campo 3 (fecha/período), :370-377: dd/mm/aaaa excepto 208
        # (mm/aaaa); no anterior a 01/01/2021, sin excepción de crédito.
        if codigo == "208":
            if not self.f_periodo_mm_aaaa or len(self.f_periodo_mm_aaaa or "") != 7:
                problems.append(
                    self.env._("El período mm/aaaa es obligatorio para el tipo 208.")
                )
        elif self.f_fecha_emision and self.f_fecha_emision < FECHA_MINIMA_DNIT:
            problems.append(
                self.env._("La fecha de emisión no puede ser anterior al 01/01/2021.")
            )

        # D4 - campo 4 (número), :378-380: no requerido p/208.
        if codigo != "208" and not self.f_numero_comprobante:
            problems.append(self.env._("Número de comprobante es obligatorio."))

        # D4 - campo 5 (tipo identificación pagador), :383-389: p/210 sólo
        # 11/12/13; p/208 fijo 11.
        if (
            codigo == "210"
            and self.f_tipo_identificacion not in INGRESOS_IDENT_210_ALLOWED
        ):
            problems.append(
                self.env._(
                    "Tipo de identificación debe ser 11, 12 o 13 para el tipo 210."
                )
            )
        elif (
            codigo in INGRESOS_IDENT_FIXED
            and self.f_tipo_identificacion != INGRESOS_IDENT_FIXED[codigo]
        ):
            problems.append(
                self.env._(
                    "Tipo de identificación debe ser %(esperado)s para el "
                    "tipo %(codigo)s.",
                    esperado=INGRESOS_IDENT_FIXED[codigo],
                    codigo=codigo,
                )
            )

        # D4 - campo 7 (nombre), :391-393: requerido excepto 11,12.
        if (
            self.f_tipo_identificacion not in ("11", "12")
            and not self.f_nombre_razon_social
        ):
            problems.append(self.env._("Nombre/razón social es obligatorio."))

        if codigo == "210" and not self.f_especificar_tipo_documento:
            problems.append(
                self.env._("Especificar Tipo de Documento es obligatorio (210).")
            )

        # D4 - campos 14/15 (comprobante asociado), :424-433: no requeridos
        # excepto 203.
        if codigo == "203" and not (
            self.f_comprobante_asociado_numero and self.f_comprobante_asociado_timbrado
        ):
            problems.append(
                self.env._(
                    "Número y timbrado del comprobante asociado son "
                    "obligatorios para el tipo 203."
                )
            )
        return problems

    def _check_state_egresos(self):
        self.ensure_one()
        problems = []
        codigo = self.f_tipo_comprobante
        if not self.f_monto_total or self.f_monto_total <= 0:
            problems.append(self.env._("El monto total debe ser mayor a 0."))
        if codigo != "207" and self.f_imputa_iva == "S":
            problems.append(
                self.env._("Imputa al IVA solo puede ser 'S' para el tipo 207.")
            )

        # D4 - campo 3 (fecha/período), :452-460: dd/mm/aaaa excepto 208 y
        # 206 (mm/aaaa); no anterior a 01/01/2021, sin excepción de crédito.
        if codigo in ("208", "206"):
            if not self.f_periodo_mm_aaaa or len(self.f_periodo_mm_aaaa or "") != 7:
                problems.append(
                    self.env._(
                        "El período mm/aaaa es obligatorio para %(codigo)s.",
                        codigo=codigo,
                    )
                )
        elif self.f_fecha_emision and self.f_fecha_emision < FECHA_MINIMA_DNIT:
            problems.append(
                self.env._("La fecha de emisión no puede ser anterior al 01/01/2021.")
            )

        # D4 - campo 4 (número/transacción), :461-467: no requerido p/
        # 205,206,207,208.
        if codigo not in ("205", "206", "207", "208") and not self.f_numero_comprobante:
            problems.append(self.env._("Número de comprobante es obligatorio."))

        # D4 - campos 5/6 (tipo/número de identificación), :468-493: no
        # requeridos p/206,207,211; fijo 11 p/204,205; fijo 17 p/202.
        if codigo in EGRESOS_IDENT_EXEMPT:
            pass
        elif not self.f_tipo_identificacion or not self.f_numero_identificacion:
            problems.append(self.env._("Identificación es obligatoria."))
        elif (
            codigo in EGRESOS_IDENT_FIXED
            and self.f_tipo_identificacion != EGRESOS_IDENT_FIXED[codigo]
        ):
            problems.append(
                self.env._(
                    "Tipo de identificación debe ser %(esperado)s para el "
                    "tipo %(codigo)s.",
                    esperado=EGRESOS_IDENT_FIXED[codigo],
                    codigo=codigo,
                )
            )

        # D4 - campo 7 (nombre), :494-498: requerido excepto 11,12 o tipo 206.
        if (
            codigo != "206"
            and self.f_tipo_identificacion not in EGRESOS_NOMBRE_EXEMPT_IDENT
            and not self.f_nombre_razon_social
        ):
            problems.append(self.env._("Nombre/razón social es obligatorio."))

        # D4 - campos 13/14 (nº cuenta/banco), :521-530: no requeridos
        # excepto 207,211.
        if codigo in ("207", "211") and not (self.f_numero_cuenta and self.f_banco):
            problems.append(
                self.env._(
                    "Número de cuenta y banco son obligatorios para %(codigo)s.",
                    codigo=codigo,
                )
            )

        # D4 - campo 15 (empleador IPS), :531-533: no requerido excepto 206.
        if codigo == "206" and not self.f_empleador_ips:
            problems.append(
                self.env._("Empleador IPS es obligatorio para el tipo 206.")
            )

        # D4 - campo 16 (especificar tipo documento), :534-536: requerido
        # p/209.
        if codigo == "209" and not self.f_especificar_tipo_documento:
            problems.append(
                self.env._("Especificar Tipo de Documento es obligatorio (209).")
            )

        # D4 - campos 17/18 (comprobante asociado), :537-546: no requeridos
        # excepto 201.
        if codigo == "201" and not (
            self.f_comprobante_asociado_numero and self.f_comprobante_asociado_timbrado
        ):
            problems.append(
                self.env._(
                    "Número y timbrado del comprobante asociado son "
                    "obligatorios para el tipo 201."
                )
            )
        return problems

    def _check_state_obligacion_imputada(self):
        self.ensure_one()
        if self.tipo_registro in ("ventas", "compras", "egresos"):
            obligaciones = [self.f_imputa_iva, self.f_imputa_ire, self.f_imputa_irp_rsp]
        else:
            obligaciones = [self.f_imputa_ire, self.f_imputa_irp_rsp]
        if any(value == "S" for value in obligaciones):
            return []
        return [
            self.env._(
                "Debe marcarse al menos una obligación imputada "
                "(IVA/IRE/IRP-RSP según el registro)."
            )
        ]
