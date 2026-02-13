# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    enable_contract_invoice_manually = fields.Boolean(
        string="Enable Manual Invoicing",
        help="Exclude contracts from being invoiced automatically",
    )
