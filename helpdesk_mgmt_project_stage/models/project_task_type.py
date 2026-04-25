# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    ticket_stage_ids = fields.Many2many(
        "helpdesk.ticket.stage",
        relation="project_task_type_helpdesk_ticket_stage_rel",
        column1="project_task_type_id",
        column2="helpdesk_ticket_stage_id",
    )
