# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CommissionItem(models.Model):
    _inherit = "commission.item"

    fiscal_position_type = fields.Selection(
        selection="_selection_fiscal_position_type",
    )

    def _selection_fiscal_position_type(self):
        return self.env["res.partner"]._selection_fiscal_position_type()
