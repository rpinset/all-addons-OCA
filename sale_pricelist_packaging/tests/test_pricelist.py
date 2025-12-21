# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.config.settings"].create(
            {
                "group_product_pricelist": True,
                "group_discount_per_so_line": True,
                "group_stock_packaging": True,
            }
        ).execute()  # execute() applique les changements.

        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_5")

        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 20,
                        }
                    ),
                ],
            }
        )

        cls.pricelist = cls.order.pricelist_id

        cls.packaging1 = cls.env["product.packaging"].create(
            {
                "name": "Test1",
                "product_id": cls.product.id,
                "qty": 10,
            }
        )
        cls.packaging2 = cls.env["product.packaging"].create(
            {
                "name": "Test2",
                "product_id": cls.product.id,
                "qty": 20,
            }
        )
        cls.env["product.pricelist.item"].create(
            [
                {
                    "applied_on": "0_product_variant",
                    "pricelist_id": cls.pricelist.id,
                    "product_id": cls.product.id,
                    "fixed_price": 100,
                    "packaging_id": cls.packaging1.id,
                },
                {
                    "applied_on": "0_product_variant",
                    "pricelist_id": cls.pricelist.id,
                    "product_id": cls.product.id,
                    "fixed_price": 200,
                    "packaging_id": cls.packaging2.id,
                },
                {
                    "applied_on": "0_product_variant",
                    "pricelist_id": cls.pricelist.id,
                    "product_id": cls.product.id,
                    "fixed_price": 10,
                },
            ]
        )

    def test_packaging_1(self):
        self.order.order_line.product_packaging_id = self.packaging1
        self.assertEqual(self.order.order_line.price_unit, 100)

    def test_packaging_2(self):
        self.order.order_line.product_packaging_id = self.packaging2
        self.assertEqual(self.order.order_line.price_unit, 200)

    def test_without_packaging(self):
        self.order.order_line.product_packaging_id = False
        self.assertEqual(self.order.order_line.price_unit, 10)
