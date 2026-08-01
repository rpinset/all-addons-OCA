# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[("route_planning", "Route Planning")],
        ondelete={"route_planning": "set default"},
    )

    @api.onchange("delivery_type")
    def _onchange_delivery_type_route(self):
        if self.delivery_type == "route_planning":
            self.integration_level = "rate"

    @api.constrains("delivery_type", "integration_level")
    def _check_delivery_type_route(self):
        for carrier in self:
            if (
                carrier.delivery_type == "route_planning"
                and carrier.integration_level != "rate"
            ):
                raise ValidationError(
                    self.env._(
                        "The delivery carrier: %s with provider type: 'Route Planning' "
                        "cannot create shipments, "
                        "please change the integration level to ' Get rate'.",
                        carrier.name,
                    )
                )

    def route_planning_rate_shipment(self, order):
        return {
            "success": True,
            "price": order.pricelist_id._get_product_price(self.product_id, 1.0),
            "error_message": False,
            "warning_message": False,
        }

    def route_planning_send_shipping(self, pickings):
        raise ValidationError(
            self.env._(
                "The delivery carrier: %s with provider type: 'Route Planning' "
                "cannot create shipments.",
                self.name,
            )
        )
