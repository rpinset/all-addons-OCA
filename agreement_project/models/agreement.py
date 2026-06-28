# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    task_count = fields.Integer("# Tasks", compute="_compute_task_count")
    project_ids = fields.One2many(
        "project.project",
        "agreement_id",
        string="Projects",
    )

    @api.depends("project_ids.tasks.agreement_id")
    def _compute_task_count(self):
        groups = self.env["project.task"]._read_group(
            [("agreement_id", "in", self.ids)],
            groupby=["agreement_id"],
            aggregates=["__count"],
        )
        counts = {agreement.id: count for agreement, count in groups}
        for ag in self:
            ag.task_count = counts.get(ag.id, 0)
