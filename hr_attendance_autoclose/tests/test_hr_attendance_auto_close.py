# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import new_test_user, users
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

from odoo.addons.base.tests.common import BaseCommon


class TestHrAttendanceReason(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hr_attendance = cls.env["hr.attendance"]
        cls.employee = cls.env["hr.employee"].create({"name": "Employee"})
        new_test_user(cls.env, login="test-user")

    def test_employee_edit(self):
        dti = datetime.now()
        dto = datetime.now() + relativedelta(hours=7)
        att = self.hr_attendance.create(
            {
                "employee_id": self.employee.id,
                "check_in": dti.strftime(DF),
                "check_out": dto.strftime(DF),
            }
        )
        self.assertEqual(att.open_worked_hours, 7.0, "Wrong hours")
        dt = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - relativedelta(hours=15)
        att = self.hr_attendance.create(
            {"employee_id": self.employee.id, "check_in": dt.strftime(DF)}
        )
        self.hr_attendance.check_for_incomplete_attendances()
        # worked_hours are now 10 hours, because Odoo adds 1 hour to lunch, see:
        # https://github.com/odoo/odoo/commit/2eda54348de1bd42fc2a1bed94cd8b7a3ebf405d
        self.assertEqual(att.worked_hours, 10.0, "Attendance not closed")
        reason = self.env.company.hr_attendance_autoclose_reason
        reason.unlink()
        dti += relativedelta(hours=10)
        dto += relativedelta(hours=10)
        att2 = self.hr_attendance.create(
            {
                "employee_id": self.employee.id,
                "check_in": dti.strftime(DF),
                "check_out": dto.strftime(DF),
            }
        )
        self.hr_attendance.check_for_incomplete_attendances()
        self.assertFalse(att2.attendance_reason_ids)

    @users("test-user")
    def test_hr_employee_can_still_read_employee_and_hr_public_employee(self):
        """This test ensure the following comment from hr.employee model has been take
        in consideration::

            NB: Any field only available on the model hr.employee (i.e. not on the
            hr.employee.public model) should have `groups="hr.group_hr_user"` on its
            definition to avoid being prefetched when the user hasn't access to the
            hr.employee model. Indeed, the prefetch loads the data for all the fields
            that are available according to the group defined on them.
        """
        for empl in self.env["hr.employee"].search([]):
            self.assertTrue(empl.name)
