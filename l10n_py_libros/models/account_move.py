# l10n_py_libros/models/account_move.py

import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

SUPPLIER_NUMBER_RE = re.compile(r"^\d{3}-\d{3}-\d{7}$")


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_py_libro_supplier_timbrado = fields.Char(
        string="Timbrado del Proveedor",
        size=8,
        help="Número de timbrado del proveedor (factura de compra en papel)",
    )

    l10n_py_libro_supplier_number = fields.Char(
        string="Número del Comprobante del Proveedor",
        help="Formato EEE-PPP-NNNNNNN",
    )

    l10n_py_libro_electronic = fields.Boolean(
        string="Comprobante electrónico",
        default=False,
        help=(
            "Marca que este comprobante de compra ya es electrónico y "
            "pre-cargado por el Marangatu: la línea correspondiente es "
            "excluída del Registro de Compras generado por este módulo."
        ),
    )

    l10n_py_condicion_venta = fields.Selection(
        selection=[("1", "Contado"), ("2", "Crédito")],
        compute="_compute_l10n_py_condicion_venta",
        store=True,
        string="Condición de Venta (DNIT)",
    )

    @api.constrains("l10n_py_libro_supplier_timbrado")
    def _check_l10n_py_libro_supplier_timbrado(self):
        for move in self:
            value = move.l10n_py_libro_supplier_timbrado
            if value and not (value.isdigit() and len(value) == 8):
                raise ValidationError(
                    self.env._(
                        "El timbrado del proveedor debe tener exactamente "
                        "8 dígitos numéricos (%(value)s).",
                        value=value,
                    )
                )

    @api.constrains("l10n_py_libro_supplier_number")
    def _check_l10n_py_libro_supplier_number(self):
        for move in self:
            value = move.l10n_py_libro_supplier_number
            if value and not SUPPLIER_NUMBER_RE.match(value):
                raise ValidationError(
                    self.env._(
                        "El número de comprobante del proveedor debe seguir "
                        "el formato EEE-PPP-NNNNNNN (%(value)s).",
                        value=value,
                    )
                )

    def _l10n_py_libro_term_is_immediate(self):
        self.ensure_one()
        term = self.invoice_payment_term_id
        if not term or not term.line_ids:
            return True
        for line in term.line_ids:
            days_field = "nb_days" if "nb_days" in line._fields else "days"
            if getattr(line, days_field, 0) != 0:
                return False
        return True

    @api.depends("invoice_payment_term_id", "invoice_payment_term_id.line_ids")
    def _compute_l10n_py_condicion_venta(self):
        for move in self:
            move.l10n_py_condicion_venta = (
                "1" if move._l10n_py_libro_term_is_immediate() else "2"
            )

    # ============== COPIA DO FLAG "COMPROBANTE ELECTRÓNICO" DO PARCEIRO ==============

    def _l10n_py_libro_electronic_should_copy(self, new_value):
        """True quando o valor atual ainda não foi editado manualmente."""
        self.ensure_one()
        current = self.l10n_py_libro_electronic
        origin_value = self._origin.l10n_py_libro_electronic if self._origin else False
        return current in (False, origin_value)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                vals.get("move_type") in ("in_invoice", "in_refund")
                and "l10n_py_libro_electronic" not in vals
                and vals.get("partner_id")
            ):
                company_id = vals.get("company_id") or self.env.company.id
                partner = self.env["res.partner"].browse(vals["partner_id"])
                vals["l10n_py_libro_electronic"] = partner.with_company(
                    company_id
                ).l10n_py_libro_electronic
        return super().create(vals_list)

    def write(self, vals):
        if (
            "partner_id" in vals
            and "l10n_py_libro_electronic" not in vals
            and vals.get("partner_id")
        ):
            for move in self:
                if (
                    move.move_type in ("in_invoice", "in_refund")
                    and move.state == "draft"
                ):
                    if move._l10n_py_libro_electronic_should_copy(None):
                        partner = self.env["res.partner"].browse(vals["partner_id"])
                        new_value = partner.with_company(
                            move.company_id.id
                        ).l10n_py_libro_electronic
                        super(AccountMove, move).write(
                            {"l10n_py_libro_electronic": new_value}
                        )
        return super().write(vals)

    @api.onchange("partner_id")
    def _onchange_partner_id_l10n_py_libro_electronic(self):
        if self.move_type in ("in_invoice", "in_refund") and self.partner_id:
            if self._l10n_py_libro_electronic_should_copy(None):
                self.l10n_py_libro_electronic = self.partner_id.with_company(
                    self.company_id.id
                ).l10n_py_libro_electronic
