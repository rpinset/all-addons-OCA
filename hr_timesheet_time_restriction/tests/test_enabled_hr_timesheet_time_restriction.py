# Copyright 2022 Dinar Gabbasov
# Copyright 2022 Ooops404
# Copyright 2022 Cetmix
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import common

_logger = logging.getLogger(__name__)


class TestHrTimesheetTimeRestriction(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test project",
                "use_timesheet_restriction": True,
            }
        )
        cls.analytic_account = cls.project.analytic_account_id
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test task",
                "project_id": cls.project.id,
            }
        )
        cls.config = cls.env["res.config.settings"].create({})
        cls.config.use_timesheet_restriction = True
        cls.config.execute()
        # Create or find an active employee for the current user
        employee = cls.env["hr.employee"].search(
            [("user_id", "=", cls.env.uid)], limit=1
        )
        if not employee:
            employee = cls.env["hr.employee"].create(
                {
                    "name": cls.env.user.name or "Test Employee",
                    "user_id": cls.env.uid,
                    "active": True,
                    "company_id": cls.env.company.id,
                }
            )
        cls.employee = employee
        cls._base_vals = {
            "task_id": cls.task.id,
            "project_id": cls.project.id,
            "account_id": cls.analytic_account.id,
            "employee_id": cls.employee.id,
            "name": "Test line",
        }

    def _create_line(self, days_offset):
        vals = dict(self._base_vals)
        vals["date"] = date.today() + timedelta(days=days_offset)
        return self.env["account.analytic.line"].create(vals)

    def test_project_restriction_days(self):
        self.project.timesheet_restriction_days = 1
        # check that we can create new timesheet
        line = self._create_line(0)
        self.assertTrue(line)

        with self.assertRaises(ValidationError):
            self._create_line(-2)

    def test_project_restriction_days_by_config(self):
        self.config.timesheet_restriction_days = 1
        self.config.execute()

        # Yesterday (offset -1): allowed, so line should be created
        line = self._create_line(-1)
        self.assertTrue(line)

        # Two days ago (offset -2): should raise
        with self.assertRaises(ValidationError):
            self._create_line(-2)

    def test_project_restriction_days_ignore_config(self):
        # Global = 1, but project override = 2
        self.config.timesheet_restriction_days = 1
        self.config.execute()
        self.project.timesheet_restriction_days = 2

        # Two days ago (offset -2): allowed
        line = self._create_line(-2)
        self.assertTrue(line)

        # Three days ago (offset -3): should raise
        with self.assertRaises(ValidationError):
            self._create_line(-3)

    def test_project_restriction_days_ignore_for_timesheet_time_manager(self):
        group = self.ref("hr_timesheet_time_restriction.group_timesheet_time_manager")
        self.env.user.write({"groups_id": [(4, group)]})
        self.project.timesheet_restriction_days = 1
        # check that we can create new timesheet with date before
        # that current date - 1
        line = self._create_line(-2)
        self.assertTrue(line, "Timesheet should be created")

    def test_set_negative_project_restriction_days(self):
        with self.assertRaises(ValidationError):
            self.project.timesheet_restriction_days = -1
        self.assertEqual(self.project.timesheet_restriction_days, 0)

    def test_set_negative_config_restriction_days(self):
        ConfigSettings = self.env["res.config.settings"].create({})
        ConfigSettings.timesheet_restriction_days = -1
        ConfigSettings._onchange_timesheet_restriction_days()
        ConfigSettings.execute()
        self.assertEqual(ConfigSettings.timesheet_restriction_days, 0)

    def test_global_restriction_without_project_flag(self):
        self.project.use_timesheet_restriction = False
        self.config.timesheet_restriction_days = 1
        self.config.execute()
        # Yesterday (–1) it is allowed, the day before yesterday (–2)
        # it is prohibited
        self.assertTrue(self._create_line(-1))
        with self.assertRaises(ValidationError):
            self._create_line(-2)

    def test_zero_day_restriction_past_and_future(self):
        self.config.timesheet_restriction_days = 0
        self.config.execute()
        # yesterday
        with self.assertRaises(ValidationError):
            self._create_line(-1)
        # tomorrow
        with self.assertRaises(ValidationError):
            self._create_line(1)

    def test_validate_negative_allowed_days(self):
        line = self._create_line(0)
        with self.assertRaises(ValidationError):
            line._validate_timesheet_date(line, -5)

    def test_validate_invalid_date_value(self):
        vals = dict(self._base_vals)
        vals["date"] = False
        dummy = self.env["account.analytic.line"].new(vals)

        with self.assertRaises(ValidationError):
            dummy._validate_timesheet_date(dummy, 1)
