from odoo import api, fields, models


class MailActivityPlan(models.Model):
    _inherit = "mail.activity.plan"

    domain = fields.Char(
        default="[]",
        help="Domain to filter the records on which this plan is applicable. "
        "Leave empty or use '[]' to apply to all records of the target model.",
    )

    @api.onchange("res_model")
    def _onchange_res_model(self):
        for item in self:
            item.domain = "[]"
