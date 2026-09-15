# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RmaChooseDeliveryCarrier(models.TransientModel):
    _inherit = "rma.choose.delivery.carrier"

    delivery_type = fields.Selection(related="carrier_id.delivery_type")
    route_area_id = fields.Many2one(
        comodel_name="route.area",
        string="Route area",
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

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        rma_id = self.env.context.get("active_id")
        rma = self.env["rma"].browse(rma_id)
        if rma:
            carrier_type = "reception" if rma.state == "confirmed" else "delivery"
            route_area = (
                rma.reception_route_area_id
                if carrier_type == "reception"
                else rma.route_area_id
            )
            res.update(route_area_id=route_area.id)
        return res

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        f_name = (
            "reception_route_area_id"
            if self.carrier_type == "reception"
            else "route_area_id"
        )
        vals[f_name] = self.route_area_id.id
        return vals
