# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TimesheetPredefinedDescription(models.Model):
    _inherit = "timesheet.predefined.description"

    allow_free_text = fields.Boolean(
        help=(
            "Enable this to allow users to enter additional text when "
            "using this predefined description."
        ),
    )
    free_text_required = fields.Boolean(
        help=(
            "If checked, the user must provide additional text when "
            "using this predefined description."
        ),
    )
    append_free_text_to_name = fields.Boolean(
        help=(
            "If enabled, any additional text entered by the user will be "
            "appended to the predefined description name."
        ),
    )

    @api.onchange("allow_free_text")
    def _onchange_allow_free_text(self):
        for rec in self:
            if not rec.allow_free_text:
                rec.free_text_required = False
                rec.append_free_text_to_name = False
