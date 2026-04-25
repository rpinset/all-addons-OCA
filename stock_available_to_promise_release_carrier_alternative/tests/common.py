# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.fields import Command

from odoo.addons.stock_available_to_promise_release.tests.common import (
    PromiseReleaseCommonCase,
)


class DeliveryCarrierAlternativeCommon(PromiseReleaseCommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ref = cls.env.ref
        cls.customer = ref("base.res_partner_12")
        cls.setUpClassProduct()
        cls.setUpClassCarrier()

        cls.wh.delivery_route_id.write(
            {
                "available_to_promise_defer_pull": True,
            }
        )
        cls.outgoing_pick_type = cls.wh.out_type_id
        cls.delivery = cls._create_picking_chain(cls.wh, [(cls.product1, 5)])
        cls.delivery.carrier_id = cls.normal_carrier

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
        cls.super_fast_carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Super fast carrier",
                "product_id": cls.delivery_product.id,
                "sequence": 10,
                "max_weight": 20,
            }
        )
        cls.the_poste_carrier = cls.carrier_model.create(
            {
                "name": "Poste Carrier",
                "product_id": cls.delivery_product.id,
                "sequence": 20,
                "max_weight": 30,
            }
        )
        cls.normal_carrier = cls.carrier_model.create(
            {
                "name": "Normal Carrier",
                "product_id": cls.delivery_product.id,
                "sequence": 30,
            }
        )

    @classmethod
    def set_alternatives(cls):
        cls.normal_carrier.alternative_carrier_ids = [
            Command.set((cls.the_poste_carrier | cls.super_fast_carrier).ids)
        ]
