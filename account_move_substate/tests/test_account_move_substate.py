# Copyright 2023 bosd (<bosd>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import Command
from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestAccountMoveSubstate(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_move_model = cls.env["account.move"]
        cls.account_model = cls.env["account.account"]

        cls.substate_type = cls.env.ref(
            "account_move_substate.base_substate_type_account_move"
        )
        cls.target_state_draft = cls.env.ref(
            "account_move_substate.target_state_value_draft"
        )
        cls.target_state_posted = cls.env.ref(
            "account_move_substate.target_state_value_posted"
        )
        cls.mail_template = cls.env.ref(
            "account_move_substate.mail_template_data_account_move_substate_verified"
        )
        cls.substate_to_verify = cls.env["base.substate"].create(
            {
                "name": "To Verify",
                "sequence": -30,
                "target_state_value_id": cls.target_state_draft.id,
            }
        )
        cls.substate_checked = cls.env["base.substate"].create(
            {
                "name": "Checked",
                "sequence": -20,
                "target_state_value_id": cls.target_state_draft.id,
            }
        )
        cls.substate_verified = cls.env["base.substate"].create(
            {
                "name": "Verified",
                "sequence": -10,
                "target_state_value_id": cls.target_state_posted.id,
                "mail_template_id": cls.mail_template.id,
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "testpartner@example.com",
                "property_account_receivable_id": cls._create_account(
                    "Test Receivable", "TREC", "asset_receivable"
                ).id,
                "property_account_payable_id": cls._create_account(
                    "Test Payable", "TPAY", "liability_payable"
                ).id,
            }
        )
        cls.revenue_account = cls._create_account("Test Revenue", "TREV", "income")
        cls.expense_account = cls._create_account("Test Expense", "TEXP", "expense")
        cls.invoice = cls._create_test_invoice()
        cls.high_value_invoice = cls._create_test_invoice(price_unit=450)
        cls.journal_entry = cls.account_move_model.create(
            {
                "move_type": "entry",
                "date": "2019-01-01",
                "partner_id": cls.partner.id,
                "line_ids": [
                    Command.create(
                        {
                            "name": "Debit line",
                            "debit": 100,
                            "credit": 0,
                            "account_id": cls.expense_account.id,
                            "partner_id": cls.partner.id,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Credit line",
                            "debit": 0,
                            "credit": 100,
                            "account_id": cls.revenue_account.id,
                            "partner_id": cls.partner.id,
                        }
                    ),
                ],
            }
        )

    @classmethod
    def _create_account(cls, name, code, account_type):
        return cls.account_model.create(
            {
                "name": name,
                "code": code,
                "account_type": account_type,
            }
        )

    @classmethod
    def _create_test_invoice(cls, price_unit=100):
        return cls.account_move_model.create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Test product",
                            "quantity": 1,
                            "price_unit": price_unit,
                            "account_id": cls.revenue_account.id,
                        }
                    )
                ],
            }
        )

    def test_account_move_substate_basic(self):
        """Test basic substate functionality with invoice"""
        invoice = self.high_value_invoice
        self.assertEqual(invoice.state, "draft")
        with self.assertRaises(ValidationError):
            invoice.substate_id = self.substate_verified
        invoice.substate_id = self.substate_to_verify.id
        self.assertEqual(invoice.substate_id, self.substate_to_verify)
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.substate_id, self.substate_verified)
        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        self.assertFalse(invoice.substate_id)

    def test_account_move_substate_with_different_states(self):
        """Test substate assignment with different account move states"""
        move = self.journal_entry
        move.substate_id = self.substate_to_verify.id
        self.assertEqual(move.substate_id, self.substate_to_verify)
        move.action_post()
        self.assertEqual(move.state, "posted")
        self.assertEqual(move.substate_id, self.substate_verified)

    def test_substate_validation_on_state_change(self):
        """Test that substate validation occurs properly during state changes"""
        move = self.invoice
        move.substate_id = self.substate_to_verify.id
        self.assertEqual(move.substate_id, self.substate_to_verify)
        with self.assertRaises(ValidationError):
            move.substate_id = self.substate_verified.id

    def test_substate_clearance_on_cancellation(self):
        """Test that substate is cleared when moving to cancel state"""
        move = self.invoice
        move.action_post()
        self.assertEqual(move.substate_id, self.substate_verified)
        move.button_cancel()
        self.assertEqual(move.state, "cancel")
        self.assertFalse(move.substate_id)

    def test_multiple_substate_assignments(self):
        """Test assigning different substates during the lifecycle of an account move"""
        move = self.invoice
        move.substate_id = self.substate_to_verify.id
        self.assertEqual(move.substate_id, self.substate_to_verify)
        move.substate_id = self.substate_checked.id
        self.assertEqual(move.substate_id, self.substate_checked)
        move.action_post()
        self.assertEqual(move.state, "posted")
        self.assertEqual(move.substate_id, self.substate_verified)
