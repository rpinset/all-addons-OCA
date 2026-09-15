# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    route_area_id = fields.Many2one(
        compute="_compute_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("carrier_id")
    def _compute_route_area_id(self):
        for item in self:
            if item.delivery_type != "route_planning":
                # Set route_area_id empty so that the data is consistent
                # with carrier_id
                item.route_area_id = False
