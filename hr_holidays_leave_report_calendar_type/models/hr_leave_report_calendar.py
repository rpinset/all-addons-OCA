# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"

    holiday_status_id = fields.Many2one(
        "hr.leave.type",
        string="Time Off Type",
        compute="_compute_holiday_status_id",
        search="_search_holiday_status_id",
        groups="hr_holidays.group_hr_holidays_user",
    )

    def _compute_holiday_status_id(self):
        leaves = self.env["hr.leave"].browse(self.ids)
        leave_status_dict = {leave.id: leave.holiday_status_id for leave in leaves}
        for record in self:
            record.holiday_status_id = leave_status_dict.get(record.id, False)

    def _search_holiday_status_id(self, operator, value):
        leaves = self.env["hr.leave"].search([("holiday_status_id", operator, value)])
        return [("id", "in", leaves.ids)]
