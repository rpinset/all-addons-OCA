# Copyright 2017 ForgeFlow S.L.
#        (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields
from odoo.tests.common import TransactionCase


# @tagged("post_install", "-at_install")
class TestAccountInvoiceViewPayment(TransactionCase):
    """
    Tests for Account Invoice View Payment.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group_ids = cls.env.ref("account.group_account_invoice").ids
        cls.test_user_1 = cls.env["res.users"].create(
            {"name": "John", "login": "test1", "groups_id": [(6, 0, group_ids)]}
        )
        cls.par_model = cls.env["res.partner"]
        cls.acc_model = cls.env["account.account"]
        cls.inv_model = cls.env["account.move"]
        cls.inv_line_model = cls.env["account.move.line"]
        cls.pay_model = cls.env["account.payment"]
        cls.reg_pay_model = cls.env["account.payment.register"]

        cls.cash = cls.env["account.journal"].create(
            {"name": "Cash Test", "type": "cash", "code": "CT"}
        )
        cls.payment_method_manual_in = cls.env.ref(
            "account.account_payment_method_manual_in"
        )

        cls.default_line_account = cls.acc_model.create(
            {
                "name": "TESTACC",
                "code": "TESTACC",
                "account_type": "income",
                "deprecated": False,
                "company_id": cls.env.user.company_id.id,
            }
        )

        cls.inbound_payment_method_line = cls.cash.inbound_payment_method_line_ids[0]
        cls.outbound_payment_method_line = cls.cash.outbound_payment_method_line_ids[0]

        cls.partner = cls._create_partner()
        cls.invoice1 = cls._create_invoice(cls.partner, "out_invoice")
        cls.invoice2 = cls._create_invoice(cls.partner, "in_invoice")
        cls.invoice3 = cls._create_invoice(cls.partner, "in_invoice")
        cls.invoice2.invoice_date = cls.invoice3.invoice_date = fields.Date.today()

    @classmethod
    def _create_partner(cls):
        partner = cls.par_model.create(
            {"name": "Test Partner", "company_type": "company"}
        )
        return partner

    @classmethod
    def _create_invoice(cls, partner, invoice_type):
        cls.invoice_lines = [
            (
                0,
                False,
                {
                    "name": "Test section",
                    "display_type": "line_section",
                },
            ),
            (
                0,
                False,
                {
                    "name": "Test description #1",
                    "account_id": cls.default_line_account.id,
                    "quantity": 1.0,
                    "price_unit": 100.0,
                },
            ),
            (
                0,
                False,
                {
                    "name": "Test description #2",
                    "account_id": cls.default_line_account.id,
                    "quantity": 2.0,
                    "price_unit": 25.0,
                },
            ),
        ]
        cls.invoice = cls.env["account.move"].create(
            {
                "partner_id": cls.partner.id,
                "move_type": invoice_type,
                "invoice_line_ids": cls.invoice_lines,
            }
        )
        return cls.invoice

    def test_account_move_view_payment_out_invoice(self):
        self.invoice1.action_post()
        wiz = (
            self.env["account.payment"]
            .with_user(self.test_user_1)
            .with_context(active_id=[self.invoice1.id], active_model="account.move")
            .create(
                {
                    "journal_id": self.cash.id,
                    "payment_method_id": self.payment_method_manual_in.id,
                    "amount": self.invoice1.amount_residual,
                    "payment_type": "inbound",
                    "payment_method_line_id": self.inbound_payment_method_line.id,
                }
            )
        )

        res = wiz.post_and_open_payment()

        expect = {"type": "ir.actions.act_window", "res_model": "account.payment"}
        self.assertDictEqual(
            expect,
            {k: v for k, v in res.items() if k in expect},
            "There was an error and the view couldn't be opened.",
        )

        view_payment = self.invoice1.action_view_payments()

        expect1 = {"type": "ir.actions.act_window", "res_model": "account.payment"}
        self.assertDictEqual(
            expect1,
            {k: v for k, v in view_payment.items() if k in expect1},
            "There was an error and the invoice couldn't be paid.",
        )

    def test_account_move_view_payment_in_invoice(self):
        self.invoice2.action_post()
        wiz = (
            self.pay_model.with_user(self.test_user_1)
            .with_context(active_id=[self.invoice2.id], active_model="account.move")
            .create(
                {
                    "journal_id": self.cash.id,
                    "payment_method_id": self.payment_method_manual_in.id,
                    "amount": self.invoice2.amount_residual,
                    "payment_type": "inbound",
                    "payment_method_line_id": self.inbound_payment_method_line.id,
                }
            )
        )

        res = wiz.post_and_open_payment()

        expect = {"type": "ir.actions.act_window", "res_model": "account.payment"}
        self.assertDictEqual(
            expect,
            {k: v for k, v in res.items() if k in expect},
            "There was an error and the view couldn't be opened.",
        )

        view_payment = self.invoice2.with_user(self.test_user_1).action_view_payments()
        expect1 = {"type": "ir.actions.act_window", "res_model": "account.payment"}
        self.assertDictEqual(
            expect1,
            {k: v for k, v in view_payment.items() if k in expect1},
            "There was an error and the view couldn't be opened.",
        )

    def test_view_account_payment_register_form(self):
        self.invoice2.action_post()
        self.invoice3.action_post()
        wiz = (
            self.reg_pay_model.with_user(self.test_user_1)
            .with_context(
                active_ids=[self.invoice2.id, self.invoice3.id],
                active_model="account.move",
            )
            .create(
                {
                    "journal_id": self.cash.id,
                }
            )
        )

        res = wiz.action_create_payments()

        expect = {"type": "ir.actions.act_window", "res_model": "account.payment"}
        self.assertDictEqual(
            expect,
            {k: v for k, v in res.items() if k in expect},
            "There was an error and the two invoices were not merged.",
        )
