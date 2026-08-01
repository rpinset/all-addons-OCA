# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Technical field to display the route area in the sale order form
    delivery_type = fields.Selection(related="carrier_id.delivery_type")

    @api.depends("carrier_id")
    def _compute_route_area_id(self):
        res = super()._compute_route_area_id()
        # Ensure that the route area is cleared
        # when changing to a non-route planning carrier
        sales = self.filtered(lambda x: x.carrier_id.delivery_type != "route_planning")
        sales.route_area_id = False
        return res
