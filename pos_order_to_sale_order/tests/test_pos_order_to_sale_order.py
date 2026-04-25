# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestPosOrderToSaleOrder(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create({"name": "Test pricelist"})
        cls.tax_10 = cls.env["account.tax"].create(
            {
                "name": "Test tax 10%",
                "type_tax_use": "sale",
                "amount": 10,
            }
        )
        cls.tax_10_price_include = cls.env["account.tax"].create(
            {
                "name": "Test tax 10% (price include)",
                "type_tax_use": "sale",
                "amount": 10,
                "price_include": True,
            }
        )
        cls.fp = cls.env["account.fiscal.position"].create(
            {
                "name": "Test fp",
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": cls.tax_10.id,
                            "tax_dest_id": cls.tax_10_price_include.id,
                        },
                    )
                ],
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test customer. Odoo",
                "property_product_pricelist": cls.pricelist.id,
                "property_account_position_id": cls.fp.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "list_price": 1.10,
                "type": "product",
                "taxes_id": [(6, 0, cls.tax_10.ids)],
            }
        )
        cls.pos_config = cls.env.ref("point_of_sale.pos_config_main")

    def test_pos_order_to_sale_order(self):
        order_data = {
            "pos_session_id": self.pos_config.current_session_id.id,
            "partner_id": self.partner.id,
            "pricelist_id": self.partner.property_product_pricelist.id,
            "fiscal_position_id": self.fp.id,
            "name": "test",
            "user_id": False,
            "lines": [
                (
                    0,
                    0,
                    {
                        "name": "test-line-1",
                        "product_id": self.product.id,
                        "price_unit": 1.1,
                        "price_subtotal": 1.1,
                        "qty": 1,
                        "discount": 0,
                        "tax_ids": [(6, 0, self.tax_10.ids)],
                    },
                ),
            ],
        }
        order_model = self.env["sale.order"]
        res = order_model.create_order_from_pos(order_data, False)
        order = order_model.browse(res["sale_order_id"])
        self.assertEqual(order.partner_id, self.partner)
        self.assertEqual(order.client_order_ref, "test")
        self.assertFalse(order.user_id)
        self.assertEqual(order.pricelist_id, self.pricelist)
        self.assertEqual(order.fiscal_position_id, self.fp)
        self.assertEqual(len(order.order_line), 1)
        self.assertEqual(order.order_line.product_id, self.product)
        self.assertEqual(order.order_line.price_unit, 1.1)
        self.assertEqual(order.order_line.product_uom_qty, 1)
        self.assertIn(self.tax_10_price_include, order.order_line.tax_id)
        self.assertEqual(order.amount_untaxed, 1)
        self.assertEqual(order.amount_tax, 0.1)
        self.assertEqual(order.amount_total, 1.1)
