from odoo import Command
from odoo.tests import tagged

from odoo.addons.mail.tests.test_mail_activity import ActivityScheduleCase


@tagged("mail_activity", "mail_activity_plan_domain")
class TestMailActivityPlanDomain(ActivityScheduleCase):
    """Tests for mail_activity_plan_domain module.

    Covers:
    - Plan domain: plans only appear for matching records.
    - Template domain: activities are only scheduled for matching records.
    - Error preview: ignores template domain (shows all potential errors).
    - Multi-record serialized execution.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create two partners: one company, one individual
        cls.partner_company = cls.env["res.partner"].create(
            {"name": "ACME Corp", "is_company": True}
        )
        cls.partner_individual = cls.env["res.partner"].create(
            {"name": "John Doe", "is_company": False}
        )
        # Plan without domain (applies to all partners)
        cls.plan_all = cls.env["mail.activity.plan"].create(
            {
                "name": "Plan All Partners",
                "res_model": "res.partner",
                "domain": "[]",
                "template_ids": [
                    Command.create(
                        {
                            "activity_type_id": cls.activity_type_todo.id,
                            "responsible_type": "other",
                            "responsible_id": cls.user_admin.id,
                            "sequence": 10,
                            "summary": "General task",
                        }
                    ),
                ],
            }
        )
        # Plan restricted to companies only
        cls.plan_companies = cls.env["mail.activity.plan"].create(
            {
                "name": "Plan Companies Only",
                "res_model": "res.partner",
                "domain": "[('is_company', '=', True)]",
                "template_ids": [
                    Command.create(
                        {
                            "activity_type_id": cls.activity_type_todo.id,
                            "responsible_type": "other",
                            "responsible_id": cls.user_admin.id,
                            "sequence": 10,
                            "summary": "Company task",
                        }
                    ),
                ],
            }
        )
        # Plan with two templates: one for all, one restricted to companies
        cls.plan_mixed = cls.env["mail.activity.plan"].create(
            {
                "name": "Plan Mixed Templates",
                "res_model": "res.partner",
                "domain": "[]",
                "template_ids": [
                    Command.create(
                        {
                            "activity_type_id": cls.activity_type_todo.id,
                            "responsible_type": "other",
                            "responsible_id": cls.user_admin.id,
                            "sequence": 10,
                            "summary": "Common task",
                            "domain": "[]",
                        }
                    ),
                    Command.create(
                        {
                            "activity_type_id": cls.activity_type_todo.id,
                            "responsible_type": "other",
                            "responsible_id": cls.user_admin.id,
                            "sequence": 20,
                            "summary": "Company-only task",
                            "domain": "[('is_company', '=', True)]",
                        }
                    ),
                ],
            }
        )

    def _make_wizard(self, records, plan=None):
        """Helper: instantiate the activity schedule wizard for the given
        records and optionally pre-select a plan.

        Uses the same Form-based approach as the core tests to ensure computed
        fields (plan_available_ids, plan_id) are correctly resolved via
        onchange semantics before the record is saved.
        """
        form = self._instantiate_activity_schedule_wizard(records)
        if plan:
            form.plan_id = plan
        return form.save()

    def test_plan_domain_field_exists(self):
        """Plan and template have the domain field with the expected default."""
        self.assertEqual(self.plan_all.domain, "[]")
        self.assertEqual(self.plan_companies.domain, "[('is_company', '=', True)]")
        for template in self.plan_mixed.template_ids:
            self.assertIsNotNone(template.domain)

    def test_plan_available_ids_without_domain(self):
        """Plan with no domain is available for any record."""
        wizard = self._make_wizard(self.partner_individual)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertNotIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)

    def test_plan_domain_excludes_non_matching_records(self):
        """Plan with domain is NOT available for records that don't match."""
        wizard = self._make_wizard(self.partner_individual)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertNotIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)

    def test_plan_domain_includes_matching_records(self):
        """Plan with domain IS available for records that match."""
        wizard = self._make_wizard(self.partner_company)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)

    def test_plan_domain_multi_record_any_match(self):
        """Plan with domain is available if AT LEAST ONE selected record matches."""
        both = self.partner_company + self.partner_individual
        wizard = self._make_wizard(both)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)

    def test_plan_available_ids_recompute_on_res_ids_change(self):
        """Changing res_ids triggers recomputation of available plans."""
        wizard = self._make_wizard(self.partner_individual)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertNotIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)
        wizard.res_ids = repr(self.partner_company.ids)
        self.assertIn(self.plan_all, wizard.plan_available_ids)
        self.assertIn(self.plan_companies, wizard.plan_available_ids)
        self.assertIn(self.plan_mixed, wizard.plan_available_ids)

    def test_template_domain_schedules_all_activities_for_company(self):
        """Both templates are scheduled when the record matches the company domain."""
        wizard = self._make_wizard(self.partner_company, plan=self.plan_mixed)
        with self._mock_activities():
            wizard.action_schedule_plan()

        activities = self._new_activities.filtered(
            lambda a: a.res_model == "res.partner"
            and a.res_id == self.partner_company.id
        )
        summaries = activities.mapped("summary")
        self.assertIn("Common task", summaries)
        self.assertIn("Company-only task", summaries)
        self.assertEqual(len(activities), 2)

    def test_template_domain_skips_non_matching_activity_for_individual(self):
        """Company-only template is NOT scheduled for an individual partner."""
        wizard = self._make_wizard(self.partner_individual, plan=self.plan_mixed)
        with self._mock_activities():
            wizard.action_schedule_plan()

        activities = self._new_activities.filtered(
            lambda a: a.res_model == "res.partner"
            and a.res_id == self.partner_individual.id
        )
        summaries = activities.mapped("summary")
        self.assertIn("Common task", summaries)
        self.assertNotIn("Company-only task", summaries)
        self.assertEqual(len(activities), 1)

    def test_template_domain_multi_record_per_record_filtering(self):
        """In multi-record mode, template domain is evaluated per record."""
        both = self.partner_company + self.partner_individual
        wizard = self._make_wizard(both, plan=self.plan_mixed)
        with self._mock_activities():
            wizard.action_schedule_plan()

        company_activities = self._new_activities.filtered(
            lambda a: a.res_model == "res.partner"
            and a.res_id == self.partner_company.id
        )
        individual_activities = self._new_activities.filtered(
            lambda a: a.res_model == "res.partner"
            and a.res_id == self.partner_individual.id
        )
        self.assertEqual(len(company_activities), 2)
        self.assertEqual(len(individual_activities), 1)
        self.assertNotIn("Company-only task", individual_activities.mapped("summary"))

    def test_error_preview_ignores_template_domain(self):
        """The wizard error preview checks ALL templates regardless of domain.

        This ensures that missing responsible warnings are shown even for
        templates that would be filtered out for the current record.
        """
        plan_error = self.env["mail.activity.plan"].create(
            {
                "name": "Plan Error Preview",
                "res_model": "res.partner",
                "domain": "[]",
                "template_ids": [
                    Command.create(
                        {
                            "activity_type_id": self.activity_type_todo.id,
                            "responsible_type": "on_demand",
                            "sequence": 10,
                            "summary": "Task needs responsible",
                            "domain": "[('is_company', '=', True)]",
                        }
                    ),
                ],
            }
        )
        # Individual record — template domain would exclude this template,
        # but the error preview must still warn about missing responsible.
        # We must clear plan_on_demand_user_id (default = current user) to
        # trigger the "no responsible" error, same as the core tests do.
        # Note: the wizard cannot be saved when has_error=True (_check_consistency
        # constraint), so we read has_error/error from the Form directly.
        form = self._instantiate_activity_schedule_wizard(self.partner_individual)
        form.plan_id = plan_error
        form.plan_on_demand_user_id = self.env["res.users"]
        self.assertTrue(form.has_error)
        self.assertIn("No responsible specified", form.error)

    def test_plan_domain_skips_non_matching_records_on_execution(self):
        """Single-record execution path works correctly for matching record."""
        wizard = self._make_wizard(self.partner_individual, plan=self.plan_all)
        with self._mock_activities():
            wizard.with_context(
                mail_activity_plan_domain_record_id=self.partner_individual.id
            ).action_schedule_plan()

        activities = self._new_activities.filtered(
            lambda a: a.res_model == "res.partner"
            and a.res_id == self.partner_individual.id
        )
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0].summary, "General task")
