# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from freezegun import freeze_time

from odoo.tests import Form, TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@freeze_time("2025-08-01")
class TestRefundEarlyPaymentDiscount(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.customer = cls.env["res.partner"].create({"name": "Test"})
        cls.discount_payment_term = cls.env["account.payment.term"].create(
            {
                "name": "EPD",
                "early_discount": True,
                "discount_days": 10,
                "discount_percentage": 10.0,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value_amount": 100,
                            "value": "percent",
                            "nb_days": 30,
                            "delay_type": "days_after",
                        },
                    )
                ],
            }
        )

    @classmethod
    def init_invoice(
        cls,
        partner,
        move_type,
        payment_term=None,
        invoice_date=None,
        currency=None,
        payment_reference=None,
    ):
        move_form = Form(
            cls.env["account.move"].with_context(default_move_type=move_type)
        )
        move_form.partner_id = partner
        move_form.invoice_payment_term_id = payment_term
        move_form.invoice_date = invoice_date
        if currency is not None:
            move_form.currency_id = currency
        if payment_reference is not None:
            move_form.payment_reference = payment_reference
        return move_form.save()

    @classmethod
    def init_invoice_line(cls, invoice, quantity, unit_price, product=None):
        with Form(invoice) as move_form:
            with move_form.invoice_line_ids.new() as line_form:
                if product:
                    line_form.product_id = product
                line_form.name = product and product.name or "test"
                line_form.quantity = quantity
                line_form.price_unit = unit_price

    def test_customer_refund_early_payment_discount(self):
        invoice = self.init_invoice(
            self.customer,
            "out_invoice",
            payment_term=self.discount_payment_term,
            invoice_date="2025-08-01",
        )
        self.init_invoice_line(invoice, 1.0, 100.0)
        invoice.action_post()
        with freeze_time("2025-08-09"):
            payment_wizard_form = Form(
                self.env["account.payment.register"].with_context(
                    active_model="account.move",
                    active_ids=invoice.ids,
                    active_id=invoice.id,
                )
            )
            payment_wizard = payment_wizard_form.save()
            self.assertEqual(payment_wizard.amount, 90.0)
            payment_wizard.action_create_payments()
            self.assertEqual(invoice.payment_state, "paid")

        with freeze_time("2025-08-15"):
            reverse_wizard_form = Form(
                self.env["account.move.reversal"].with_context(
                    active_model="account.move",
                    active_ids=invoice.ids,
                    active_id=invoice.id,
                )
            )
            reverse_wizard = reverse_wizard_form.save()
            refund_action = reverse_wizard.reverse_moves()
            refund = self.env["account.move"].browse(refund_action["res_id"])
            self.assertEqual(refund.amount_total, 100)
            refund.invoice_payment_term_id = self.discount_payment_term
            refund.action_post()
            payment_wizard_form = Form(
                self.env["account.payment.register"].with_context(
                    active_model="account.move",
                    active_ids=refund.ids,
                    active_id=refund.id,
                )
            )
            payment_wizard = payment_wizard_form.save()
            self.assertEqual(payment_wizard.amount, 90.0)
