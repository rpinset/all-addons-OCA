# Copyright 2025 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestSaleOrderCancelNoEmail(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "consu"}
        )

    def _create_confirmed_sale_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                        },
                    )
                ],
            }
        )
        sale_order.action_confirm()
        return sale_order

    def test_cancel_with_disable_warning_context(self):
        sale_order = self._create_confirmed_sale_order()
        self.assertEqual(sale_order.state, "sale")
        result = sale_order.with_context(disable_cancel_warning=True).action_cancel()
        self.assertTrue(result)
        self.assertEqual(sale_order.state, "cancel")

    def test_cancel_without_context_opens_wizard(self):
        sale_order = self._create_confirmed_sale_order()
        self.assertEqual(sale_order.state, "sale")
        result = sale_order.action_cancel()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("res_model"), "sale.order.cancel")
