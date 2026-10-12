# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaquilaProgram(models.Model):
    _inherit = "l10n_py.maquila.program"

    admission_ids = fields.One2many(
        "l10n_py.maquila.admission",
        "program_id",
        string="Admissions",
    )
    admission_count = fields.Integer(compute="_compute_admission_count")
    export_ids = fields.One2many(
        "l10n_py.maquila.export",
        "program_id",
        string="Exports",
    )
    export_count = fields.Integer(compute="_compute_export_count")
    guarantee_ids = fields.One2many(
        "l10n_py.maquila.guarantee",
        "program_id",
        string="Guarantees",
    )
    guarantee_count = fields.Integer(compute="_compute_guarantee_count")

    @api.depends("admission_ids")
    def _compute_admission_count(self):
        for rec in self:
            rec.admission_count = len(rec.admission_ids)

    @api.depends("export_ids")
    def _compute_export_count(self):
        for rec in self:
            rec.export_count = len(rec.export_ids)

    @api.depends("guarantee_ids")
    def _compute_guarantee_count(self):
        for rec in self:
            rec.guarantee_count = len(rec.guarantee_ids)

    def action_view_admissions(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Admissions",
            "res_model": "l10n_py.maquila.admission",
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id)],
            "context": {"default_program_id": self.id},
        }

    def action_view_exports(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Exports",
            "res_model": "l10n_py.maquila.export",
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id)],
            "context": {"default_program_id": self.id},
        }

    def action_view_guarantees(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Guarantees",
            "res_model": "l10n_py.maquila.guarantee",
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id)],
            "context": {"default_program_id": self.id},
        }
