from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    display_valued_in_picking = fields.Boolean(default=False)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    display_valued_in_picking = fields.Boolean(
        related="company_id.display_valued_in_picking", readonly=False
    )
