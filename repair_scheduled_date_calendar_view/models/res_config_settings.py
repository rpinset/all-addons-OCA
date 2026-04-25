# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    planned_duration_default = fields.Float(
        default=1.0,
        config_parameter="repair_scheduled_date_calendar_view.planned_duration_default",
        help="Default planned duration for repair orders (in hours). "
        "Shown as hh:mm in the UI.",
    )
