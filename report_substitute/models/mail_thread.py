# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):

    _inherit = "mail.thread"

    def message_post_with_template(self, template_id, **kwargs):
        template = self.env["mail.template"].browse(template_id)
        if template and template.report_template and self.ids:
            active_ids = self.ids
            report_template = template.report_template.get_substitution_report(
                active_ids
            )
            return super(
                MailThread, self.with_context(default_report_template=report_template)
            ).message_post_with_template(template_id, **kwargs)
        return super().message_post_with_template(template_id, **kwargs)
