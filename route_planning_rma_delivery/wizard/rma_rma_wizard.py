# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RmaRmaWizard(models.TransientModel):
    _inherit = "rma.rma.wizard"

    delivery_type = fields.Selection(related="reception_carrier_id.delivery_type")
    reception_route_area_id = fields.Many2one(
        compute="_compute_reception_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("reception_carrier_id")
    def _compute_reception_route_area_id(self):
        for item in self:
            if item.delivery_type != "route_planning":
                # Set reception_route_area_id empty so that the data is consistent
                # with reception_carrier_id
                item.reception_route_area_id = False
