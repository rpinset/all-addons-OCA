# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaquilaProgram(models.Model):
    _inherit = "l10n_py.maquila.program"

    cnime_report_ids = fields.One2many(
        "l10n_py.maquila.cnime.report",
        "program_id",
        string="CNIME Reports",
    )
    cnime_report_count = fields.Integer(compute="_compute_cnime_report_count")

    @api.depends("cnime_report_ids")
    def _compute_cnime_report_count(self):
        for rec in self:
            rec.cnime_report_count = len(rec.cnime_report_ids)

    def action_view_cnime_reports(self):
        return {
            "type": "ir.actions.act_window",
            "name": "CNIME Reports",
            "res_model": "l10n_py.maquila.cnime.report",
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id)],
            "context": {"default_program_id": self.id},
        }
