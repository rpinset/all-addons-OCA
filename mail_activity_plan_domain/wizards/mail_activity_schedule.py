from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class MailActivitySchedule(models.TransientModel):
    _inherit = "mail.activity.schedule"

    @api.depends("res_ids")
    def _compute_plan_available_ids(self):
        # Add res_ids as dependency so that available plans recompute when
        # the selected records change (needed for plan domain evaluation)
        return super()._compute_plan_available_ids()

    def _compute_plan_id(self):
        # Preserve an already-selected plan when it is still available.
        # The core implementation resets plan_id to False unless plan_mode is
        # active. This override keeps the current value when it is still among
        # the available plans, avoiding unwanted resets triggered by the ORM
        # recompute cascade (e.g. when res_ids changes or during create()).
        self = self.filtered(
            lambda s: not s.plan_id or s.plan_id not in s.plan_available_ids
        )
        return super()._compute_plan_id()

    def _get_eval_context(self):
        return {"uid": self.env.uid, "user": self.env.user}

    def _get_summary_lines(self, templates):
        # We filter the templates that will be displayed in the summary
        new_templates = self.env[templates._name]
        eval_context = self._get_eval_context()
        for record in self._get_applied_on_records():
            new_templates += templates.filtered(
                lambda tpl, record=record: self._is_template_domain_matching(
                    tpl, record, eval_context
                )
            )
        return super()._get_summary_lines(new_templates)

    def _get_plan_available_base_domain(self):
        # Extend the base domain to also filter plans whose domain matches
        # at least one of the currently selected records (AND condition).
        domain = super()._get_plan_available_base_domain()
        records = self._get_applied_on_records()
        if not records:
            return domain
        all_plans = self.env["mail.activity.plan"].search(domain)
        eval_context = self._get_eval_context()
        valid_ids = [
            plan.id
            for plan in all_plans
            if self._is_plan_domain_matching(plan, records, eval_context)
        ]
        return [("id", "in", valid_ids)]

    def _is_plan_domain_matching(self, plan, records, eval_context):
        """Return True if the plan has no domain or if at least one of the
        given records matches the plan's domain."""
        if not plan.domain or plan.domain == "[]":
            return True
        return bool(records.filtered_domain(safe_eval(plan.domain, eval_context)))

    def action_schedule_plan(self):
        # Serialize execution record by record so that the template domain
        # can be evaluated individually per record.
        # When the context key ``mail_activity_plan_domain_record_id`` is set,
        # this method acts as a single-record dispatcher and delegates to the
        # standard implementation via super(). Otherwise it loops over each
        # record, calling itself with the proper context.
        if self.env.context.get("mail_activity_plan_domain_record_id"):
            # Single-record mode: let the standard implementation run.
            # _get_applied_on_records and _plan_filter_activity_templates_to_schedule
            # are already overridden to handle the context record.
            return super().action_schedule_plan()
        applied_on = self._get_applied_on_records()
        for record in applied_on:
            self.with_context(
                mail_activity_plan_domain_record_id=record.id
            ).action_schedule_plan()
        if len(applied_on) == 1:
            return {"type": "ir.actions.client", "tag": "soft_reload"}
        return {
            "type": "ir.actions.act_window",
            "res_model": self.res_model,
            "name": self.env._("Launch Plans"),
            "view_mode": "list,form",
            "target": "current",
            "domain": [("id", "in", applied_on.ids)],
        }

    def _get_applied_on_records(self):
        # When called from the serialized loop (context has a single record
        # ID), return only that record instead of re-browsing all res_ids.
        record_id = self.env.context.get("mail_activity_plan_domain_record_id")
        if record_id:
            return self.env[self.res_model].browse(record_id)
        return super()._get_applied_on_records()

    def _plan_filter_activity_templates_to_schedule(self):
        # Filter plan templates whose domain matches the current record.
        # Note: intentionally NOT used by _check_plan_templates_error so that
        # the error preview still shows all potential issues regardless of
        # template domains.
        templates = super()._plan_filter_activity_templates_to_schedule()
        record_id = self.env.context.get("mail_activity_plan_domain_record_id")
        if not record_id:
            return templates
        record = self.env[self.res_model].browse(record_id)
        eval_context = self._get_eval_context()
        return templates.filtered(
            lambda tpl: self._is_template_domain_matching(tpl, record, eval_context)
        )

    def _is_template_domain_matching(self, template, record, eval_context):
        """Return True if the template has no domain or if the given record
        matches the template's domain."""
        if not template.domain or template.domain == "[]":
            return True
        return bool(record.filtered_domain(safe_eval(template.domain, eval_context)))
