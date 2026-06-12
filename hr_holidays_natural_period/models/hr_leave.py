# Copyright 2020-2025 Tecnativa - Víctor Martínez
# Copyright 2024 Tecnativa - Carlos Lopez
# Copyright 2025 Grupo Isonor - Alexandre D. Díaz
# Copyright 2026 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        # Inject context for getting the proper computation in
        # resource.calendar~_attendance_intervals_batch
        mod_holidays_status_ids = self.env.context.get("mod_holidays_status_ids", [])
        natural_day_instances = self.filtered(
            lambda x: x.holiday_status_id.id in mod_holidays_status_ids
            or x.holiday_status_id.request_unit
            in ("natural_day", "natural_day_half_day")
        )
        res = super(HrLeave, self - natural_day_instances)._get_durations(
            check_leave_type=check_leave_type, resource_calendar=resource_calendar
        )
        if not natural_day_instances:
            return res
        leaves_by_hs = defaultdict(lambda: self.env["hr.leave"])
        for natural_day in natural_day_instances:
            leaves_by_hs[natural_day.holiday_status_id] += natural_day
        for holiday_status, leaves in leaves_by_hs.items():
            orig_request_unit = holiday_status.request_unit
            new_request_unit = (
                "half_day" if orig_request_unit == "natural_day_half_day" else "day"
            )
            # We need to set request_unit as day/half_day to avoid incorrect
            # _check_validity
            # HACK: The field is updated in this way to prevent infinite recursion.
            if holiday_status.id not in mod_holidays_status_ids:
                self.env.cache.update_raw(
                    holiday_status,
                    holiday_status._fields["request_unit"],
                    [new_request_unit],
                    dirty=True,
                )
            _leaves = leaves.with_context(
                natural_period=True, old_request_unit=orig_request_unit
            )
            _res = super(HrLeave, _leaves)._get_durations(
                check_leave_type=check_leave_type, resource_calendar=resource_calendar
            )
            res.update(_res)
            if holiday_status.id not in mod_holidays_status_ids:
                self.env.cache.update_raw(
                    holiday_status,
                    holiday_status._fields["request_unit"],
                    [orig_request_unit],
                    dirty=True,
                )
        return res
