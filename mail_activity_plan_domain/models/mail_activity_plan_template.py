from odoo import fields, models


class MailActivityPlanTemplate(models.Model):
    _inherit = "mail.activity.plan.template"

    domain = fields.Char(
        default="[]",
        help="Domain to filter the records for which this activity will be "
        "scheduled. Leave empty or use '[]' to always schedule this activity.",
    )
