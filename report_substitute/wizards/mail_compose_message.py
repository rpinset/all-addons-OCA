# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessage(models.TransientModel):

    _inherit = "mail.compose.message"

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields):
        if self.template_id:
            report_template = self.template_id.report_template
            active_ids = []
            if self.env.context.get("active_ids"):
                active_ids = self.env.context.get("active_ids")
            elif self.env.context.get("default_res_id"):
                active_ids = [self.env.context.get("default_res_id")]
            if (
                report_template
                and report_template.action_report_substitution_rule_ids
                and active_ids
            ):
                report_template = (
                    self.template_id.report_template.get_substitution_report(active_ids)
                )
                return super(
                    MailComposeMessage,
                    self.with_context(default_report_template=report_template),
                ).generate_email_for_composer(template_id, res_ids, fields)
        return super().generate_email_for_composer(template_id, res_ids, fields)
