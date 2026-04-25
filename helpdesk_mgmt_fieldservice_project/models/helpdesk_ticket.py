# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def action_create_order(self):
        action = super().action_create_order()
        if project := self.project_id:
            action["context"]["default_project_id"] = project.id
        if task := self.task_id:
            action["context"]["default_project_task_id"] = task.id
        return action
