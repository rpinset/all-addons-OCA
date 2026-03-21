# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_partner_street_number = fields.Boolean(
        "Use split fields for street name in partner form",
        implied_group="partner_street_number.group_edit_split_street_name",
    )
