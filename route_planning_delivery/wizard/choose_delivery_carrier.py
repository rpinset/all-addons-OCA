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

    # It is important to redefine the fields in the onchange event
    @api.onchange("carrier_id", "total_weight")
    def _onchange_carrier_id(self):
        res = super()._onchange_carrier_id()
        # We call super() and then define the corresponding price in the same way
        # that delivery does.
        # The delivery module only calculates and displays the price if `delivery_type`
        # is in ("fixed", "base_on_rule"), but for specific delivery_type values
        # (such as route_planning), you need to add specific code if, for example, you
        # want to set a fixed price of 10$ for the carrier's product, have it displayed
        # in the wizard, and have it applied to the sales order.
        if self.delivery_type == "route_planning":
            vals = self._get_delivery_rate()
            if vals.get("error_message"):
                return {"error": vals["error_message"]}
        return res

    def button_confirm(self):
        res = super().button_confirm()
        self.order_id.write({"route_area_id": self.route_area_id.id})
        return res
