# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT

from .common import CommonTestCase


class TestSaleOrder(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))

    def create_sale_order(self, payment_method_line=None):
        with Form(self.env["sale.order"]) as sale_form:
            sale_form.partner_id = self.base_partner
            for _, p in self.products.items():
                with sale_form.order_line.new() as order_line:
                    order_line.product_id = p
                    order_line.name = p.name
                    order_line.product_uom_qty = 2
                    order_line.product_uom = p.uom_id
                    order_line.price_unit = p.list_price
        sale = sale_form.save()
        self.assertEqual(
            sale.payment_method_line_id,
            self.base_partner.property_inbound_payment_method_line_id,
        )
        sale_form = Form(sale)

        # force payment method
        if payment_method_line:
            sale_form.payment_method_line_id = payment_method_line
        return sale_form.save()

    def create_invoice_and_check(
        self, order, expected_payment_method_line, expected_partner_bank
    ):
        order.action_confirm()
        order._create_invoices()
        invoice = order.invoice_ids
        self.assertEqual(len(invoice), 1)
        self.assertEqual(
            invoice.preferred_payment_method_line_id, expected_payment_method_line
        )
        self.assertEqual(invoice.partner_bank_id, expected_partner_bank)

    def test_sale_to_invoice_payment_method_line(self):
        """
        Data:
            A partner with a specific payment_method_line
            A sale order created with the payment_method_line of the partner
        Test case:
            Create the invoice from the sale order
        Expected result:
            The invoice must be created with the payment_method_line of the partner
        """
        order = self.create_sale_order()
        self.create_invoice_and_check(order, self.payment_method_line, self.bank)

    def test_sale_to_invoice_payment_method_line_2(self):
        """
        Data:
            A partner with a specific payment_method_line
            A sale order created with an other payment_method_line
        Test case:
            Create the invoice from the sale order
        Expected result:
            The invoice must be created with the specific payment_method_line
        """
        order = self.create_sale_order(payment_method_line=self.payment_method_line_2)
        self.create_invoice_and_check(order, self.payment_method_line_2, self.bank)

    def test_sale_to_invoice_payment_method_line_via_payment(self):
        """
        Data:
            A partner with a specific payment_method_line
            A sale order created with an other payment_method_line
        Test case:
            Create the invoice from sale.advance.payment.inv
        Expected result:
            The invoice must be created with the specific payment_method_line
        """
        order = self.create_sale_order(payment_method_line=self.payment_method_line_2)
        context = {
            "active_model": "sale.order",
            "active_ids": [order.id],
            "active_id": order.id,
        }
        order.action_confirm()
        payment = self.env["sale.advance.payment.inv"].create(
            {
                "advance_payment_method": "fixed",
                "fixed_amount": 5,
                "sale_order_ids": order,
            }
        )
        payment.with_context(**context).create_invoices()
        invoice = order.invoice_ids
        self.assertEqual(len(invoice), 1)
        self.assertEqual(
            invoice.preferred_payment_method_line_id, self.payment_method_line_2
        )
        self.assertEqual(
            invoice.partner_bank_id,
            self.payment_method_line_2.journal_id.bank_account_id,
        )

    def test_several_sale_to_invoice_payment_method_line(self):
        """
        Data:
            A partner with a specific payment_method_line
            A sale order created with the payment_method_line of the partner
            A sale order created with another payment_method_line
        Test case:
            Create the invoice from the sale orders
        Expected result:
            Two invoices should be generated
        """
        order_1 = self.create_sale_order()
        order_2 = self.create_sale_order(self.payment_method_line_2)
        orders = order_1 | order_2
        orders.action_confirm()
        invoices = orders._create_invoices()
        self.assertEqual(2, len(invoices))
