# Copyright 2016-2026 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, tools


class MailTemplate(models.Model):
    _inherit = "mail.template"

    body_type = fields.Selection(
        [("qweb", "QWeb"), ("qweb_view", "QWeb View")],
        "Body templating engine",
        default="qweb",
        required=True,
    )
    body_view_id = fields.Many2one("ir.ui.view", domain=[("type", "=", "qweb")])
    body_view_arch = fields.Text(related="body_view_id.arch")

    def generate_email(self, res_ids, fields):
        multi_mode = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi_mode = False
        result = super().generate_email(res_ids, fields=fields)
        if self.body_type != "qweb_view" or (fields and "body_html" not in fields):
            return result if multi_mode else result[res_ids[0]]
        for lang, (_template, template_res_ids) in self._classify_per_lang(
            res_ids
        ).items():
            self_with_lang = self.with_context(lang=lang)
            IrQweb = self_with_lang.env["ir.qweb"]
            for res_id in template_res_ids:
                record = self_with_lang.env[self_with_lang.model].browse(res_id)
                result_res_id = result[res_id]
                body_html = IrQweb._render(
                    self_with_lang.body_view_id.id,
                    {"object": record, "email_template": self_with_lang},
                )
                body_html = tools.ustr(body_html)
                rendered_post_temp = self_with_lang._render_template_postprocess(
                    {res_id: body_html}
                )
                result_res_id["body_html"] = rendered_post_temp[res_id]
                result_res_id["body"] = tools.html_sanitize(result_res_id["body_html"])
        return result if multi_mode else result[res_ids[0]]
