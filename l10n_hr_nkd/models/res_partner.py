from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    l10n_hr_nkd_id = fields.Many2one(
        comodel_name="l10n.hr.nkd",
        string="NKD",
        help="Main occupation classified according to NKD-2007",
    )
