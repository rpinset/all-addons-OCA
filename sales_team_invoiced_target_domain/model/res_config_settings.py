from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crm_team_invoiced_domain = fields.Char(
        related="company_id.crm_team_invoiced_domain", readonly=False
    )
