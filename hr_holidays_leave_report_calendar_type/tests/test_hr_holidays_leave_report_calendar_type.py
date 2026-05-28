# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLeaveReportCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "Test Holiday Status",
                "requires_allocation": "no",
            }
        )

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee for Leave Report",
            }
        )

        cls.leave = cls.env["hr.leave"].create(
            {
                "name": "Test Leave",
                "employee_id": cls.employee.id,
                "holiday_status_id": cls.leave_type.id,
                "date_from": "2026-04-01 08:00:00",
                "date_to": "2026-04-02 17:00:00",
            }
        )

        cls.leave.action_validate()
        cls.env.flush_all()

    def test_field_exists(self):
        self.assertIn(
            "holiday_status_id",
            self.env["hr.leave.report.calendar"]._fields,
            "The 'holiday_status_id' field is not found in the Odoo model.",
        )

    def test_field_assigned_properly(self):
        calendar_record = self.env["hr.leave.report.calendar"].browse(self.leave.id)

        self.assertEqual(
            calendar_record.holiday_status_id,
            self.leave.holiday_status_id,
            "The holiday_status_id is not properly assigned in the calendar report.",
        )

    def test_search_holiday_status_id(self):
        calendars = self.env["hr.leave.report.calendar"].search(
            [("holiday_status_id", "=", self.leave_type.id)]
        )
        self.assertIn(self.leave.id, calendars.ids)
