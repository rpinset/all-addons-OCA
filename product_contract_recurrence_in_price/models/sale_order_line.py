# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        """
        This is the base method for all line amounts computations.
        For 'include_recurrence_in_price' lines, we multiply the quantity by
        the number of times the line will be invoiced.
        """
        self.ensure_one()
        if self.include_recurrence_in_price:
            return self.env["account.tax"]._prepare_base_line_for_taxes_computation(
                self,
                **{
                    "tax_ids": self.tax_id,
                    "quantity": self.product_uom_qty * self.recurring_invoicing_number,
                    "partner_id": self.order_id.partner_id,
                    "currency_id": self.order_id.currency_id
                    or self.order_id.company_id.currency_id,
                    "rate": self.order_id.currency_rate,
                    **kwargs,
                },
            )
        return super()._prepare_base_line_for_taxes_computation(**kwargs)

    @api.depends("recurring_invoicing_number", "include_recurrence_in_price")
    def _compute_amount(self):
        return super()._compute_amount()
