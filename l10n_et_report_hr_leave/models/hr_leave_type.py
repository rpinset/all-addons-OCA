# Copyright (C) 2025 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrLeaveType(models.Model):

    _inherit = "hr.leave.type"

    ethiopic_name = fields.Char()

    def get_remaining_days_by_employee(self, employee_id):
        employee_ids = [employee_id]
        res = {
            employee_id: {
                leave_type.id: {
                    "max_leaves": 0,
                    "leaves_taken": 0,
                    "remaining_leaves": 0,
                    "virtual_remaining_leaves": 0,
                    "virtual_leaves_taken": 0,
                }
                for leave_type in self
            }
            for employee_id in employee_ids
        }

        if employee_id:
            res = self.get_days(employee_id)
        return res
