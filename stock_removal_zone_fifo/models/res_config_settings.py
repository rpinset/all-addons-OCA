# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    zone_in_date_update_out_of_zone = fields.Boolean(
        related="company_id.zone_in_date_update_out_of_zone", readonly=False
    )
