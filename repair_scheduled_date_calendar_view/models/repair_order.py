# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RepairOrder(models.Model):
    _inherit = "repair.order"

    def _get_default_planned_duration(self):
        """Read default planned duration from system parameter."""
        return float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "repair_scheduled_date_calendar_view.planned_duration_default",
                1.0,
            )
        )

    planned_duration = fields.Float(
        # Keep field default as generic fallback when nothing passed at all
        default=lambda self: self._get_default_planned_duration(),
        help="Planned duration of the repair order in hours.",
    )

    @api.model
    def default_get(self, fields_list):
        """Set default planned duration from system parameter."""
        res = super().default_get(fields_list)

        if "planned_duration" in fields_list:
            # Always use configured default, ignoring calendar placeholders
            res["planned_duration"] = self._get_default_planned_duration()

        return res

    @api.constrains("planned_duration")
    def _check_planned_duration(self):
        """Disallow negative durations."""
        for rec in self:
            if rec.planned_duration < 0:
                raise ValidationError(_("Planned duration must be non-negative."))
