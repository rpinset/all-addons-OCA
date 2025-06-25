# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import tests

from odoo.addons.account.tests.common import TestAccountReconciliationCommon


@tests.tagged("post_install", "-at_install")
class TestReconciliationWidget(TestAccountReconciliationCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.bank_statement_model = cls.env["account.bank.statement"]
        cls.bank_journal = cls.company_data["default_journal_bank"]
        cls.reconciliation_widget = cls.env["account.reconciliation.widget"]

    def test_account_excluded(self):
        """Configure an account to be excluded in the bank journal.
        In the bank statement, the lines of that account
        are not proposed for reconciliation.
        """
        # Arrange
        invoice = self.create_invoice(currency_id=self.currency_euro_id)
        receivable_account = invoice.line_ids.filtered(
            lambda line: line.account_id.internal_type == "receivable"
        ).account_id
        excluded_account = receivable_account.copy(
            default={
                "name": "Test excluded account",
                "code": "TESTEXCLACC",
            }
        )

        bank_journal = self.bank_journal_euro
        bank_journal.account_reconcile_exclude_account_ids = excluded_account

        excluded_invoice = self.create_invoice(currency_id=self.currency_euro_id)
        excluded_invoice.line_ids.filtered(
            lambda line: line.account_id.internal_type == "receivable"
        ).account_id = excluded_account
        bank_statement = self.bank_statement_model.create(
            {
                "name": "Test bank statement",
                "journal_id": bank_journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "payment_ref": "Payment for %s" % invoice.name,
                            "amount": 10,
                        },
                    )
                ],
            }
        )

        # Act
        move_lines_list = (
            self.reconciliation_widget.get_move_lines_for_bank_statement_line(
                bank_statement.line_ids.id,
                mode="rp",
            )
        )

        # Assert
        move_lines_ids = [ml["id"] for ml in move_lines_list]
        move_lines = self.env["account.move.line"].browse(move_lines_ids)
        self.assertIn(invoice, move_lines.move_id)
        self.assertNotIn(excluded_invoice, move_lines.move_id)
