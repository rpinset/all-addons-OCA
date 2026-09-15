# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Rma(models.Model):
    _inherit = "rma"

    reception_carrier_delivery_type = fields.Selection(
        related="reception_carrier_id.delivery_type",
        string="Reception carrier delivery type",
    )
    carrier_delivery_type = fields.Selection(
        related="carrier_id.delivery_type", string="Carrier delivery type"
    )
    reception_route_area_id = fields.Many2one(
        compute="_compute_reception_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("carrier_id")
    def _compute_route_area_id(self):
        # Overwrite the compute so that the data is consistent based on carrier_id
        _self = self.filtered(lambda x: x.carrier_delivery_type != "route_planning")
        _self.route_area_id = False
        self -= _self
        return super()._compute_route_area_id()

    @api.depends("reception_carrier_id")
    def _compute_reception_route_area_id(self):
        for item in self:
            if item.reception_carrier_delivery_type != "route_planning":
                # Set reception_route_area_id empty so that the data is consistent
                # with reception_carrier_id
                item.reception_route_area_id = False
