# Copyright 2026 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.base.tests.common import BaseCommon


class TestAccountAnalyticLine(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

        # Analytic plan and account
        cls.analytic_plan = cls.env["account.analytic.plan"].create(
            {
                "name": "Test Plan",
            }
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Test Analytic Account",
                "plan_id": cls.analytic_plan.id,
            }
        )
        # Project linked to analytic account
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "analytic_account_id": cls.analytic_account.id,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
                "partner_id": cls.partner.id,
            }
        )
        # Product for timesheets
        cls.product = cls.env["product.product"].create(
            {
                "name": "Timesheet Product",
                "type": "service",
                "uom_id": cls.env.ref("uom.product_uom_hour").id,
            }
        )
        # Employee with billable product
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "timesheet_billable_product_id": cls.product.id,
            }
        )

    def _create_analytic_line(
        self,
        name,
        unit_amount,
        billable=True,
        employee=None,
        project=None,
        task=None,
        account=None,
    ):
        return self.env["account.analytic.line"].create(
            {
                "name": name,
                "account_id": (account or self.analytic_account).id,
                "employee_id": (employee or self.employee).id,
                "project_id": (project or self.project).id,
                "task_id": (task or self.task).id,
                "unit_amount": unit_amount,
                "is_billable": billable,
            }
        )

    def test_create_sale_order_basic(self):
        """A sales order is created for billable analytic lines."""
        line = self._create_analytic_line("Work done", 3.0)
        line.create_sale_orders()
        sale_order = self.env["sale.order"].search(
            [("analytic_account_id", "=", self.analytic_account.id)]
        )
        self.assertEqual(len(sale_order), 1)
        self.assertEqual(sale_order.partner_id, self.task.partner_id)
        self.assertEqual(sale_order.analytic_account_id, self.analytic_account)

    def test_non_billable_lines_excluded(self):
        """Non-billable lines are not included in any sales order."""
        self._create_analytic_line("Non billable work", 2.0, billable=False)
        self._create_analytic_line("Billable work", 1.0, billable=True)
        lines = self.env["account.analytic.line"].search(
            [("account_id", "=", self.analytic_account.id)]
        )
        lines.create_sale_orders()
        sale_order = self.env["sale.order"].search(
            [("analytic_account_id", "=", self.analytic_account.id)]
        )
        self.assertEqual(len(sale_order), 1)
        self.assertAlmostEqual(sale_order.order_line[0].product_uom_qty, 1.0)

    def test_unit_amount_summed_per_employee_project_task(self):
        """Hours are summed correctly for the same employee/project/task."""
        line1 = self._create_analytic_line("Morning session", 2.5)
        line2 = self._create_analytic_line("Afternoon session", 1.5)
        (line1 | line2).create_sale_orders()
        sale_order = self.env["sale.order"].search(
            [("analytic_account_id", "=", self.analytic_account.id)]
        )
        self.assertEqual(len(sale_order.order_line), 1)
        self.assertAlmostEqual(sale_order.order_line[0].product_uom_qty, 4.0)

    def test_name_joined_from_analytic_lines(self):
        """Order line name is a newline-joined concatenation of analytic line names."""
        line1 = self._create_analytic_line("Task A description", 1.0)
        line2 = self._create_analytic_line("Task B description", 1.0)
        (line1 | line2).create_sale_orders()
        sale_order = self.env["sale.order"].search(
            [("analytic_account_id", "=", self.analytic_account.id)]
        )
        expected_name = "Test Task:\nTask A description\nTask B description"
        self.assertEqual(sale_order.order_line[0].name, expected_name)

    def test_separate_order_lines_per_employee(self):
        """Different employees generate separate order lines."""
        product2 = self.env["product.product"].create(
            {
                "name": "Timesheet Product 2",
                "type": "service",
                "uom_id": self.env.ref("uom.product_uom_hour").id,
            }
        )
        employee2 = self.env["hr.employee"].create(
            {
                "name": "Employee 2",
                "timesheet_billable_product_id": product2.id,
            }
        )
        self._create_analytic_line("Work by employee 1", 2.0)
        self._create_analytic_line("Work by employee 2", 3.0, employee=employee2)
        lines = self.env["account.analytic.line"].search(
            [("account_id", "=", self.analytic_account.id)]
        )
        lines.create_sale_orders()
        sale_order = self.env["sale.order"].search(
            [("analytic_account_id", "=", self.analytic_account.id)]
        )
        self.assertEqual(len(sale_order.order_line), 2)

    def test_sale_order_line_id_linked(self):
        """Analytic lines are linked back to their sales order line."""
        line = self._create_analytic_line("Work done", 2.0)
        line.create_sale_orders()
        self.assertTrue(line.sale_order_line_id)
        self.assertEqual(
            line.sale_order_line_id.product_id,
            self.employee.timesheet_billable_product_id,
        )

    def test_separate_sale_orders_per_analytic_account(self):
        """Each analytic account gets its own sales order."""
        partner2 = self.env["res.partner"].create({"name": "Partner 2"})
        account2 = self.env["account.analytic.account"].create(
            {
                "name": "Analytic Account 2",
                "plan_id": self.analytic_plan.id,
            }
        )
        project2 = self.env["project.project"].create(
            {
                "name": "Project 2",
                "analytic_account_id": account2.id,
            }
        )
        task2 = self.env["project.task"].create(
            {
                "name": "Task in project 2",
                "project_id": project2.id,
                "partner_id": partner2.id,
            }
        )
        self._create_analytic_line("Work account 1", 1.0)
        self._create_analytic_line(
            "Work account 2", 1.0, account=account2, project=project2, task=task2
        )
        lines = self.env["account.analytic.line"].search(
            [("account_id", "in", [self.analytic_account.id, account2.id])]
        )
        lines.create_sale_orders()
        orders = self.env["sale.order"].search(
            [("analytic_account_id", "in", [self.analytic_account.id, account2.id])]
        )
        self.assertEqual(len(orders), 2)
