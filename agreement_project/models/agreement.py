# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    task_count = fields.Integer("# Tasks", compute="_compute_task_count")
    project_id = fields.Many2one(
        "project.project", compute="_compute_project_id", store=True
    )

    def _compute_task_count(self):
        for ag in self:
            count = self.env["project.task"].search_count(
                [("agreement_id", "=", ag.id)]
            )
            ag.task_count = count

    def _compute_project_id(self):
        for ag in self:
            project = self.env["project.project"].search([("agreement_id", "=", ag.id)])
            ag.project_id = project
