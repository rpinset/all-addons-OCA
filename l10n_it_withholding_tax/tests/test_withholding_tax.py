# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2023 Simone Rubino - TAKOBI
# Copyright 2024 Simone Rubino - Aion Tech
# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import time
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestWithholdingTax(TransactionCase):
    def setUp(self):
        super(TestWithholdingTax, self).setUp()

        # Accounts
        type_payable = self.env.ref("account.data_account_type_payable")
        type_receivable = self.env.ref("account.data_account_type_receivable")
        self.wt_account_payable = self.env["account.account"].create(
            {
                "name": "Debiti per ritenute da versare",
                "code": "WT_001",
                "user_type_id": type_payable.id,
                "reconcile": True,
            }
        )
        self.wt_account_receivable = self.env["account.account"].create(
            {
                "name": "Crediti per ritenute subite",
                "code": "WT_002",
                "user_type_id": type_receivable.id,
                "reconcile": True,
            }
        )

        # Journals
        self.journal_misc = self.env["account.journal"].search(
            [("type", "=", "general")], limit=1
        )
        self.journal_bank = self.env["account.journal"].create(
            {"name": "Bank", "type": "bank", "code": "BNK67"}
        )

        # Payment Register
        self.payment_register_model = self.env["account.payment.register"]
        self.register_view_id = "account.view_account_payment_register_form"

        # Payments
        vals_payment = {
            "name": "",
            "line_ids": [(0, 0, {"value": "balance", "days": 15})],
        }
        self.payment_term_15 = self.env["account.payment.term"].create(vals_payment)

        self.account_expense, self.account_expense1 = self.env[
            "account.account"
        ].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                )
            ],
            limit=2,
        )

        # Withholding tax
        wt_vals = {
            "name": "Code 1040",
            "code": "1040",
            "certification": True,
            "account_receivable_id": self.wt_account_receivable.id,
            "account_payable_id": self.wt_account_payable.id,
            "journal_id": self.journal_misc.id,
            "payment_term": self.payment_term_15.id,
            "rate_ids": [
                (
                    0,
                    0,
                    {
                        "tax": 20,
                        "base": 1,
                    },
                )
            ],
        }
        self.wt1040 = self.env["withholding.tax"].create(wt_vals)

        # Supplier Invoice with WT
        invoice_line_vals = [
            (
                0,
                0,
                {
                    "quantity": 1.0,
                    "account_id": self.account_expense.id,
                    "name": "Advice",
                    "price_unit": 1000.00,
                    "invoice_line_tax_wt_ids": [(6, 0, [self.wt1040.id])],
                    "tax_ids": False,
                },
            )
        ]
        self.invoice = self.env["account.move"].create(
            {
                "invoice_date": time.strftime("%Y") + "-07-15",
                "name": "Test Supplier Invoice WT",
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "purchase")])[0]
                .id,
                "partner_id": self.env.ref("base.res_partner_12").id,
                "invoice_line_ids": invoice_line_vals,
                "move_type": "in_invoice",
            }
        )
        self.invoice._onchange_invoice_line_wt_ids()
        self.invoice.action_post()

    def test_withholding_tax(self):
        domain = [("name", "=", "Code 1040")]
        wts = self.env["withholding.tax"].search(domain)
        self.assertEqual(len(wts), 1, msg="Withholding tax was not created")

        self.assertEqual(
            self.invoice.withholding_tax_amount, 200, msg="Invoice WT amount"
        )
        self.assertEqual(
            self.invoice.amount_net_pay, 800, msg="Invoice WT amount net pay"
        )

        domain = [
            ("invoice_id", "=", self.invoice.id),
            ("withholding_tax_id", "=", self.wt1040.id),
        ]
        wt_statement = self.env["withholding.tax.statement"].search(domain)
        self.assertEqual(len(wt_statement), 1, msg="WT statement was not created")
        self.assertEqual(wt_statement.base, 1000, msg="WT statement Base amount")
        self.assertEqual(wt_statement.amount, 0, msg="WT statement amount applied")
        self.assertEqual(wt_statement.amount_paid, 0, msg="WT statement Base paid")

        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 800)

        ctx = {
            "active_model": "account.move",
            "active_ids": [self.invoice.id],
        }
        register_payments = self.payment_register_model.with_context(ctx).create(
            {
                "payment_date": time.strftime("%Y") + "-07-15",
                "amount": 800,
                "journal_id": self.journal_bank.id,
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
            }
        )
        register_payments.action_create_payments()

        partials = self.invoice._get_reconciled_invoices_partials()

        # WT payment generation
        self.assertEqual(len(partials), 2, msg="Missing WT payment")

        # WT amount in payment move lines
        self.assertTrue({p[1] for p in partials} == {800, 200})

        # WT amount applied in statement
        domain = [
            ("invoice_id", "=", self.invoice.id),
            ("withholding_tax_id", "=", self.wt1040.id),
        ]
        wt_statement = self.env["withholding.tax.statement"].search(domain)
        self.assertEqual(wt_statement.amount, 200)
        self.assertEqual(self.invoice.state, "posted")
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 0)

    def test_partial_payment(self):
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 800)
        ctx = {
            "active_model": "account.move",
            "active_ids": [self.invoice.id],
            "active_id": self.invoice.id,
            "default_reconciled_invoice_ids": [(4, self.invoice.id, None)],
        }
        register_payments = self.payment_register_model.with_context(ctx).create(
            {
                "payment_date": time.strftime("%Y") + "-07-15",
                "amount": 600,
                "journal_id": self.journal_bank.id,
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_out"
                ).id,
            }
        )
        register_payments.action_create_payments()

        partials = self.invoice._get_reconciled_invoices_partials()

        # WT payment generation
        self.assertEqual(len(partials), 2, msg="Missing WT payment")

        # WT amount in payment move lines
        self.assertTrue({p[1] for p in partials} == {600, 150})

        # WT amount applied in statement
        domain = [
            ("invoice_id", "=", self.invoice.id),
            ("withholding_tax_id", "=", self.wt1040.id),
        ]
        wt_statement = self.env["withholding.tax.statement"].search(domain)
        self.assertEqual(wt_statement.amount, 150)
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 200)
        self.assertEqual(self.invoice.amount_residual, 250)
        self.assertEqual(self.invoice.state, "posted")

    def test_overlapping_rates(self):
        """Check that overlapping rates cannot be created"""
        with self.assertRaises(ValidationError):
            self.wt1040.rate_ids = [
                (
                    0,
                    0,
                    {
                        "date_start": fields.Date.to_string(
                            date.today() - timedelta(days=1)
                        )
                    },
                )
            ]

    def test_keep_selected_wt(self):
        """Check that selected Withholding tax is kept in lines."""
        invoice_line_vals = [
            (
                0,
                0,
                {
                    "quantity": 1.0,
                    "account_id": self.account_expense.id,
                    "name": "Advice",
                    "price_unit": 1000.00,
                    "tax_ids": False,
                },
            )
        ]
        invoice = self.env["account.move"].create(
            {
                "invoice_date": time.strftime("%Y") + "-07-15",
                "name": "Test Supplier Invoice WT",
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "purchase")])[0]
                .id,
                "partner_id": self.env.ref("base.res_partner_12").id,
                "invoice_line_ids": invoice_line_vals,
                "move_type": "in_invoice",
            }
        )
        invoice_form = Form(invoice)
        with invoice_form.invoice_line_ids.edit(0) as line_form:
            line_form.invoice_line_tax_wt_ids.clear()
            line_form.invoice_line_tax_wt_ids.add(self.wt1040)
        invoice = invoice_form.save()
        self.assertTrue(invoice.invoice_line_ids.invoice_line_tax_wt_ids)

    def test_duplicating_wt(self):
        new_tax = self.wt1040.copy()
        self.assertEqual(new_tax.code, "1040 (copy)")
        self.assertEqual(new_tax.name, "Code 1040")

    def test_create_payments(self):
        """Test create payment when Register Payment wizard is open from Bill tree view"""
        ctx = {
            "active_ids": [self.invoice.id],
            "active_model": "account.move",
        }
        f = Form(
            self.payment_register_model.with_context(ctx), view=self.register_view_id
        )
        payment_register = f.save()
        # passing default_move_type="in_invoice" in the context in order
        # to simulate opening of payment_register from Bills tree view
        payment_register.with_context(
            default_move_type="in_invoice"
        ).action_create_payments()

    def _get_statements(self, move):
        """Get statements linked to `move`."""
        statements = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "=", move.id),
            ],
        )
        return statements

    def _assert_recreate_statements(self, move, statements_count):
        """Post a `move` that is Withholding Tax and has no statements,
        it creates `statements_count` statements."""
        # Arrange
        statements = self._get_statements(move)
        # pre-condition
        self.assertFalse(statements)
        self.assertTrue(move.withholding_tax)

        # Act
        move.action_post()

        # Assert
        posted_move_statements_count = len(self._get_statements(move))
        self.assertEqual(posted_move_statements_count, statements_count)

    def test_draft_recreate_statements(self):
        """Set to draft and re-confirm a move: the Tax Statements are recreated."""
        # Arrange
        move = self.invoice
        statements = self._get_statements(move)
        statements_count = len(statements)
        # pre-condition: There is a statement(s)
        self.assertTrue(statements)

        # Act
        move.button_draft()

        # Assert: The original statement is deleted and there are no statements
        self.assertFalse(statements.exists())
        self._assert_recreate_statements(move, statements_count)

    def test_cancel_recreate_statements(self):
        """Cancel and re-confirm a move: the Tax Statements are recreated."""
        # Arrange
        move = self.invoice
        statements = self._get_statements(move)
        statements_count = len(statements)
        # pre-condition: There is a statement(s)
        self.assertTrue(statements)

        # Act
        move.button_cancel()

        # Assert: The original statement is deleted and there are no statements
        self.assertFalse(statements.exists())
        self._assert_recreate_statements(move, statements_count)

    def _get_payment_wizard(self, invoice):
        wizard_action = invoice.action_register_payment()
        wizard_model = wizard_action["res_model"]
        wizard_context = wizard_action["context"]
        wizard = self.env[wizard_model].with_context(**wizard_context).create({})
        return wizard

    def test_payment_reset_net_pay_residual(self):
        """The amount to pay is reset to the Residual Net To Pay
        when amount and Journal are changed."""
        # Arrange: Pay an invoice
        invoice = self.invoice
        wizard = self._get_payment_wizard(invoice)
        user_set_amount = 20
        # pre-condition
        self.assertEqual(
            wizard.amount,
            invoice.amount_net_pay_residual,
        )
        self.assertTrue(
            invoice.withholding_tax_amount,
        )

        # Act: Change amount
        wizard.amount = user_set_amount

        # Assert: User's change is kept
        self.assertEqual(
            wizard.amount,
            user_set_amount,
        )

        # Act: Change Journal
        wizard.journal_id = self.journal_bank

        # Assert: Amount is reset to the Residual Net To Pay
        self.assertEqual(
            wizard.amount,
            invoice.amount_net_pay_residual,
        )

    def _get_records_from_action(self, action):
        context = action.get("context", dict())
        model = self.env[action["res_model"]].with_context(**context)
        domain = action.get("domain", [("id", "=", action["res_id"])])
        return model.search(domain)

    def test_no_wt_invoice_payment_write_off(self):
        """The write-off amount is only applied to withholding invoices."""
        # Arrange
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.env.ref("base.res_partner_12")
        with invoice_form.invoice_line_ids.new() as line:
            line.name = "Test line"
            line.price_unit = 1000
            line.invoice_line_tax_wt_ids.clear()
            line.invoice_line_tax_wt_ids.add(self.wt1040)
        invoice_form.withholding_tax = False
        invoice = invoice_form.save()
        invoice.action_post()

        wizard = self._get_payment_wizard(invoice)
        writeoff_account = self.account_expense1
        writeoff_amount = 1
        wizard.update(
            {
                "amount": wizard.amount - writeoff_amount,
                "payment_difference_handling": "reconcile",
                "writeoff_account_id": writeoff_account,
            }
        )
        # pre-condition
        self.assertFalse(invoice.withholding_tax)
        self.assertEqual(wizard.payment_difference, writeoff_amount)

        # Act
        payments_action = wizard.action_create_payments()

        # Assert
        payments = self._get_records_from_action(payments_action)
        payment_move = payments.move_id
        writeoff_move_line = payment_move.line_ids.filtered(
            lambda move_line, account=writeoff_account: move_line.account_id == account
        )
        self.assertEqual(writeoff_move_line.balance, writeoff_amount)

    def test_wt_after_repost(self):
        wt_statement_ids = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "=", self.invoice.id),
                ("withholding_tax_id", "=", self.wt1040.id),
            ]
        )
        self.assertEqual(len(wt_statement_ids), 1)
        ctx = {
            "active_model": "account.move",
            "active_ids": [self.invoice.id],
            "active_id": self.invoice.id,
            "default_reconciled_invoice_ids": [(4, self.invoice.id, None)],
        }
        register_payments = (
            self.env["account.payment.register"]
            .with_context(ctx)
            .create(
                {
                    "payment_date": time.strftime("%Y") + "-07-15",
                    "amount": 600,
                    "journal_id": self.journal_bank.id,
                    "payment_method_id": self.env.ref(
                        "account.account_payment_method_manual_out"
                    ).id,
                }
            )
        )
        register_payments.action_create_payments()
        partials = self.invoice._get_reconciled_invoices_partials()
        self.assertTrue({p[1] for p in partials} == {600, 150})

        self.invoice.button_draft()
        self.invoice.action_post()
        wt_statement_ids = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "=", self.invoice.id),
                ("withholding_tax_id", "=", self.wt1040.id),
            ]
        )
        self.assertEqual(len(wt_statement_ids), 1)
        debit_line_id = partials[0][2].move_id.line_ids.filtered(lambda l: l.debit)
        self.invoice.js_assign_outstanding_line(debit_line_id.id)
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 200)
        self.assertEqual(self.invoice.amount_residual, 250)
        self.assertEqual(self.invoice.state, "posted")

    def _create_bill(self, price_unit=1000.0):
        bill_model = self.env["account.move"].with_context(
            default_move_type="in_invoice",
        )
        bill_form = Form(bill_model)
        bill_form.invoice_date = fields.Date.from_string("2020-01-01")
        bill_form.partner_id = self.env.ref("base.res_partner_12")
        with bill_form.invoice_line_ids.new() as line:
            line.name = "Advice"
            line.price_unit = price_unit
            line.invoice_line_tax_wt_ids.clear()
            line.invoice_line_tax_wt_ids.add(self.wt1040)
            line.tax_ids.clear()
        bill = bill_form.save()
        bill.action_post()

        wt_statement_ids = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "=", bill.id),
                ("withholding_tax_id", "=", self.wt1040.id),
            ]
        )
        self.assertEqual(len(wt_statement_ids), 1)

        return bill

    def _get_refund(self, bill):
        refund_wizard_model = self.env["account.move.reversal"].with_context(
            active_id=bill.id,
            active_ids=bill.ids,
            active_model=bill._name,
        )
        refund_wizard_form = Form(refund_wizard_model)
        refund_wizard_form.refund_method = "cancel"
        refund_wizard = refund_wizard_form.save()
        refund_result = refund_wizard.reverse_moves()

        refund_model = refund_result.get("res_model")
        refund_id = refund_result.get("res_id")
        refund = self.env[refund_model].browse(refund_id)
        return refund

    def test_refund_wt_propagation(self):
        """
        When a Refund is created, the Withholding Tax is propagated to it.
        """
        # Arrange: Create a bill
        bill = self._create_bill()
        self.assertTrue(bill.withholding_tax)

        # Act: Create a refund
        refund = self._get_refund(bill)

        # Assert: The refund has the Withholding Tax flag enabled
        self.assertTrue(refund.withholding_tax)

    def test_refund_reconciliation_amount(self):
        """
        When a refund is created, the amount reconciled
        is the whole amount of the vendor bill.
        """
        # Arrange: Create a bill
        bill = self._create_bill()
        bill_amount = bill.amount_total

        # Act: Create a refund
        refund = self._get_refund(bill)

        # Assert: The reconciliation is for the whole bill
        reconciliation = self.env["account.partial.reconcile"].search(
            [
                ("debit_move_id", "in", refund.line_ids.ids),
                ("credit_move_id", "in", bill.line_ids.ids),
            ]
        )
        self.assertEqual(reconciliation.amount, bill_amount)

    def test_refund_wt_moves(self):
        """
        When a refund is created,
        no Withholding Tax Moves are created.
        """
        # Arrange: Create a bill
        bill = self._create_bill()

        # Act: Create a refund
        refund = self._get_refund(bill)

        # Assert: There are no Withholding Tax Moves
        reconciliation = self.env["account.partial.reconcile"].search(
            [
                ("debit_move_id", "in", refund.line_ids.ids),
                ("credit_move_id", "in", bill.line_ids.ids),
            ]
        )
        withholding_tax_moves = self.env["withholding.tax.move"].search(
            [
                ("reconcile_partial_id", "=", reconciliation.id),
            ]
        )
        self.assertFalse(withholding_tax_moves)

    def test_multi_invoice_with_payment(self):
        invoice = self._create_bill(price_unit=477.19)  # wt 95.44 net 486.73
        invoice1 = self._create_bill(price_unit=13.10)  # wt 2.62  net 13.36
        invoice2 = self._create_bill(price_unit=100.00)  # wt 20.00  net 102.00
        invoice3 = self._create_bill(price_unit=48.40)  # wt 9.68  net 49.37
        invoice4 = self._create_bill(price_unit=48.40)  # wt 9.68  net 49.37
        # we add 0.50 to the total paid for bank expenses
        invoices = invoice | invoice1 | invoice2 | invoice3 | invoice4
        ctx = {
            "active_model": "account.move",
            "active_ids": invoices.ids,
        }
        register_payments = (
            self.env["account.payment.register"]
            .with_context(ctx)
            .create(
                {
                    "payment_date": fields.Date.today().replace(month=7, day=15),
                    "amount": 486.73 + 13.36 + 102 + 49.37 + 49.37 + 0.50,
                    "group_payment": True,
                    "payment_difference_handling": "reconcile",
                    "writeoff_account_id": self.account_expense1.id,
                    "writeoff_label": "Bank expense",
                    "journal_id": self.journal_bank.id,
                    "payment_method_id": self.env.ref(
                        "account.account_payment_method_manual_out"
                    ).id,
                }
            )
        )
        payment_action = register_payments.action_create_payments()
        payment_id = payment_action["res_id"]
        payment = self.env["account.payment"].browse(payment_id)
        self.assertEqual(payment.reconciled_bill_ids.ids, invoices.ids)
        statements = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "in", invoices.ids),
            ],
        )
        self.assertEqual(len(statements), len(invoices))
        self.assertAlmostEqual(
            sum(x.tax for x in statements), 95.44 + 2.62 + 20 + 9.68 + 9.68
        )
        wh_move_ids = statements.mapped("move_ids.wt_account_move_id")
        self.assertEqual(len(wh_move_ids), len(statements))

    def test_multi_invoice_with_partial_payment(self):
        invoice = self._create_bill(price_unit=100)  # wt 20 net 80
        invoice1 = self._create_bill(price_unit=150)  # wt 30  net 120
        invoice2 = self._create_bill(price_unit=2000)  # wt 400  net 1600
        self.assertAlmostEqual(invoice.amount_net_pay_residual, 80)
        # pay partially the first invoice, it's impossible to register bank expenses
        ctx = {
            "active_model": "account.move",
            "active_ids": invoice.id,
        }
        register_payments = (
            self.env["account.payment.register"]
            .with_context(ctx)
            .create(
                {
                    "payment_date": fields.Date.today().replace(month=7, day=15),
                    "amount": 10,
                    "group_payment": True,
                    "payment_difference_handling": "open",
                    "journal_id": self.journal_bank.id,
                    "payment_method_id": self.env.ref(
                        "account.account_payment_method_manual_out"
                    ).id,
                }
            )
        )
        payment_action = register_payments.action_create_payments()
        payment_id = payment_action["res_id"]
        payment = self.env["account.payment"].browse(payment_id)
        self.assertEqual(payment.reconciled_bill_ids.ids, invoice.ids)
        self.assertAlmostEqual(invoice.amount_net_pay_residual, 70)
        # Payment the residual of the first invoice and the others, with 0.50
        # for bank expenses
        invoices = invoice | invoice1 | invoice2
        ctx = {
            "active_model": "account.move",
            "active_ids": invoices.ids,
        }
        register_payments = (
            self.env["account.payment.register"]
            .with_context(ctx)
            .create(
                {
                    "payment_date": fields.Date.today().replace(month=7, day=15),
                    "amount": 970 + 130 + 1600 + 0.50,
                    "group_payment": True,
                    "payment_difference_handling": "reconcile",
                    "writeoff_account_id": self.account_expense1.id,
                    "writeoff_label": "Bank expense",
                    "journal_id": self.journal_bank.id,
                    "payment_method_id": self.env.ref(
                        "account.account_payment_method_manual_out"
                    ).id,
                }
            )
        )
        payment_action = register_payments.action_create_payments()
        payment_id = payment_action["res_id"]
        payment = self.env["account.payment"].browse(payment_id)
        self.assertEqual(payment.reconciled_bill_ids.ids, invoices.ids)
        statements = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "in", invoices.ids),
            ],
        )
        self.assertEqual(len(statements), len(invoices))
        self.assertAlmostEqual(sum(x.tax for x in statements), 1.96 + 18.04 + 30 + 400)
        wh_move_ids = statements.mapped("move_ids.wt_account_move_id")
        self.assertEqual(len(wh_move_ids), 4)

    def test_multi_withholding_tax(self):
        """
        When there are multiple Withholding Taxes,
        the WT moves are generated correctly during payment.
        """
        # Arrange
        other_wt_form = Form(self.wt1040.copy())
        with other_wt_form.rate_ids.new() as rate:
            rate.tax = 20
        other_wt = other_wt_form.save()
        bill = self._create_bill()
        bill.button_draft()
        with Form(bill) as bill_form, bill_form.invoice_line_ids.edit(0) as line:
            line.invoice_line_tax_wt_ids.add(other_wt)
        bill.action_post()

        # Act
        self.env["account.payment.register"].with_context(
            active_model=bill._name,
            active_ids=bill.ids,
        ).create({}).action_create_payments()

        # Assert
        self.assertEqual(bill.payment_state, "paid")

    def test_no_generate_wt_move(self):
        """
        When "Do not generate move" is enabled,
        no WT move is generated upon payment.
        """
        # Arrange
        amount = 2000
        wt_amount = 500
        bill = self._create_bill(price_unit=amount)
        bill.withholding_tax_no_generate_move = True
        wt_statement = self.env["withholding.tax.statement"].search(
            [
                ("invoice_id", "=", bill.id),
            ]
        )
        # pre-condition
        self.assertTrue(bill.withholding_tax_no_generate_move)

        # Act 1: Partial payment generating no move
        self.env["account.payment.register"].with_context(
            active_model=bill._name,
            active_ids=bill.ids,
        ).create(
            {
                "amount": 100,
            }
        ).action_create_payments()

        # Assert 1: No move generated
        self.assertFalse(wt_statement.amount)
        self.assertFalse(wt_statement.move_ids)

        # Arrange 2: Enable WT Move generation
        bill.withholding_tax_no_generate_move = False

        # Act 2: Pay again
        self.env["account.payment.register"].with_context(
            active_model=bill._name,
            active_ids=bill.ids,
        ).create(
            {
                "amount": amount - 100,
            }
        ).action_create_payments()

        # Assert 2: WT move generated for all the paid amount
        wt_move = wt_statement.move_ids
        self.assertEqual(len(wt_move), 1)
        self.assertEqual(wt_statement.amount, wt_amount)
