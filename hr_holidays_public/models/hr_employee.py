# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    is_public_holiday = fields.Boolean(
        string="Public Holiday Today", compute="_compute_is_public_holiday"
    )

    def _compute_is_public_holiday(self):
        holiday_public = self.env["hr.holidays.public"]
        for item in self:
            item.is_public_holiday = holiday_public.is_public_holiday(
                fields.Date.context_today(item), employee_id=item.id
            )

    def _get_im_status_hr_holidays_public(self, key):
        im_status_mapped = {
            "online": "leave_online",
            "away": "leave_away",
            "offline": "leave_offline",
        }
        return im_status_mapped[key]

    def _compute_leave_status(self):
        res = super()._compute_leave_status()
        for item in self.filtered(lambda x: not x.is_absent and x.is_public_holiday):
            item.is_absent = True
        return res
