# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.depends(
        "price_subtotal", "product_uom_qty", "purchase_price", "agent_ids.amount"
    )
    def _compute_margin(self):
        for line in self:
            line.margin = (
                line.price_subtotal
                - (line.purchase_price * line.product_uom_qty)
                - sum(line.mapped("agent_ids.amount"))
            )
            line.margin_percent = (
                line.price_subtotal and line.margin / line.price_subtotal
            )
