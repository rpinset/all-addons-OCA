# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleOrder(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.utm_source = cls.env["utm.source"].create(
            {
                "name": "Test UTM Source",
            }
        )
        cls.sale_order = cls.env["sale.order"]

    def test_create_sale_order_with_partner_utm_source(self):
        """Test creating a sale order with a partner having a UTM source"""
        # Set UTM source on partner
        self.partner.utm_source_id = self.utm_source

        # Create sale order
        order = self.sale_order.create(
            {
                "partner_id": self.partner.id,
            }
        )

        # Check that UTM source was copied from partner
        self.assertEqual(order.source_id, self.utm_source)

    def test_create_sale_order_without_partner_utm_source(self):
        """Test creating a sale order with a partner without UTM source"""
        # Create sale order without UTM source on partner
        order = self.sale_order.create(
            {
                "partner_id": self.partner.id,
            }
        )

        # Check that UTM source is not set
        self.assertFalse(order.source_id)

    def test_create_multiple_sale_orders(self):
        """Test creating multiple sale orders in a batch"""
        # Set UTM source on partner
        self.partner.utm_source_id = self.utm_source

        # Create multiple sale orders
        orders = self.sale_order.create(
            [
                {
                    "partner_id": self.partner.id,
                },
                {
                    "partner_id": self.partner.id,
                },
            ]
        )

        # Check that UTM source was copied for all orders
        for order in orders:
            self.assertEqual(order.source_id, self.utm_source)
