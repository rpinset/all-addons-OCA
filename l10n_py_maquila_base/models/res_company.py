# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_py_is_maquiladora = fields.Boolean(
        string="Is Maquiladora",
        help="Check if this company operates under Maquila regime (Ley 7547/2025)",
    )
