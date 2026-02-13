# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_contract_invoice_manually = fields.Boolean(
        related="company_id.enable_contract_invoice_manually", readonly=False
    )
