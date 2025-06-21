# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    @api.model
    def _get_forecast_update_trigger_fields(self):
        return super()._get_forecast_update_trigger_fields() + [
            "qty_type",
            "qty_formula_id",
        ]
