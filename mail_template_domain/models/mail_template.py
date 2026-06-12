from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    filter_model = fields.Boolean(string="Restrict?")
    filter_domain = fields.Char(
        string="Restrict domain",
        help="If set, this template will only appear in the email composer "
        "when the active record matches this domain.",
        compute="_compute_filter_domain",
        store=True,
        readonly=False,
    )

    @api.depends("filter_model")
    def _compute_filter_domain(self):
        for item in self.filtered(lambda x: not x.filter_model):
            item.filter_domain = "[]"

    @api.onchange("model_id")
    def _onchange_model_id(self):
        for item in self:
            item.filter_domain = "[]"
