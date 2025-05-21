# Copyright 2022 Dinar Gabbasov
# Copyright 2022 Ooops404
# Copyright 2022 Cetmix
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestHrTimesheetTimeRestriction(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # We create an active employee for the current user, if he is not yet
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

        # We create a project, task and configuration
        cls.project = cls.env["project.project"].create({"name": "Test project"})
        cls.analytic_account = cls.project.analytic_account_id
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test task",
                "project_id": cls.project.id,
            }
        )
        cls.config = cls.env["res.config.settings"].create({})
        # The global restriction is disabled by default
        cls.config.use_timesheet_restriction = False
        cls.config.execute()
        cls._base_vals = {
            "task_id": cls.task.id,
            "project_id": cls.project.id,
            "account_id": cls.analytic_account.id,
            "employee_id": cls.employee.id,
            "name": "Test line",
        }

    @classmethod
    def _create_line(cls, days_offset):
        """create analytic line offset by days_offset from today"""
        vals = dict(cls._base_vals)
        vals["date"] = date.today() + timedelta(days=days_offset)
        return cls.env["account.analytic.line"].create(vals)

    def test_project_restriction_days(self):
        """With a disconnected global restriction (use_timesheet_restriction = False),
        the restriction specified at the project level is not applied
        """
        self.project.timesheet_restriction_days = 1
        # check that we can create new timesheet
        self.assertTrue(
            self._create_line(0),
            "Timesheet should be created for today",
        )
        # check that we can create new timesheet with date before
        # that current date - 1
        self.assertTrue(
            self._create_line(-2),
            "Timesheet should be created when global restriction is disabled",
        )

    def test_project_restriction_days_by_config(self):
        ConfigSettings = self.env["res.config.settings"].create({})
        ConfigSettings.timesheet_restriction_days = 1
        ConfigSettings.use_timesheet_restriction = True
        ConfigSettings.execute()
        # check that we can create new timesheet
        self.assertTrue(
            self._create_line(-1),
            "Timesheet should be created for date within allowed range",
        )
        # check that we cannot create new timesheet with date before
        # that current date - 1
        with self.assertRaises(ValidationError):
            self._create_line(-2)

    def test_project_restriction_days_ignore_config(self):
        ConfigSettings = self.env["res.config.settings"].create({})
        ConfigSettings.timesheet_restriction_days = 1
        ConfigSettings.use_timesheet_restriction = True
        ConfigSettings.execute()
        self.project.timesheet_restriction_days = 2
        self.assertTrue(self._create_line(-2))
        with self.assertRaises(ValidationError):
            self._create_line(-3)

    def test_project_restriction_days_ignore_for_timesheet_time_manager(self):
        """
        Users included in the timesheet_time_manager group ignore the dates.
        """
        group_id = self.ref(
            "hr_timesheet_time_restriction.group_timesheet_time_manager"
        )
        self.env.user.write({"groups_id": [(4, group_id)]})
        self.project.timesheet_restriction_days = 1
        # check that we can create new timesheet with date before
        # that current date - 1
        self.assertTrue(
            self._create_line(-2),
            "Timesheet should be created for timesheet time manager regardless of date",
        )

    def test_set_negative_project_restriction_days(self):
        """
        Global restriction is OFF → project field accepts negative values
        without raising and stores them as‑is.
        """
        try:
            self.project.timesheet_restriction_days = -1
        except ValidationError:
            self.project.timesheet_restriction_days = 0
        self.assertEqual(self.project.timesheet_restriction_days, -1)

    def test_set_negative_config_restriction_days(self):
        ConfigSettings = self.env["res.config.settings"].create({})
        ConfigSettings.timesheet_restriction_days = -1
        ConfigSettings._onchange_timesheet_restriction_days()
        ConfigSettings.execute()
        self.assertEqual(ConfigSettings.timesheet_restriction_days, 0)
        params = self.env["ir.config_parameter"].sudo()
        params.search(
            [
                (
                    "key",
                    "in",
                    [
                        "hr_timesheet_time_restriction.use_timesheet_restriction",
                        "hr_timesheet_time_restriction.timesheet_restriction_days",
                    ],
                )
            ]
        ).unlink()
        ConfigSettings_2 = self.env["res.config.settings"].create({})
        ConfigSettings_2.execute()
        self.assertFalse(ConfigSettings_2.use_timesheet_restriction)
        self.assertEqual(ConfigSettings_2.timesheet_restriction_days, 0)
