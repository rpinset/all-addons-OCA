# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    client_order_ref = fields.Char(
        "Customer Order Ref",
        compute="_compute_client_order_ref",
        store=True,
        readonly=False,
    )

    @api.depends("order_id.client_order_ref")
    def _compute_client_order_ref(self):
        for rec in self:
            rec.client_order_ref = rec.order_id.client_order_ref

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res["client_order_ref"] = self.client_order_ref
        return res
