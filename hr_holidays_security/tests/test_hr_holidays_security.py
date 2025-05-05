# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import Form, SavepointCase

from odoo.addons.mail.tests.common import mail_new_test_user


class HrHolidaysSecurityCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        # Define some users and their employees
        # responsible 1
        # |- r1 team member A
        # responsible 2
        # |- r2 team member B
        cls.manager = cls.create_user_and_employee(
            cls, "manager", groups="hr_holidays.group_hr_holidays_manager"
        )
        cls.responsible_1 = cls.create_user_and_employee(
            cls, "responsible_1", groups="hr_holidays.group_hr_holidays_responsible"
        )
        cls.responsible_2 = cls.create_user_and_employee(
            cls, "responsible_2", groups="hr_holidays.group_hr_holidays_responsible"
        )
        cls.r1_team_member_a = cls.create_user_and_employee(
            cls, "r1_team_member_a", groups="base.group_user"
        )
        cls.r2_team_member_b = cls.create_user_and_employee(
            cls, "r2_team_member_b", groups="base.group_user"
        )
        cls.r1_team_member_a.employee_id.leave_manager_id = cls.responsible_1
        cls.r2_team_member_b.employee_id.leave_manager_id = cls.responsible_2
        cls.sick_time_off = cls.env.ref("hr_holidays.holiday_status_sl")

    def create_user_and_employee(self, login, groups):
        user = mail_new_test_user(self.env, login=login, groups=groups)
        self.env["hr.employee"].create(
            {
                "name": "Employee %s" % login,
                "user_id": user.id,
            }
        )
        return user

    def new_leave(self, user):
        return Form(self.env["hr.leave"].with_user(user.id))

    def _test_act_window_form_view(self, user, xml_id, view_id):
        res = self.env["ir.actions.act_window"].with_user(user)._for_xml_id(xml_id)
        for view, view_type in res["views"]:
            if view_type == "form":
                self.assertEqual(view, view_id)

    def test_act_window_hr_leave(self):
        leave_form = self.env.ref("hr_holidays_security.hr_leave_view_form_responsible")
        self._test_act_window_form_view(
            self.responsible_1,
            "hr_holidays.hr_leave_action_action_approve_department",
            leave_form.id,
        )
        leave_allocation_form = self.env.ref(
            "hr_holidays_security.hr_leave_allocation_view_form_manager"
        )
        self._test_act_window_form_view(
            self.responsible_1,
            "hr_holidays.hr_leave_allocation_action_approve_department",
            leave_allocation_form.id,
        )

    def test_leave_approvals_01(self):
        leave_request = self.new_leave(self.responsible_1)
        leave_request.employee_id = self.r2_team_member_b.employee_id
        leave_request.holiday_status_id = self.sick_time_off
        leave_request.request_date_from = fields.Date.today()
        leave_request.request_date_to = fields.Date.today()
        with self.assertRaises(AccessError):
            leave_request.save()

    def test_leave_approvals_02(self):
        leave_request = self.new_leave(self.responsible_2)
        leave_request.employee_id = self.r2_team_member_b.employee_id
        leave_request.holiday_status_id = self.sick_time_off
        leave_request.request_date_from = fields.Date.today()
        leave_request.request_date_to = fields.Date.today()
        leave = leave_request.save()
        leave.action_validate()
        self.assertEqual(leave.state, "validate")

    def test_leave_approvals_03(self):
        leave_request = self.new_leave(self.responsible_2)
        leave_request.employee_id = self.r2_team_member_b.employee_id
        leave_request.holiday_status_id = self.sick_time_off
        leave_request.request_date_from = fields.Date.today()
        leave_request.request_date_to = fields.Date.today()
        leave = leave_request.save()
        leave_responsible_1 = leave.with_user(self.responsible_1)
        with self.assertRaises(AccessError):
            leave_responsible_1.action_validate()

    def test_leave_approvals_04(self):
        leave_request = self.new_leave(self.responsible_2)
        leave_request.employee_id = self.r2_team_member_b.employee_id
        leave_request.holiday_status_id = self.sick_time_off
        leave_request.request_date_from = fields.Date.today()
        leave_request.request_date_to = fields.Date.today()
        leave = leave_request.save()
        leave_manager = leave.with_user(self.manager)
        leave_manager.action_validate()
        self.assertEqual(leave.state, "validate")
