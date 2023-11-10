from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    l10n_hr_nkd_id = fields.Many2one(
        comodel_name="l10n.hr.nkd",
        string="NKD",
        help="Main occupation classified according to NKD-2007",
    )

    @api.onchange("l10n_hr_nkd_id")
    def _onchange_nkd_id(self):
        self.l10n_hr_nkd = self.l10n_hr_nkd_id.code
