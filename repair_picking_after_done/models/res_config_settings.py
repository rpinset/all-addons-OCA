# Copyright 2024 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_transfer_repair = fields.Boolean(
        "Automatic Transfer on Repair Completion",
        config_parameter="repair.auto_transfer_repair",
        help="Automatically create and validate transfers for "
        "repair orders upon completion.",
    )
