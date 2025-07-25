# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.tests.common import Form, TransactionCase


class RecruitmentTestCase(TransactionCase):
    def setUp(self):
        super().setUp()

        self.Contract = self.env["hr.contract"]
        self.Partner = self.env["res.partner"]
        self.Period = self.env["hr.payroll.period"]
        self.PPSchedule = self.env["hr.payroll.period.schedule"]
        self.PolicyGroup = self.env["hr.policy.group"]
        self.labour_model = self.env["hr.employee.wizard.new"]
        benefits_model = self.env["hr.employee.wizard.benefit"]
        self.company = self.env.user.company_id
        self.state = self.env["res.country.state"].search([], limit=1)[0]
        self.country = self.env["res.country"].search([], limit=1)[0]
        self.job = self.env["hr.job"].search([], limit=1)[0]
        self.department = self.env["hr.department"].search([], limit=1)[0]
        self.structure = self.env["hr.payroll.structure"].search([], limit=1)[0]
        self.pps = self.create_payroll_schedule("monthly", date.today())
        self.pgroup = self.PolicyGroup.create({"name": "PGroup"})
        self.calendar_id = self.env.ref("resource_schedule.resource_calendar_44h")
        self.benefits = self.env["hr.benefit"].create({"name": "A", "code": "A"})

        benefits_data = {
            "benefit_id": self.benefits.id,
            "effective_date": "2017-01-01",
            "end_date": "2017-12-30",
            "adv_override": True,
            "prm_override": True,
            "adv_amount": 50.0,
            "prm_amount": 100.0,
            "prm_total": 2000.0,
        }
        self.benefit = benefits_model.create(benefits_data)

        self.labour_data = {
            "name": "Jean-Luc Picard",
            "ethiopic_name": "ዦን-ሉክ ፒካርድ",
            "new_benefit_ids": [(6, 0, [self.benefit.id])],
            "state": "personal",
            "company_id": self.company.id,
            "use_ethiopic_dob": True,
            "etcal_dob_year": "1998",
            "etcal_dob_month": "1",
            "etcal_dob_day": "1",
            # "birth_date": "2005-09-11",
            "gender": "m",
            "id_no": "123",
            "city": "test_city",
            "state_id": self.state.id,
            "country_id": self.country.id,
            "telephone": "123456789",
            "mobile": "09124578",
            "education": "none",
            "job_id": self.job.id,
            "department_id": self.department.id,
            "struct_id": self.structure.id,
            "pps_id": self.pps.id,
            "policy_group_id": self.pgroup.id,
            "wage": 2000,
            "calendar_id": self.calendar_id.id,
            "date_start": "2017-01-01",
        }

    def create_wizard(self):
        ctx = self.env.context.copy()
        ctx["csdate"] = self.labour_data["date_start"]
        return self.labour_model.with_context(ctx).create(self.labour_data)

    def create_payroll_schedule(self, stype=False, initial_date=False):
        return self.PPSchedule.create(
            {
                "name": "PPS",
                "tz": "Africa/Addis_Ababa",
                "type": stype,
                "initial_period_date": initial_date,
            }
        )

    def create_payroll_period(self, sched_id, start, end):
        return self.Period.create(
            {
                "name": "Period 1",
                "schedule_id": sched_id,
                "date_start": start,
                "date_end": end,
            }
        )

    def test_onchange_dob(self):

        f = Form(self.env["hr.employee.wizard.new"])
        f.name = "Jean-luc Picard"
        f.ethiopic_name = "ዦን-ሉክ ፒካርድ"
        f.gender = "f"
        f.education = "none"
        f.use_ethiopic_dob = True
        f.etcal_dob_year = "1998"
        f.etcal_dob_month = "1"
        f.etcal_dob_day = "1"

        self.assertEqual(
            f.birth_date,
            date(2005, 9, 11),
            "The ethiopic dob was correctly translated to the Gregorian date",
        )

        wizard = f.save()
        wizard.hire_applicant()
        ee = self.env["hr.employee"].search([("name", "=", "Jean-luc Picard")])

        self.assertTrue(ee, "I created the employee")
        self.assertEqual(
            ee.ethiopic_name,
            "ዦን-ሉክ ፒካርድ",
            "The contents of ethiopic name are saved in the employee record",
        )
        self.assertEqual(ee.etcal_dob_year, "1998", "The ethiopian DoB Year was saved")
        self.assertEqual(ee.etcal_dob_month, "1", "The ethiopian DoB MOnth was saved")
        self.assertEqual(ee.etcal_dob_day, "1", "The ethiopian DoB Day was saved")
        self.assertEqual(ee.certificate, "none", "The education level was saved")
