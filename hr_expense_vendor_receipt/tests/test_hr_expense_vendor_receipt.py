from odoo import Command
from odoo.exceptions import MissingError
from odoo.tests import tagged

from odoo.addons.hr_expense.tests.common import TestExpenseCommon


@tagged("-at_install", "post_install")
class TestHrExpenseEmployeePayment(TestExpenseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.exp_emp_partner = cls.expense_employee.work_contact_id
        cls.exp_emp_partner_bank_account = cls.env["res.partner.bank"].create(
            {
                "acc_number": "1112223334",
                "partner_id": cls.exp_emp_partner.id,
                "acc_type": "bank",
            }
        )

    def test_create_expense_sheet_with_receipt_journal(self):
        journal = self.env["account.journal"].create(
            {
                "name": "Receipts",
                "code": "ref",
                "type": "purchase",
                "company_id": self.company_data["company"].id,
                "receipts": True,
            }
        )
        expense_sheet = self.create_expense_report(
            {
                "name": "SHEET TEST",
                "employee_journal_id": journal.id,
                "journal_id": journal.id,
                "expense_line_ids": [
                    Command.create(
                        {
                            "name": "EXPENSE 1",
                            "payment_mode": "own_account",
                            "employee_id": self.expense_employee.id,
                            "product_id": self.product_c.id,
                            "total_amount": 1000.00,
                        }
                    )
                ],
            }
        )
        expense_sheet.action_submit_sheet()
        expense_sheet.action_approve_expense_sheets()
        expense_sheet.action_sheet_move_post()
        self.assertEqual(
            expense_sheet.account_move_ids[0].journal_id,
            journal,
            (
                f"The journal must be {journal.display_name}, "
                f"but is {expense_sheet.account_move_ids[0].journal_id.display_name}"
            ),
        )
        self.assertEqual(
            "in_receipt",
            expense_sheet.account_move_ids[0].move_type,
            (
                "The move_type must be in_receipt, but is "
                f"{expense_sheet.account_move_ids[0].move_type}"
            ),
        )
        move_id = expense_sheet.account_move_ids[0]
        expense_sheet.action_reset_expense_sheets()
        with self.assertRaises(MissingError):
            # move this is already deleted
            self.assertFalse(move_id.state, "posted")
