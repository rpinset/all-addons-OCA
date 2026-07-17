# Copyright 2025 Tecnativa - Carlos Lopez
# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    route_area_id = fields.Many2one(
        "route.area",
        compute="_compute_route_area_id",
        inverse="_inverse_route_area_id",
        store=True,
        readonly=False,
        tracking=True,
    )

    @api.depends("partner_shipping_id", "company_id")
    def _compute_route_area_id(self):
        for order in self:
            company = order.company_id or self.env.company
            partner = order.partner_shipping_id.with_company(company)
            order.route_area_id = partner.route_area_id

    def _inverse_route_area_id(self):
        """When we change the route area (for example, through the change delivery
        method wizard if route_planning_delivery is installed) from sale order,
        we will update the route_area_id for pending pickings and moves
        """
        for item in self.filtered("picking_ids"):
            item.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            ).write({"route_area_id": item.route_area_id.id})


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_route_area_location(self):
        self.ensure_one()
        return self.order_id.route_area_id.location_id

    def _get_location_final(self):
        location = super()._get_location_final()
        ra_location = self._get_route_area_location()
        return ra_location or location
