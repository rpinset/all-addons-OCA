# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        route_area = self.wizard_id.reception_route_area_id
        if route_area:
            vals["reception_route_area_id"] = route_area.id
            vals["location_id"] = route_area.location_id.id
        return vals


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    reception_route_area_id = fields.Many2one(
        comodel_name="route.area",
        string="Reception route area",
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if "picking_id" in res and "reception_route_area_id" in fields:
            picking = self.env["stock.picking"].browse(res.get("picking_id"))
            res["reception_route_area_id"] = picking.route_area_id.id
        return res
