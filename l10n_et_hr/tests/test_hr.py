# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.tests.common import Form, TransactionCase


class RecruitmentTestCase(TransactionCase):
    def setUp(self):
        super().setUp()

        self.Employee = self.env["hr.employee"]
        self.ee = self.Employee.create(
            {
                "name": "Mike",
                "ethiopic_name": "ሚኪ",
            }
        )
        self.dept = self.env["hr.department"].create(
            {
                "name": "Admin",
                "ethiopic_name": "አስተዳደር",
            }
        )
        self.job = self.env["hr.job"].create(
            {
                "name": "somejob",
                "ethiopic_name": "ቦዘኔ",
            }
        )

    def test_name_get(self):

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_employee_name"
        )
        self.assertEqual(
            use_ethiopic_name, False, "By default the ethiopic name knob is OFF"
        )

        self.assertEqual(
            self.ee.display_name,
            "Mike",
            "By default the content of the name field is displayed",
        )

    def test_name_get_ethiopic(self):

        self.env["ir.config_parameter"].set_param(
            "l10n_et_hr.use_ethiopic_employee_name", True
        )

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_employee_name"
        )
        self.assertTrue(use_ethiopic_name, "I turned the ethiopic name knob ON")

        self.assertEqual(
            self.ee.display_name,
            "ሚኪ",
            "The content of 'ethiopic_name' field is displayed",
        )

    def test_onchange_dob(self):

        f = Form(self.Employee)
        f.name = "Test"
        f.use_ethiopic_dob = (True,)
        f.etcal_dob_year = "2000"
        f.etcal_dob_month = "1"
        f.etcal_dob_day = "1"

        self.assertEqual(
            f.birthday,
            date(2007, 9, 12),
            "When the ethiopic dob was set the 'birthday' field was modified",
        )

    def test_department_name_get(self):

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_department"
        )
        self.assertEqual(
            use_ethiopic_name,
            False,
            "By default the department ethiopic name knob is OFF",
        )

        self.assertEqual(
            self.dept.display_name,
            "Admin",
            "By default the content of the department name field is displayed",
        )

    def test_department_name_get_ethiopic(self):

        self.env["ir.config_parameter"].set_param(
            "l10n_et_hr.use_ethiopic_department", True
        )

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_department"
        )
        self.assertTrue(
            use_ethiopic_name, "I turned the ethiopic department name knob ON"
        )

        self.assertEqual(
            self.dept.display_name,
            "አስተዳደር",
            "The content of 'ethiopic_name' field is displayed",
        )

    def test_job_name_get(self):

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_job"
        )
        self.assertEqual(
            use_ethiopic_name, False, "By default the job ethiopic name knob is OFF"
        )

        self.assertEqual(
            self.job.display_name,
            "somejob",
            "By default the content of the job name field is displayed",
        )

    def test_job_name_get_ethiopic(self):

        self.env["ir.config_parameter"].set_param("l10n_et_hr.use_ethiopic_job", True)

        use_ethiopic_name = self.env["ir.config_parameter"].get_param(
            "l10n_et_hr.use_ethiopic_job"
        )
        self.assertTrue(use_ethiopic_name, "I turned the ethiopic job name knob ON")

        self.assertEqual(
            self.job.display_name,
            "ቦዘኔ",
            "The content of 'ethiopic_name' field is displayed",
        )

    def test_employee_name_get(self):

        self.assertEqual(
            self.ee.name_get()[0][1],
            "Mike",
            "The name_get() method is working as expected",
        )

        self.env["ir.config_parameter"].set_param(
            "l10n_et_hr.use_ethiopic_employee_name", True
        )
        self.assertEqual(
            self.ee.name_get()[0][1],
            "ሚኪ",
            "The name_get() method is working as expected",
        )
