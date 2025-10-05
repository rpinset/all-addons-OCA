# Copyright Cetmix OU 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ProductAcquirerSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # value stored в ir.config_parameter
    product_acquirer_restriction_mode = fields.Selection(
        selection=[("first", "First Product"), ("all", "All Products")],
        config_parameter="product_acquirer_settings.product_acquirer_restriction_mode",
    )
