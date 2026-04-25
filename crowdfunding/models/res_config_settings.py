# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crowdfunding_default_fee_percentage = fields.Float(
        related="company_id.crowdfunding_default_fee_percentage",
        readonly=False,
    )
    crowdfunding_product_id = fields.Many2one(
        related="company_id.crowdfunding_product_id",
        readonly=False,
    )
