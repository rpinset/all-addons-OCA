import ast

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    domain_template_id = fields.Binary(compute="_compute_domain_template_id")
    # add domain to the existing field
    template_id = fields.Many2one(domain="domain_template_id")

    @api.depends("res_ids", "model")
    def _compute_domain_template_id(self):
        mail_template_model = self.env["mail.template"]
        for item in self:
            if not item.res_ids:
                res_ids = []
            elif isinstance(item.res_ids, list):
                res_ids = item.res_ids
            elif isinstance(item.res_ids, str):
                res_ids = ast.literal_eval(item.res_ids)
            records = self.env[item.model].browse(res_ids)
            if not records.exists():
                item.domain_template_id = []
                continue
            full_templates = mail_template_model.search([("model", "=", item.model)])
            valid_templates = mail_template_model
            for template in full_templates:
                if not template.filter_model or not template.filter_domain:
                    valid_templates += template
                    continue
                records_ok = records.filtered_domain(safe_eval(template.filter_domain))
                if len(records) == len(records_ok):
                    valid_templates += template
            domain = [("id", "in", valid_templates.ids)]
            item.domain_template_id = domain
