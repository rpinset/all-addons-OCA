# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_client_order_ref_sale = fields.Boolean(
        related="company_id.show_client_order_ref_sale", readonly=False
    )
    show_client_order_ref_invoice = fields.Boolean(
        related="company_id.show_client_order_ref_invoice", readonly=False
    )
