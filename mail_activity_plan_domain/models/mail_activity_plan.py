from odoo import fields, models


class MailActivityPlan(models.Model):
    _inherit = "mail.activity.plan"

    domain = fields.Char(
        default="[]",
        help="Domain to filter the records on which this plan is applicable. "
        "Leave empty or use '[]' to apply to all records of the target model.",
    )
