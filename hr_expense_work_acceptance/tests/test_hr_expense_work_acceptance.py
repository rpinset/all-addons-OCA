# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ast

from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests.common import Form, TransactionCase


class TestHrExpensePayToVendor(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wa_model = cls.env["work.acceptance"]
        cls.vendor = cls.env["res.partner"].create({"name": "Test Vendor"})
        cls.payment_obj = cls.env["account.payment"]
        cls.account_payment_register = cls.env["account.payment.register"]
        cls.payment_journal = cls.env["account.journal"].search(
            [("type", "in", ["cash", "bank"])], limit=1
        )

        cls.main_company = cls.env.ref("base.main_company")
        # Enable and Config WA
        cls.env["res.config.settings"].create(
            {"group_wa_accepted_before_inv": True, "group_enable_wa_on_exp": True}
        ).execute()

        # Ensure product and UoM are set correctly to avoid NOT NULL violations
        cls.product_product = cls.env.ref("product.product_product_6")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        # Fix: Use write instead of assignment to persist changes to DB
        cls.product_product.write(
            {
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )

        cls.expense_journal = cls.env["account.journal"].create(
            {
                "name": "Purchase Journal - Test",
                "code": "HRTPJ",
                "type": "purchase",
                "company_id": cls.main_company.id,
            }
        )
        cls.expense_sheet = cls.env["hr.expense.sheet"].create(
            {
                "employee_id": cls.env.ref("hr.employee_admin").id,
                "name": "Expense test",
                "journal_id": cls.expense_journal.id,
            }
        )
        cls.expenses = cls.env["hr.expense"].create(
            [
                {
                    "name": "Expense Line 1",
                    "employee_id": cls.env.ref("hr.employee_admin").id,
                    "product_id": cls.product_product.id,
                    "product_uom_id": cls.uom_unit.id,
                    "unit_amount": 1,
                    "quantity": 10,
                    "sheet_id": cls.expense_sheet.id,
                },
                {
                    "name": "Expense Line 1",
                    "employee_id": cls.env.ref("hr.employee_admin").id,
                    "product_id": cls.product_product.id,
                    "product_uom_id": cls.uom_unit.id,
                    "unit_amount": 1,
                    "quantity": 20,
                    "sheet_id": cls.expense_sheet.id,
                },
            ]
        )

    def _create_work_acceptance(self, expense_sheet):
        wa_vals = {
            "partner_id": self.vendor.id,
            "responsible_id": self.env.user.id,
            "date_due": fields.Datetime.now(),
            "date_receive": fields.Datetime.now(),
            "company_id": self.main_company.id,
            "sheet_id": expense_sheet.id,
            "wa_line_ids": [],
        }
        for expense in expense_sheet.expense_line_ids:
            wa_vals["wa_line_ids"].append(
                Command.create(
                    {
                        "expense_id": expense.id,
                        "product_id": expense.product_id.id,
                        "name": expense.name,
                        "product_uom": expense.product_uom_id.id,
                        "product_qty": expense.quantity,
                        "price_unit": expense.unit_amount,
                    }
                )
            )
        return self.wa_model.create(wa_vals)

    def test_01_hr_expense_work_acceptance(self):
        """When expense is set to pay to vendor, I expect,
        - After post journal entries, all journal items will use partner_id = vendor
        - After make payment, all journal items will use partner_id = vendor
        """
        # No WA
        self.assertEqual(len(self.expense_sheet.wa_ids), 0)
        self.assertEqual(self.expense_sheet.wa_count, 0)
        self.assertEqual(self.expense_sheet.wa_accepted, 0)
        for expense in self.expenses:
            self.assertEqual(expense.qty_accepted, 0)
        # Create 2 WA
        res = self.expense_sheet.with_context(create_wa=True).action_view_wa()
        # Verify context via Form but use helper to create
        f = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(f.sheet_id, self.expense_sheet)

        wa_ids = work_acceptance = self._create_work_acceptance(self.expense_sheet)
        self.assertEqual(work_acceptance.state, "draft")
        work_acceptance.button_cancel()
        self.assertEqual(work_acceptance.state, "cancel")
        res = self.expense_sheet.with_context(create_wa=True).action_view_wa()
        work_acceptance = self._create_work_acceptance(self.expense_sheet)
        wa_ids += work_acceptance

        # Invalidate cache to ensure compute fields see the new lines
        self.expenses.invalidate_recordset()
        self.expense_sheet.invalidate_recordset()

        # Check smart button link to 2 WA
        self.assertEqual(len(self.expense_sheet.wa_ids), 2)
        res = self.expense_sheet.with_context().action_view_wa()
        domain = ast.literal_eval(res.get("domain", False))
        self.assertEqual(domain[0][2], wa_ids.ids)
        self.assertEqual(self.expense_sheet.wa_count, 2)
        self.assertEqual(self.expense_sheet.wa_accepted, 0)  # wa not accept
        # WA Accepted
        work_acceptance.button_accept()
        for expense in self.expenses:
            self.assertEqual(expense.qty_accepted, expense.quantity)
        self.assertEqual(len(self.expense_sheet.wa_ids), 2)
        self.assertEqual(self.expense_sheet.wa_count, 2)
        # recompute, expense sheet should accepted wa
        self.expense_sheet._compute_wa_accepted()
        self.assertEqual(self.expense_sheet.wa_accepted, 1)

    def test_02_hr_expense_required_wa(self):
        """Test Config WA"""
        self.expense_sheet.action_submit_sheet()
        self.expense_sheet.approve_expense_sheets()
        # Test post journal entry without WA
        with self.assertRaises(UserError):
            self.expense_sheet.action_sheet_move_create()
        # Test create wa but not accepted
        res = self.expense_sheet.with_context(create_wa=True).action_view_wa()
        work_acceptance = self._create_work_acceptance(self.expense_sheet)
        res = self.expense_sheet.with_context().action_view_wa()
        self.assertEqual(res["res_id"], self.expense_sheet.wa_ids.id)
        with self.assertRaises(UserError):
            self.expense_sheet.action_sheet_move_create()
        work_acceptance.button_accept()
        self.expense_sheet.action_sheet_move_create()
