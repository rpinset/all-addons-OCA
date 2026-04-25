# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def write(self, vals):
        result = super().write(vals)
        if "stage_id" in vals:
            for this in self:
                this.sudo()._set_stage_task()
        return result

    def _set_stage_task(self):
        self.ensure_one()
        if not self.task_id:
            return
        new_stage = (self.stage_id.task_stage_ids & self.task_id.project_id.type_ids)[
            :1
        ]
        if new_stage and self.task_id.stage_id != new_stage:
            self.task_id.stage_id = new_stage
