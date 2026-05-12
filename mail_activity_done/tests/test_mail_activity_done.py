# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestMailActivityDoneMethods(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["res.users"].create(
            {
                "company_id": cls.env.ref("base.main_company").id,
                "name": "Test User",
                "login": "testuser@testuser.local",
                "email": "testuser@testuser.local",
                "tz": "Europe/Brussels",
                "groups_id": [
                    fields.Command.set(
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("base.group_partner_manager").id,
                        ]
                    )
                ],
            }
        )
        cls.partner = (
            cls.env["res.partner"]
            .with_user(cls.employee)
            .create({"name": "test partner"})
        )
        activity_type = cls.env["mail.activity.type"].create(
            {"name": "test activity type"}
        )
        today = fields.Date.context_today(cls.employee)
        cls.act1 = (
            cls.env["mail.activity"]
            .with_user(cls.employee)
            .create(
                {
                    "activity_type_id": activity_type.id,
                    "res_id": cls.partner.id,
                    "res_model": "res.partner",
                    "res_model_id": cls.env["ir.model"]._get("res.partner").id,
                    "user_id": cls.employee.id,
                    "date_deadline": today,
                }
            )
        )
        cls.act2 = (
            cls.env["mail.activity"]
            .with_user(cls.employee)
            .create(
                {
                    "activity_type_id": activity_type.id,
                    "res_id": cls.partner.id,
                    "res_model": "res.partner",
                    "res_model_id": cls.env["ir.model"]._get("res.partner").id,
                    "user_id": cls.employee.id,
                    "date_deadline": today,
                }
            )
        )
        cls.activities = cls.act1 + cls.act2

    def _set_activities_done(self):
        self.activities._action_done()
        self.activities.flush_recordset()

    def test_mail_activity_done(self):
        self.act1._action_done()
        self.assertTrue(self.act1.exists())
        self.assertEqual(self.act1.state, "done")

    def test_systray_get_activities(self):
        act_count = self.employee.with_user(self.employee).systray_get_activities()
        self.assertEqual(
            act_count[0]["total_count"],
            2,
            "Number of activities should be equal to two",
        )
        self.act1._action_done()
        act_count = self.employee.with_user(self.employee).systray_get_activities()
        self.assertEqual(
            act_count[0]["total_count"],
            1,
            "Number of activities should be equal to one",
        )

    def test_read_progress_bar(self):
        params = {
            "domain": [],
            "group_by": "id",
            "progress_bar": {"field": "activity_state"},
        }
        result = self.partner._read_progress_bar(**params)
        self.assertEqual(result[0]["__count"], 1)
        self._set_activities_done()
        result = self.partner._read_progress_bar(**params)
        self.assertEqual(len(result), 0)

    def test_activity_state_search(self):
        today_activities = (
            self.env["res.partner"]
            .with_user(self.employee)
            .search([("activity_state", "=", "today")])
        )
        self.assertEqual(len(today_activities), 1)
        self._set_activities_done()
        today_activities = (
            self.env["res.partner"]
            .with_user(self.employee)
            .search([("activity_state", "=", "today")])
        )
        self.assertEqual(len(today_activities), 0)
