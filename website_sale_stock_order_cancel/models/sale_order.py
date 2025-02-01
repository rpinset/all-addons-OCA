# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("commitment_date", "expected_date", "state", "picking_ids.state")
    def _compute_can_cancel(self):
        res = super()._compute_can_cancel()
        for order in self:
            if order.picking_ids.filtered(lambda p: p.state == "done"):
                order.can_cancel = False
        return res
