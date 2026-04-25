# Copyright Binhex - Adasat Torres de Leon
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrder(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.user = cls.env.ref("base.user_admin")
        cls.product = cls.env.ref("product.product_product_4")
        cls.pos_config = cls.env.ref("point_of_sale.pos_config_main")
        cls.pos_session = cls.env["pos.session"].create(
            {"config_id": cls.pos_config.id, "user_id": cls.user.id}
        )

    def test_create_order_from_pos(self):
        order_data = {
            "pos_session_id": self.pos_session.id,
            "partner_id": self.partner.id,
            "name": "Test Ref",
            "user_id": self.user.id,
            "pricelist_id": self.env.ref("product.list0").id,
            "fiscal_position_id": False,
            "commitment_date": "2026-02-28T17:27:00.000Z",
            "lines": [
                (
                    0,
                    0,
                    {
                        "product_id": self.product.id,
                        "qty": 1,
                        "discount": 0,
                        "price_unit": 10.0,
                        "tax_ids": False,
                    },
                )
            ],
        }
        result = self.env["sale.order"].create_order_from_pos(
            order_data, action="draft"
        )
        self.assertIn("sale_order_id", result)
        sale_order = self.env["sale.order"].browse(result["sale_order_id"])
        self.assertEqual(sale_order.partner_id, self.partner)
        self.assertEqual(sale_order.origin, "Point of Sale %s" % self.pos_session.name)
        self.assertEqual(sale_order.client_order_ref, "Test Ref")
        self.assertEqual(sale_order.user_id, self.user)
        self.assertEqual(sale_order.pricelist_id, self.env.ref("product.list0"))
        self.assertFalse(sale_order.fiscal_position_id)
        self.assertEqual(sale_order.state, "draft")
        self.assertEqual(len(sale_order.order_line), 1)
        self.assertEqual(sale_order.order_line.product_id, self.product)
        self.assertEqual(sale_order.order_line.product_uom_qty, 1)
        self.assertEqual(sale_order.order_line.price_unit, 10.0)
        self.assertEqual(sale_order.commitment_date, datetime(2026, 2, 28, 17, 27, 0))

    def test_create_order_from_pos_without_commitment_date(self):
        """Verifica que commitment_date es opcional"""
        order_data = {
            "pos_session_id": self.pos_session.id,
            "partner_id": self.partner.id,
            "name": "Test Ref 2",
            "user_id": self.user.id,
            "pricelist_id": self.env.ref("product.list0").id,
            "fiscal_position_id": False,
            "lines": [
                (
                    0,
                    0,
                    {
                        "product_id": self.product.id,
                        "qty": 1,
                        "discount": 0,
                        "price_unit": 10.0,
                        "tax_ids": False,
                    },
                )
            ],
        }
        result = self.env["sale.order"].create_order_from_pos(
            order_data, action="draft"
        )
        sale_order = self.env["sale.order"].browse(result["sale_order_id"])
        self.assertFalse(sale_order.commitment_date)
