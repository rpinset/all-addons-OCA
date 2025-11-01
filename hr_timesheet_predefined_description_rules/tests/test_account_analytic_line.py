# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestAccountAnalyticLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AccountAnalyticAccount = cls.env["account.analytic.account"]
        cls.PredefinedDescription = cls.env["timesheet.predefined.description"]
        cls.AccountAnalyticLine = cls.env["account.analytic.line"]
        cls.AnalyticPlan = cls.env["account.analytic.plan"]

        cls.plan = cls.AnalyticPlan.create({"name": "Test Plan"})
        cls.analytic_account = cls.AccountAnalyticAccount.create(
            {"name": "Test Account", "plan_id": cls.plan.id}
        )
        cls.predef_fixed = cls.PredefinedDescription.create(
            {
                "name": "Fixed",
                "allow_free_text": False,
            }
        )
        cls.predef_free = cls.PredefinedDescription.create(
            {
                "name": "Free",
                "allow_free_text": True,
                "append_free_text_to_name": True,
                "free_text_required": False,
            }
        )
        cls.predef_required = cls.PredefinedDescription.create(
            {
                "name": "Required",
                "allow_free_text": True,
                "append_free_text_to_name": True,
                "free_text_required": True,
            }
        )
        cls.Task = cls.env["project.task"]
        cls.task = cls.Task.create(
            {
                "name": "Test Task",
                "project_id": cls.env["project.project"]
                .create({"name": "Test Project"})
                .id,
            }
        )
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "user_id": cls.env.user.id,
                "company_id": cls.env.user.company_id.id,
            }
        )

    def _create_line(self):
        return self.AccountAnalyticLine.create(
            {
                "name": "Original Description",
                "account_id": self.analytic_account.id,
                "task_id": self.task.id,
                "employee_id": self.employee.id,
            }
        )

    def test_fixed_description_write(self):
        line = self._create_line()
        line.write(
            {
                "predefined_description_id": self.predef_fixed.id,
                "free_text": "Should be ignored",
            }
        )
        line.invalidate_cache()
        self.assertEqual(line.name, "Fixed")

    def test_free_text_append_write(self):
        line = self._create_line()
        line.write(
            {
                "predefined_description_id": self.predef_free.id,
                "free_text": "Additional Info",
            }
        )
        line.invalidate_cache()
        self.assertEqual(line.name, "Free. Additional Info")
        self.assertEqual(line.free_text, "Additional Info")

    def test_free_text_required_write(self):
        line = self._create_line()
        with self.assertRaises(UserError):
            line.write(
                {
                    "predefined_description_id": self.predef_required.id,
                    "free_text": "",
                }
            )
        line.write(
            {
                "predefined_description_id": self.predef_required.id,
                "free_text": "Extra Info",
            }
        )
        line.invalidate_cache()
        self.assertEqual(line.name, "Required. Extra Info")
        self.assertEqual(line.free_text, "Extra Info")
