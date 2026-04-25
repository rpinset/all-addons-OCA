# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class HelpdeskTicketStage(models.Model):
    _inherit = "helpdesk.ticket.stage"

    task_stage_ids = fields.Many2many(
        "project.task.type",
        relation="project_task_type_helpdesk_ticket_stage_rel",
        column1="helpdesk_ticket_stage_id",
        column2="project_task_type_id",
    )
