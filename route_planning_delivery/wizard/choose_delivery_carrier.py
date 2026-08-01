# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = "choose.delivery.carrier"

    route_area_id = fields.Many2one(
        "route.area",
        compute="_compute_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id", "company_id", "delivery_type", "order_id")
    def _compute_route_area_id(self):
        self.route_area_id = False
        for wizard in self.filtered(lambda w: w.delivery_type == "route_planning"):
            company = wizard.company_id or self.env.company
            partner = wizard.partner_id.with_company(company)
            wizard.route_area_id = self.order_id.route_area_id or partner.route_area_id

    def button_confirm(self):
        res = super().button_confirm()
        self.order_id.write({"route_area_id": self.route_area_id.id})
        return res
