# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Rma(models.Model):
    _inherit = "rma"

    reception_route_area_id = fields.Many2one(
        comodel_name="route.area",
        string="Reception route area",
        inverse="_inverse_reception_route_area_id",
    )
    route_area_id = fields.Many2one(
        comodel_name="route.area",
        string="Delivery route area",
        compute="_compute_route_area_id",
        inverse="_inverse_route_area_id",
        store=True,
        readonly=False,
    )

    def _compute_warehouse_id(self):
        """Support for non-RMA locations."""
        res = super()._compute_warehouse_id()
        for record in self.filtered(lambda x: x.location_id and not x.warehouse_id):
            record.warehouse_id = record.location_id.warehouse_id
        return res

    @api.depends("partner_shipping_id", "company_id")
    def _compute_route_area_id(self):
        for rma in self:
            company = rma.company_id or self.env.company
            partner = rma.partner_shipping_id.with_company(company)
            rma.route_area_id = partner.route_area_id

    def _inverse_reception_route_area_id(self):
        for item in self.filtered(lambda x: x.reception_move_id):
            item.onchange_reception_route_area_id()
            item.reception_move_id.picking_id.filtered(
                lambda p: p.state not in ("done", "cancel")
            ).write({"route_area_id": item.reception_route_area_id.id})

    def _inverse_route_area_id(self):
        for item in self.filtered(lambda x: x.delivery_move_ids):
            item.delivery_move_ids.picking_id.filtered(
                lambda p: p.state not in ("done", "cancel")
            ).write({"route_area_id": item.route_area_id.id})

    @api.onchange("reception_route_area_id")
    def onchange_reception_route_area_id(self):
        if self.reception_route_area_id:
            self.location_id = self.reception_route_area_id.location_id
        else:
            self.location_id = self.move_id.picking_type_id.warehouse_id.rma_loc_id

    def _get_route_area(self):
        """Return the route area to be used in deliveries."""
        self.ensure_one()
        return self.route_area_id

    def _get_location_final(self):
        location = super()._get_location_final()
        route_area = self._get_route_area()
        return route_area.location_id or location
