# Copyright 2025 APSL-Nagarro Bernat Obrador Mesquida (<https://apsl.tech/es/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestAccountInvoiceAutoSpread(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.a_expense = cls.env["account.account"].create(
            {
                "code": "X2120",
                "name": "Expenses - (test)",
                "account_type": "expense",
            }
        )

        cls.expenses_journal = cls.env["account.journal"].create(
            {
                "name": "Vendor Bills - Test",
                "code": "TEXJ",
                "type": "purchase",
                "default_account_id": cls.a_expense.id,
                "refund_sequence": True,
            }
        )

        cls.account_payable = cls.env["account.account"].create(
            {
                "name": "Test account payable",
                "code": "321spread",
                "account_type": "income_other",
                "reconcile": True,
            }
        )

    def test_01_auto_spread_sheet_from_entry(self):
        self.env["account.spread.template"].create(
            {
                "name": "test",
                "spread_type": "purchase",
                "period_number": 5,
                "period_type": "month",
                "spread_account_id": self.account_payable.id,
                "spread_journal_id": self.expenses_journal.id,
                "auto_spread": True,
                "auto_spread_ids": [(0, 0, {"account_id": self.a_expense.id})],
            }
        )

        move = self.env["account.move"].create(
            {
                "name": "test",
                "move_type": "entry",
                "journal_id": self.expenses_journal.id,
                "date": "2025-01-01",
                "line_ids": [
                    (0, 0, {"account_id": self.a_expense.id, "debit": 100}),
                    (0, 0, {"account_id": self.account_payable.id, "credit": 100}),
                ],
            }
        )
        move.action_post()

        self.assertTrue(move.line_ids[0].spread_id)
        self.assertFalse(move.line_ids[1].spread_id)

        spread = move.line_ids[0].spread_id
        spread.create_all_moves()
        self.assertTrue(spread.line_ids[0].move_id.is_created_from_spread)

    def test_02_no_auto_spread_sheet_from_entry(self):
        self.env["account.spread.template"].create(
            {
                "name": "test",
                "spread_type": "purchase",
                "period_number": 5,
                "period_type": "month",
                "spread_account_id": self.account_payable.id,
                "spread_journal_id": self.expenses_journal.id,
                "auto_spread": False,
                "auto_spread_ids": [(0, 0, {"account_id": self.a_expense.id})],
            }
        )

        move = self.env["account.move"].create(
            {
                "name": "test",
                "move_type": "entry",
                "journal_id": self.expenses_journal.id,
                "date": "2025-01-01",
                "line_ids": [
                    (0, 0, {"account_id": self.a_expense.id, "debit": 100}),
                    (0, 0, {"account_id": self.account_payable.id, "credit": 100}),
                ],
            }
        )
        move.action_post()

        self.assertFalse(move.line_ids[0].spread_id)
        self.assertFalse(move.line_ids[1].spread_id)
