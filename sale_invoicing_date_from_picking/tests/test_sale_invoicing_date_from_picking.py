# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date

from odoo.tests.common import TransactionCase


class TestSaleInvoicingDateFromPicking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 1.0,
                        },
                    )
                ],
            }
        )
        cls.sale_order.action_confirm()
        cls.wizard = cls.env["sale.advance.payment.inv"].create(
            {
                "advance_payment_method": "delivered",
                "stock_picking_ids": cls.sale_order.picking_ids.ids,
                "invoice_date": date.today(),
            }
        )

    def test_invoice_date_is_set(self):
        (invoices,) = self.wizard._create_invoices(self.sale_order)
        self.assertEqual(invoices.invoice_date, date.today())
