# l10n_py_base/models/res_company.py

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    country_id = fields.Many2one(
        default=lambda self: self.env.ref("base.py", raise_if_not_found=False)
    )
