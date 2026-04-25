# Copyright 2014-2020 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method_line_id = fields.Many2one(
        comodel_name="account.payment.method.line",
        compute="_compute_payment_method_line_id",
        string="Payment Method",
        store=True,
        readonly=False,
        precompute=True,
        check_company=True,
        tracking=2,
        domain="[('payment_type', '=', 'inbound'), ('company_id', '=', company_id), "
        "('selectable', '=', True)]",
    )

    @api.depends("partner_id")
    def _compute_payment_method_line_id(self):
        for order in self:
            payment_method_line = False
            if order.partner_id and order.company_id:
                payment_method_line = order.with_company(
                    order.company_id
                ).partner_id.property_inbound_payment_method_line_id
            order.payment_method_line_id = payment_method_line

    def _get_payment_method_line_vals(self, vals):
        if self.payment_method_line_id:
            vals["preferred_payment_method_line_id"] = self.payment_method_line_id.id
            if (
                self.payment_method_line_id.bank_account_link == "fixed"
                and self.payment_method_line_id.payment_method_id.code == "manual"
            ):
                vals["partner_bank_id"] = (
                    self.payment_method_line_id.journal_id.bank_account_id.id
                )

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        self._get_payment_method_line_vals(vals)
        return vals

    def _get_invoice_grouping_keys(self) -> list:
        """
        When several sale orders are generating invoices,
        we want to add the payment method in grouping criteria.
        """
        keys = super()._get_invoice_grouping_keys()
        if "preferred_payment_method_line_id" not in keys:
            keys.append("preferred_payment_method_line_id")
        return keys
