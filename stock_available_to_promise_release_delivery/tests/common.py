# Copyright 2025 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
from odoo.fields import Command

from odoo.addons.stock_available_to_promise_release.tests.common import (
    PromiseReleaseCommonCase,
)


class Common(PromiseReleaseCommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ref = cls.env.ref
        cls.customer = ref("base.res_partner_12")
        cls.wh.delivery_route_id.write(
            {
                "available_to_promise_defer_pull": True,
            }
        )
        cls.setUpClassProduct()
        cls.setUpClassCarrier()

    @classmethod
    def setUpClassProduct(cls):
        cls.product_model = cls.env["product.product"]
        cls.product = cls.product1
        cls.product.weight = 10.0
        cls.product.volume = 10.0
        cls.delivery_product = cls.env.ref("delivery.product_product_delivery")
        cls.product2.weight = 0.1

    @classmethod
    def setUpClassCarrier(cls):
        cls.carrier_model = cls.env["delivery.carrier"]
        # Normal carrier without route
        cls.normal_carrier = cls.carrier_model.create(
            {
                "name": "Normal Carrier",
                "product_id": cls.delivery_product.id,
                "sequence": 30,
            }
        )
        # The Poste carrier with a route
        cls.the_poste_carrier = cls.carrier_model.create(
            {
                "name": "Poste Carrier",
                "product_id": cls.delivery_product.id,
                "sequence": 20,
                "max_weight": 30,
            }
        )
        cls.new_route = cls.wh.delivery_route_id.copy({"shipping_selectable": True})
        cls.the_poste_delivery_rule = cls.new_route.rule_ids.filtered(
            lambda r: r.location_dest_id
            == cls.env.ref("stock.stock_location_customers")
        )
        cls.the_poste_delivery_rule.picking_type_id = cls.wh.out_type_id.copy()
        cls.the_poste_pick_rule = cls.new_route.rule_ids - cls.the_poste_delivery_rule
        cls.the_poste_pick_rule.picking_type_id = cls.wh.pick_type_id.copy()
        cls.the_poste_carrier.route_ids = [Command.set(cls.new_route.ids)]
