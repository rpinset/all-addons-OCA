# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import tagged

from odoo.addons.account_payment_batch_oca.tests.test_payment_order_outbound import (
    TestPaymentOrderOutboundBase,
)


@tagged("-at_install", "post_install")
class TestAccountPaymentEarlyPaymentDiscount(TestPaymentOrderOutboundBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.pay_terms_7_days_10_discount = cls.env["account.payment.term"].create(
            {
                "name": "10% early discount 7 days",
                "early_discount": True,
                "discount_percentage": 10,
                "discount_days": 7,
            }
        )

        cls.mode.payment_account_id = cls.env["account.account"].create(
            {
                "name": "Outstanding Payments",
                "prefix": "BNKT",
                "code_digits": 550010,
                "account_type": "asset_current",
                "reconcile": True,
            }
        )

    def test_basic_order(self):
        """Simple payment order should still work"""
        self.invoice.action_post()

        self.invoice.create_account_payment_line()
        self.assertFalse(self.invoice.invoice_payment_term_id.early_discount)

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)
        self.assertFalse(payment_line.pay_with_discount)

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

    def test_order_with_discount(self):
        """One invoice with discount of 10%"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount

        self.invoice.action_post()
        self.invoice.create_account_payment_line()
        self.assertTrue(self.invoice.invoice_payment_term_id.early_discount)

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)

        self.assertEqual(payment_order.date_prefered, "due")
        self.assertFalse(payment_line.pay_with_discount)

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            100.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            100.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            90.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )

        self.assertTrue(payment_line.can_have_discount)
        payment_line.pay_with_discount = True

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            100.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            90.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            90.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_line.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 3)

        # 3 move lines:
        # -10.0: early payment discount
        # -90.0: payment
        # 100.0: invoice amount
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-90.0, -10.0, 100.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_order_with_discount_and_tax(self):
        """One invoice with discount of 10% and tax of 15%"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        # Tax of 15%
        self.invoice.invoice_line_ids.tax_ids = self.tax_purchase_a

        self.invoice.action_post()
        self.invoice.create_account_payment_line()
        self.assertTrue(self.invoice.invoice_payment_term_id.early_discount)

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)

        self.assertEqual(payment_order.date_prefered, "due")
        self.assertFalse(payment_line.pay_with_discount)

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            100.0 + 15.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            100.0 + 15.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            90.0 + 13.50,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            10.0 + 1.50,
            places=payment_line.currency_id.decimal_places,
        )

        self.assertTrue(payment_line.can_have_discount)
        payment_line.pay_with_discount = True

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            100.0 + 15.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            90.0 + 13.50,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            90.0 + 13.50,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            10.0 + 1.50,
            places=payment_line.currency_id.decimal_places,
        )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_line.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 4)

        # 4 move lines:
        # -10.0: early payment discount
        # -1.50: early payment discount TAX
        # -103.50: payment
        # 115.0: invoice amount
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-103.50, -10.0, -1.50, 115.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_order_with_discount_and_refund(self):
        """Invoice (100$) with discount(10%) and partially paid with refund(90$)"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice.action_post()

        self.refund = self._create_supplier_refund(self.invoice, manual=True)
        # payment term should be the same as on invoice
        self.refund.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.refund.action_post()

        (self.invoice.line_ids + self.refund.line_ids).filtered(
            lambda line: line.account_type == "liability_payable"
        ).reconcile()

        self.invoice.create_account_payment_line()

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        self.assertTrue(payment_line.can_have_discount)
        payment_line.pay_with_discount = True

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_line.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 4)

        # 4 move lines:
        # -10.0: early payment discount on invoice (10% of 100%)
        # -9.00: payment
        # 9.0: early payment discount on refund (10% of 90$)
        # 10.0: invoice amount
        # note that if in config account for early payment
        # discount gain/loss is set at the same,
        # ealy payment discount lines will be additioned
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-10.0, -9.0, 9.0, 10.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_order_with_discount_forced(self):
        """Invoice (100$) with discount(10%) even if
        it is not in condition of payment term"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice.invoice_date = fields.Date.today() + relativedelta(months=-1)
        self.invoice.action_post()

        self.refund = self._create_supplier_refund(self.invoice, manual=True)
        # payment term should be the same as on invoice
        self.refund.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.refund.action_post()

        (self.invoice.line_ids + self.refund.line_ids).filtered(
            lambda line: line.account_type == "liability_payable"
        ).reconcile()

        self.invoice.create_account_payment_line()

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)
        # Discount date is in the past so, we should force discount if
        # we want to do an "early payment discount"
        self.assertTrue(payment_line.discount_date < fields.Date.today())

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        self.assertTrue(payment_line.can_have_discount)
        payment_line.pay_with_discount = True

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_line.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 4)

        # 4 move lines:
        # -10.0: early payment discount on invoice (10% of 100%)
        # -9.00: payment
        # 9.0: early payment discount on refund (10% of 90$)
        # 10.0: invoice amount
        # note that if in config account for early payment discount
        # gain/loss is set at the same,
        # ealy payment discount lines will be additioned
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-10.0, -9.0, 9.0, 10.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_with_2_nc(self):
        """Invoice (100$) with discount(10%) and partially paid with refunds(40+50)"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice.action_post()

        self.refund = self._create_supplier_refund(self.invoice, manual=True)
        # payment term should be the same as on invoice
        self.refund.invoice_line_ids.price_unit = 40.0
        self.refund.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.refund.action_post()

        self.refund2 = self._create_supplier_refund(self.invoice, manual=True)
        # payment term should be the same as on invoice
        self.refund2.invoice_line_ids.price_unit = 50.0
        self.refund2.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.refund2.action_post()

        (self.invoice.line_ids + self.refund.line_ids + self.refund2.line_ids).filtered(
            lambda line: line.account_type == "liability_payable"
        ).reconcile()

        self.invoice.create_account_payment_line()

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_line = payment_order.payment_line_ids
        self.assertEqual(len(payment_line), 1)

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        self.assertTrue(payment_line.can_have_discount)
        payment_line.pay_with_discount = True

        self.assertAlmostEqual(
            payment_line.amount_residual_currency,
            10.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.discount_amount_currency,
            9.0,
            places=payment_line.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            payment_line.diff_amount_residual_currency_amount_discount_currency,
            1.0,
            places=payment_line.currency_id.decimal_places,
        )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_line.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 4)

        # 4 move lines:
        # -10.0: early payment discount on invoice (10% of 100%)
        # -9.00: payment
        # 9.0: early payment discount on refund (10% of 90$)
        # 10.0: invoice amount
        # note that if in config account for early payment
        # discount gain/loss is set at the same,
        # ealy payment discount lines will be additioned
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-10.0, -9.0, 9.0, 10.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_with_2_invoices(self):
        """Two invoices and discount of 10%"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice.action_post()
        self.invoice.create_account_payment_line()
        self.assertTrue(self.invoice.invoice_payment_term_id.early_discount)

        self.invoice_02.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice_02.action_post()
        self.invoice_02.create_account_payment_line()

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_lines = payment_order.payment_line_ids
        self.assertEqual(len(payment_lines), 2)

        self.assertEqual(payment_order.date_prefered, "due")

        for payment_line in payment_lines:
            self.assertFalse(payment_line.pay_with_discount)

            self.assertAlmostEqual(
                payment_line.amount_residual_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.amount_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.discount_amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.diff_amount_residual_currency_amount_discount_currency,
                10.0,
                places=payment_line.currency_id.decimal_places,
            )

            self.assertTrue(payment_line.can_have_discount)
            payment_line.pay_with_discount = True

            self.assertAlmostEqual(
                payment_line.amount_residual_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.discount_amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.diff_amount_residual_currency_amount_discount_currency,
                10.0,
                places=payment_line.currency_id.decimal_places,
            )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 1)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        payment_move_lines = payment_lines.payment_ids.move_id.line_ids
        self.assertEqual(len(payment_move_lines), 3)

        # 3 move lines:
        # -20.0: early payment discount
        # -180.0: payment
        # 200.0: invoice amount
        amounts = payment_move_lines.mapped("amount_currency")
        for amount, target_amount in zip(
            sorted(amounts), [-180.0, -20.0, 200.0], strict=False
        ):
            self.assertAlmostEqual(
                amount,
                target_amount,
                places=payment_move_lines.currency_id.decimal_places,
            )

    def test_with_2_invoices_different_partner(self):
        """Two invoices with 2 different partners and discount of 10%"""
        self.invoice.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice.action_post()
        self.invoice.create_account_payment_line()
        self.assertTrue(self.invoice.invoice_payment_term_id.early_discount)

        partnerb = self.env["res.partner"].create(
            {
                "name": "Test Partner B",
            }
        )

        self.invoice_02.invoice_payment_term_id = self.pay_terms_7_days_10_discount
        self.invoice_02.partner_id = partnerb
        self.invoice_02.preferred_payment_method_line_id = self.mode
        self.invoice_02.action_post()
        self.invoice_02.create_account_payment_line()

        payment_order = self.env["account.payment.order"].search(self.domain)
        self.assertEqual(len(payment_order), 1)

        payment_lines = payment_order.payment_line_ids
        self.assertEqual(len(payment_lines), 2)

        self.assertEqual(payment_order.date_prefered, "due")

        for payment_line in payment_lines:
            self.assertFalse(payment_line.pay_with_discount)

            self.assertAlmostEqual(
                payment_line.amount_residual_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.amount_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.discount_amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.diff_amount_residual_currency_amount_discount_currency,
                10.0,
                places=payment_line.currency_id.decimal_places,
            )

            self.assertTrue(payment_line.can_have_discount)
            payment_line.pay_with_discount = True

            self.assertAlmostEqual(
                payment_line.amount_residual_currency,
                100.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.discount_amount_currency,
                90.0,
                places=payment_line.currency_id.decimal_places,
            )
            self.assertAlmostEqual(
                payment_line.diff_amount_residual_currency_amount_discount_currency,
                10.0,
                places=payment_line.currency_id.decimal_places,
            )

        payment_order.draft2open()
        self.assertEqual(payment_order.payment_count, 2)
        self.assertEqual(payment_order.payment_lot_count, 1)

        payment_order.open2generated()
        payment_order.generated2uploaded()

        self.assertEqual(payment_order.state, "uploaded")

        for payment_line in payment_lines:
            payment_move_lines = payment_line.payment_ids.move_id.line_ids
            self.assertEqual(len(payment_move_lines), 3)

            # 3 move lines:
            # -10.0: early payment discount
            # -90.0: payment
            # 100.0: invoice amount
            amounts = payment_move_lines.mapped("amount_currency")
            for amount, target_amount in zip(
                sorted(amounts), [-90.0, -10.0, 100.0], strict=False
            ):
                self.assertAlmostEqual(
                    amount,
                    target_amount,
                    places=payment_move_lines.currency_id.decimal_places,
                )
