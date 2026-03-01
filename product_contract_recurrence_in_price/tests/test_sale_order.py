# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.product_contract.tests.test_sale_order import (
    TestSaleOrder as TestSaleOrderBase,
)


class TestSaleOrder(TestSaleOrderBase):
    def test_compute_amount(self):
        """
        Check that recurrence is taken into account in line amounts.
        A SO line recurrent over 2 years and invoiced every 4 months will
        be invoiced 6 times in total.
        """
        tax = self.env["account.tax"].create(
            {
                "name": "10% tax",
                "amount_type": "percent",
                "amount": 10,
            }
        )
        self.order_line1.update(
            {
                "price_unit": 100,
                "product_uom_qty": 10,
                "recurrence_number": 2,
                "recurrence_interval": "yearly",
                "recurring_interval": 4,
                "recurring_rule_type": "monthly",
                "tax_id": [(4, tax.id)],
            }
        )
        self.assertEqual(self.order_line1.price_subtotal, 1000)
        self.assertEqual(self.order_line1.price_tax, 100)
        self.assertEqual(self.order_line1.price_total, 1100)
        self.order_line1.include_recurrence_in_price = True
        self.assertEqual(self.order_line1.recurring_invoicing_number, 6)
        self.assertEqual(self.order_line1.price_subtotal, 6000)
        self.assertEqual(self.order_line1.price_tax, 600)
        self.assertEqual(self.order_line1.price_total, 6600)
