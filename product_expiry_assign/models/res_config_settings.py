# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_ignore_expiration_date = fields.Boolean(
        string="Ignore Expiration Date",
        related="company_id.product_ignore_expiration_date",
        readonly=False,
    )
