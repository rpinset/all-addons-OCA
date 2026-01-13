# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestSaleOrderLineClientOrderReference(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "service"}
        )
        cls.test_partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.sale_order = cls.env["sale.order"].create(
            {"partner_id": cls.test_partner.id, "client_order_ref": "Test Ref"}
        )
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.test_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            }
        )

    def test_01_prepare_invoice_line(self):
        self.assertEqual(self.order_line.client_order_ref, "Test Ref")
        self.order_line.write({"client_order_ref": "Test Customer Ref"})
        self.sale_order.action_confirm()
        invoice = self.sale_order._create_invoices()
        self.assertEqual(invoice.invoice_line_ids.client_order_ref, "Test Customer Ref")
