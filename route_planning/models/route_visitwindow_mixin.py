# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RouteVisitwindowMixin(models.AbstractModel):
    _name = "route.visitwindow.mixin"
    _description = "Visit Window Mixin"
    _order = "day_of_week, time_from"

    day_of_week = fields.Selection(
        [
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        required=True,
    )
    time_from = fields.Float(help="Start time of the visit window")
    time_to = fields.Float(help="End time of the visit window", default=24.0)

    @api.constrains("time_from", "time_to")
    def _check_time_from_to(self):
        for record in self:
            if record.time_from >= record.time_to:
                raise models.ValidationError(
                    self.env._("The time from must be earlier than the time to.")
                )
