# l10n_py_account/models/account_move.py

from num2words import num2words

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.constrains("state", "l10n_latam_document_type_id")
    def _check_l10n_latam_documents(self):
        """Pular validação de documento LATAM durante instalação de módulos.

        As invoices demo do account padrão são postadas pelo try_loading sem
        document number, causando ValidationError. Isso é comportamento
        esperado em todas as localizações LATAM — pulamos durante instalação.
        """
        if not self.env.registry.ready:
            return
        return super()._check_l10n_latam_documents()

    # ============== CAMPOS CONTABILIDAD PARAGUAY ==============

    l10n_py_authorization_id = fields.Many2one(
        "account.authorization",
        string="Timbrado",
        domain=(
            "[('company_id', '=', company_id), "
            "('active', '=', True), "
            "('state', '!=', 'expired')]"
        ),
        help="Timbrado utilizado para esta factura",
    )

    l10n_py_invoice_number = fields.Integer(
        string="Número de Factura",
        help="Número de factura según timbrado autorizado",
    )

    l10n_py_full_invoice_number = fields.Char(
        string="Número Completo",
        compute="_compute_l10n_py_full_invoice_number",
        store=True,
        help="Número completo de factura (formato: 001-001-0000001)",
    )

    # ============== CAMPOS IVA BREAKDOWN (SIFEN) ==============

    l10n_py_amount_subtotal_10 = fields.Monetary(
        string="Total Gravado 10% (F005)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Subtotal gravado 10% — valor con impuesto incluido (SIFEN F005)",
    )

    l10n_py_amount_iva_10 = fields.Monetary(
        string="Liquidación IVA 10% (F016)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Liquidación IVA 10% (SIFEN F016)",
    )

    l10n_py_amount_subtotal_5 = fields.Monetary(
        string="Total Gravado 5% (F004)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Subtotal gravado 5% — valor con impuesto incluido (SIFEN F004)",
    )

    l10n_py_amount_iva_5 = fields.Monetary(
        string="Liquidación IVA 5% (F015)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Liquidación IVA 5% (SIFEN F015)",
    )

    l10n_py_amount_exempt = fields.Monetary(
        string="Total Exento (F003)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Subtotal exento/no gravado (SIFEN F003)",
    )

    l10n_py_amount_iva_total = fields.Monetary(
        string="Total IVA (F014)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Total liquidación IVA (SIFEN F014)",
    )

    l10n_py_base_10 = fields.Monetary(
        string="Base Gravada 10% (F019)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Base gravada neta 10% sin IVA (SIFEN F019)",
    )

    l10n_py_base_5 = fields.Monetary(
        string="Base Gravada 5% (F018)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Base gravada neta 5% sin IVA (SIFEN F018)",
    )

    l10n_py_base_total = fields.Monetary(
        string="Total Base Gravada (F020)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Total base gravada (SIFEN F020 = F018 + F019)",
    )

    l10n_py_total_operation = fields.Monetary(
        string="Total Operación (F008)",
        compute="_compute_l10n_py_iva",
        store=True,
        currency_field="currency_id",
        help="Total de la operación (SIFEN F008 = F003 + F004 + F005)",
    )

    # ============== CAMPOS TIPO DE CAMBIO PYG ==============

    l10n_py_exchange_rate = fields.Float(
        string="Tipo de Cambio",
        digits=(16, 4),
        help="Tipo de cambio a guaraníes (PYG) para facturación en moneda extranjera",
    )

    l10n_py_amount_total_pyg = fields.Monetary(
        string="Total en Guaraníes (F023)",
        compute="_compute_l10n_py_total_pyg",
        store=True,
        currency_field="currency_id",
        help="Total de la operación en guaraníes (SIFEN F023)",
    )

    l10n_py_amount_total_words = fields.Char(
        string="Total en Letras",
        compute="_compute_l10n_py_amount_total_words",
    )

    _sql_constraints = [
        (
            "l10n_py_invoice_unique",
            "unique(l10n_py_authorization_id, l10n_py_invoice_number)",
            "El número de factura debe ser único por timbrado.",
        ),
    ]

    # ============== ACTION METHODS ==============

    def action_post(self):
        """Override para asignar numeración secuencial al confirmar"""
        for move in self:
            if (
                move.move_type in ("out_invoice", "out_refund")
                and move.company_id.country_id.code == "PY"
                and move.journal_id.l10n_latam_use_documents
                and move.l10n_latam_document_type_id
            ):
                if not move.l10n_py_authorization_id:
                    if not self.env.registry.ready:
                        # Pular durante instalação/demo (invoices genéricas
                        # criadas pelo account.chart.template.try_loading)
                        continue
                    raise UserError(
                        _(
                            "Debe seleccionar un timbrado para confirmar "
                            "una factura de venta."
                        )
                    )
                if not move.l10n_py_invoice_number:
                    auth = move.l10n_py_authorization_id
                    auth.check_validity()
                    # Flush pending writes so the SQL query sees all data
                    self.env["account.move"].flush_model(["l10n_py_invoice_number"])
                    # Query next number directly to avoid ORM cache issues
                    self.env.cr.execute(
                        """
                        SELECT COALESCE(MAX(l10n_py_invoice_number), 0)
                        FROM account_move
                        WHERE l10n_py_authorization_id = %s
                          AND l10n_py_invoice_number > 0
                          AND move_type IN ('out_invoice', 'out_refund')
                        """,
                        (auth.id,),
                    )
                    max_num = self.env.cr.fetchone()[0]
                    next_num = max_num + 1 if max_num else auth.invoice_number_from
                    if next_num > auth.invoice_number_to:
                        raise UserError(
                            _(
                                "La faja de numeración está agotada "
                                "para el timbrado %(timbrado)s.",
                                timbrado=auth.name,
                            )
                        )
                    auth.check_number_available(next_num, exclude_move_id=move.id)
                    move.l10n_py_invoice_number = next_num
        return super().action_post()

    # ============== COMPUTE METHODS ==============

    @api.depends(
        "l10n_py_authorization_id",
        "l10n_py_invoice_number",
    )
    def _compute_l10n_py_full_invoice_number(self):
        """Calcular número completo de factura (formato: 001-001-0000001)"""
        for move in self:
            if move.l10n_py_authorization_id and move.l10n_py_invoice_number:
                auth = move.l10n_py_authorization_id
                number_str = str(move.l10n_py_invoice_number).zfill(7)
                move.l10n_py_full_invoice_number = (
                    f"{auth.establishment}-" f"{auth.expedition_point}-" f"{number_str}"
                )
            else:
                move.l10n_py_full_invoice_number = False

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "invoice_line_ids.price_total",
        "invoice_line_ids.tax_ids",
    )
    def _compute_l10n_py_iva(self):
        """Calcular desglose de IVA según fórmula SIFEN v150.

        Fórmula SIFEN: base = price_total / (1 + tasa/100)
                        iva  = price_total - base
        """
        for move in self:
            subtotal_10 = iva_10 = base_10 = 0.0
            subtotal_5 = iva_5 = base_5 = 0.0
            exempt = 0.0

            for line in move.invoice_line_ids.filtered(
                lambda line: line.display_type == "product"
            ):
                tax_rate = 0
                for tax in line.tax_ids:
                    if tax.amount == 10:
                        tax_rate = 10
                    elif tax.amount == 5:
                        tax_rate = 5

                if tax_rate == 10:
                    base = line.price_total / 1.1
                    subtotal_10 += line.price_total  # F005
                    iva_10 += line.price_total - base  # F016
                    base_10 += base  # F019
                elif tax_rate == 5:
                    base = line.price_total / 1.05
                    subtotal_5 += line.price_total  # F004
                    iva_5 += line.price_total - base  # F015
                    base_5 += base  # F018
                else:
                    exempt += line.price_subtotal  # F003

            move.l10n_py_amount_subtotal_10 = subtotal_10
            move.l10n_py_amount_iva_10 = iva_10
            move.l10n_py_base_10 = base_10
            move.l10n_py_amount_subtotal_5 = subtotal_5
            move.l10n_py_amount_iva_5 = iva_5
            move.l10n_py_base_5 = base_5
            move.l10n_py_amount_exempt = exempt
            move.l10n_py_amount_iva_total = iva_10 + iva_5  # F014
            move.l10n_py_base_total = base_10 + base_5  # F020
            move.l10n_py_total_operation = exempt + subtotal_5 + subtotal_10  # F008

    @api.depends("amount_total", "l10n_py_exchange_rate")
    def _compute_l10n_py_total_pyg(self):
        """Calcular total en guaraníes (F023) para facturas en moneda extranjera"""
        for move in self:
            if move.l10n_py_exchange_rate and move.l10n_py_exchange_rate > 0:
                move.l10n_py_amount_total_pyg = (
                    move.amount_total * move.l10n_py_exchange_rate
                )
            else:
                move.l10n_py_amount_total_pyg = 0.0

    @api.depends("amount_total", "currency_id")
    def _compute_l10n_py_amount_total_words(self):
        """Convertir total a letras en español"""
        # Mapa de nombres en español para monedas comunes en Paraguay
        _CURRENCY_NAMES_ES = {
            "PYG": "guaraníes",
            "USD": "dólares americanos",
            "BRL": "reales",
            "EUR": "euros",
            "ARS": "pesos argentinos",
        }
        for move in self:
            if move.amount_total:
                currency_code = move.currency_id.name or ""
                currency_name = _CURRENCY_NAMES_ES.get(
                    currency_code,
                    move.currency_id.currency_unit_label or "guaraníes",
                )
                amount_words = num2words(int(move.amount_total), lang="es")
                move.l10n_py_amount_total_words = (
                    f"{amount_words} {currency_name}".capitalize()
                )
            else:
                move.l10n_py_amount_total_words = False

    # ============== CONSTRAINT METHODS ==============

    @api.constrains("l10n_py_authorization_id", "l10n_py_invoice_number")
    def _check_authorization_number(self):
        """Validar que el número de factura esté dentro del rango autorizado"""
        for move in self:
            if move.l10n_py_authorization_id and move.l10n_py_invoice_number:
                move.l10n_py_authorization_id.check_number_available(
                    move.l10n_py_invoice_number,
                    exclude_move_id=move.id,
                )

    @api.constrains("l10n_py_authorization_id")
    def _check_authorization_validity(self):
        """Validar que el timbrado esté vigente"""
        for move in self:
            if move.l10n_py_authorization_id:
                move.l10n_py_authorization_id.check_validity()

    # ============== ONCHANGE METHODS ==============

    @api.onchange("l10n_py_authorization_id")
    def _onchange_authorization_id(self):
        """Limpiar número al cambiar timbrado — se asigna en action_post"""
        if self.l10n_py_authorization_id:
            self.l10n_py_invoice_number = 0
