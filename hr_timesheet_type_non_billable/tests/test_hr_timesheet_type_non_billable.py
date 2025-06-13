from odoo.tests.common import TransactionCase


class TestHrTimesheetTypeNonBillable(TransactionCase):
    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "allocated_hours": 50,
            }
        )
        cls.billable_type = cls.env["project.time.type"].create(
            {
                "name": "Billable",
                "non_billable": False,
            }
        )
        cls.non_billable_type = cls.env["project.time.type"].create(
            {
                "name": "Non-Billable",
                "non_billable": True,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
                "planned_hours": 10,
            }
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "project_id": cls.project.id,
                "planned_hours": 8,
                "description": "Test Helpdesk Ticket",
            }
        )

    def test_non_billable_timesheet(self):
        self.env["account.analytic.line"].create(
            {
                "employee_id": self.employee.id,
                "name": "Non-Billable Timesheet",
                "project_id": self.project.id,
                "task_id": self.task.id,
                "unit_amount": 2,
                "time_type_id": self.non_billable_type.id,
            }
        )

        self.env["account.analytic.line"].create(
            {
                "employee_id": self.employee.id,
                "name": "Billable Timesheet",
                "project_id": self.project.id,
                "task_id": self.task.id,
                "unit_amount": 3,
                "time_type_id": self.billable_type.id,
            }
        )

        self.assertEqual(
            self.task.remaining_hours,
            7,
            "Task remaining hours should exclude non-billable timesheets.",
        )

        self.assertEqual(
            self.task.effective_hours,
            3,
            "Task effective hours should only include billable timesheets.",
        )

        self.assertEqual(
            self.project.remaining_hours,
            47,
            "Project remaining hours should exclude non-billable timesheets.",
        )

    def test_helpdesk_ticket_non_billable_timesheet(self):
        self.env["account.analytic.line"].create(
            {
                "employee_id": self.employee.id,
                "name": "Non-Billable Helpdesk Timesheet",
                "project_id": self.project.id,
                "ticket_id": self.ticket.id,
                "unit_amount": 1,
                "time_type_id": self.non_billable_type.id,
            }
        )

        self.env["account.analytic.line"].create(
            {
                "employee_id": self.employee.id,
                "name": "Billable Helpdesk Timesheet",
                "project_id": self.project.id,
                "ticket_id": self.ticket.id,
                "unit_amount": 2,
                "time_type_id": self.billable_type.id,
            }
        )

        self.assertEqual(
            self.ticket.total_hours,
            2,
            "Helpdesk ticket total hours should exclude non-billable timesheets.",
        )

        self.assertEqual(
            self.ticket.remaining_hours,
            6,
            "Helpdesk ticket effective hours should only include billable timesheets.",
        )
