# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLineAgent(models.Model):
    _inherit = "sale.order.line.agent"

    @api.depends(
        "object_id.order_id.partner_id",
    )
    def _compute_amount(self):
        res = None
        for line in self:
            res = super(
                SaleOrderLineAgent,
                line.with_context(
                    sale_commission_customer=line.object_id.order_id.partner_id
                ),
            )._compute_amount()
        return res
