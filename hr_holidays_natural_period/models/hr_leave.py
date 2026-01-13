# Copyright 2020-2025 Tecnativa - Víctor Martínez
# Copyright 2024 Tecnativa - Carlos Lopez
# Copyright 2025 Grupo Isonor - Alexandre D. Díaz
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        # We need to set request_unit as 'day'
        # to avoid the calculations being done as hours.
        mod_holidays_status_ids = self.env.context.get("mod_holidays_status_ids", [])
        natural_day_instances = self.filtered(
            lambda x: x.holiday_status_id.id in mod_holidays_status_ids
            or x.holiday_status_id.request_unit
            in ("natural_day", "natural_day_half_day")
        )
        _self = self - natural_day_instances
        res = super(HrLeave, _self)._get_durations(
            check_leave_type=check_leave_type, resource_calendar=resource_calendar
        )
        if not natural_day_instances:
            return res
        leaves_by_hs = defaultdict(lambda: self.env["hr.leave"])
        for natural_day in natural_day_instances:
            hs_id = natural_day.holiday_status_id
            leaves_by_hs[hs_id] += natural_day
        for holiday_status_id, leaves in leaves_by_hs.items():
            orig_request_unit = holiday_status_id.request_unit
            new_request_unit = (
                "half_day" if orig_request_unit == "natural_day_half_day" else "day"
            )
            # FIXME: The field is updated in this way to prevent infinite recursion.
            self.env.cache.update_raw(
                holiday_status_id,
                holiday_status_id._fields["request_unit"],
                [new_request_unit],
                dirty=True,
            )
            _leaves = leaves.with_context(
                **{
                    "natural_period": True,
                    "old_request_unit": orig_request_unit,
                }
            )
            _res = super(
                HrLeave,
                _leaves,
            )._get_durations(
                check_leave_type=check_leave_type, resource_calendar=resource_calendar
            )
            res.update(_res)
            self.env.cache.update_raw(
                holiday_status_id,
                holiday_status_id._fields["request_unit"],
                [orig_request_unit],
                dirty=True,
            )
        return res
