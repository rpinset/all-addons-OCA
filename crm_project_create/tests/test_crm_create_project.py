# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from markupsafe import Markup

from odoo.tests.common import Form, TransactionCase, users

from odoo.addons.mail.tests.common import mail_new_test_user


class TestCrmCreateProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create(
            {
                "name": "Company Test",
            }
        )
        cls.user_salesman = mail_new_test_user(
            cls.env,
            login="user_salesman",
            name="User Salesman",
            email="user_salesman@test.example.com",
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman",
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Test",
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "lead",
                "partner_id": cls.partner.id,
                "user_id": cls.user_salesman.id,
            }
        )
        cls.default_plan = cls.env["account.analytic.plan"].create(
            {"name": "Default", "company_id": False}
        )

    @users("user_salesman")
    def test_crm_project_create(self):
        """Test the creation of a project from a lead."""
        wizard_form = Form(
            self.env["crm.create.project"].with_context(
                active_model="crm.lead",
                active_id=self.lead.id,
                default_lead_id=self.lead.id,
                default_project_name=self.lead.name,
            )
        )
        self.assertEqual(wizard_form.project_name, self.lead.name)
        wizard_form.project_name = "Test Project"
        wizard_form.project_description = "Test Description"
        wizard = wizard_form.save()
        wizard.create_project()

        self.assertTrue(self.lead.project_id)
        self.assertEqual(self.lead.project_id.name, "Test Project")
        self.assertEqual(
            self.lead.project_id.description,
            Markup("<p>Test Description</p>"),
        )
        # When a lead is archived, so it's project and their analytic account.
        analytic_account = self.env["account.analytic.account"].create(
            {
                "name": "Test analytic account",
                "plan_id": self.default_plan.id,
                "company_id": False,
            }
        )
        self.lead.project_id.analytic_account_id = analytic_account
        self.lead.action_archive()
        self.assertFalse(self.lead.project_id.active)
        self.assertFalse(self.lead.project_id.analytic_account_id.active)
        # Reactivate the lead
        self.lead.toggle_active()
        self.assertTrue(self.lead.project_id.active)
        self.assertTrue(self.lead.project_id.analytic_account_id.active)
        # Mark lead as lost
        lost_wizard = self.env["crm.lead.lost"].create(
            {
                "lost_reason_id": self.env.ref("crm.lost_reason_1").id,
            }
        )
        lost_wizard.with_context(active_ids=self.lead.ids).action_lost_reason_apply()
        self.assertFalse(self.lead.project_id.active)
        self.assertFalse(self.lead.project_id.analytic_account_id.active)
