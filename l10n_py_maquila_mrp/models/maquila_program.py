# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MaquilaProgram(models.Model):
    _inherit = "l10n_py.maquila.program"

    def _maquila_van_for_period(self, period_start, period_end):
        """National added value for a period, shared by the VAN wizard and the
        CNIME report so both report the same figure. Requires an analytic
        account and at least one completed production to determine the
        origin split of the cost. Returns a dict."""
        self.ensure_one()
        if not self.analytic_account_id:
            raise UserError(
                _(
                    "Program %(program)s has no analytic account configured.",
                    program=self.code,
                )
            )
        analytic_lines = self.env["account.analytic.line"].search(
            [
                ("account_id", "=", self.analytic_account_id.id),
                ("date", ">=", period_start),
                ("date", "<=", period_end),
            ]
        )
        total = sum(abs(line.amount) for line in analytic_lines)
        productions = self.env["mrp.production"].search(
            [
                ("l10n_py_maquila_program_id", "=", self.id),
                ("date_start", ">=", period_start),
                ("date_start", "<=", period_end),
                ("state", "=", "done"),
            ]
        )
        if not productions:
            raise UserError(
                _(
                    "Cannot compute the VAN for program %(program)s: there is no "
                    "completed production in the period, so the origin split of "
                    "the cost cannot be determined.",
                    program=self.code,
                )
            )
        national = mercosul = imported = 0.0
        for production in productions:
            for move in production.move_raw_ids.filtered(lambda m: m.state == "done"):
                bom_line = production.bom_id.bom_line_ids.filtered(
                    lambda bl, p=move.product_id: bl.product_id == p
                )[:1]
                origin = bom_line.l10n_py_origin_type if bom_line else "imported"
                cost = abs(sum(move.stock_valuation_layer_ids.mapped("value")))
                if origin == "national_py":
                    national += cost
                elif origin == "national_mercosul":
                    mercosul += cost
                else:
                    imported += cost
        return {
            "total_cost": total,
            "national_cost": national,
            "mercosul_cost": mercosul,
            "imported_cost": imported,
            "van_amount": total - mercosul - imported,
        }

    bom_ids = fields.One2many(
        "mrp.bom",
        "l10n_py_maquila_program_id",
        string="Bills of Materials",
    )
    bom_count = fields.Integer(compute="_compute_bom_count")
    production_ids = fields.One2many(
        "mrp.production",
        "l10n_py_maquila_program_id",
        string="Productions",
    )
    production_count = fields.Integer(compute="_compute_production_count")
    waste_ids = fields.One2many(
        "l10n_py.maquila.waste",
        "program_id",
        string="Waste Records",
    )
    waste_count = fields.Integer(compute="_compute_waste_count")

    @api.depends("bom_ids")
    def _compute_bom_count(self):
        for rec in self:
            rec.bom_count = len(rec.bom_ids)

    @api.depends("production_ids")
    def _compute_production_count(self):
        for rec in self:
            rec.production_count = len(rec.production_ids)

    @api.depends("waste_ids")
    def _compute_waste_count(self):
        for rec in self:
            rec.waste_count = len(rec.waste_ids)

    def action_view_boms(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Bills of Materials",
            "res_model": "mrp.bom",
            "view_mode": "list,form",
            "domain": [("l10n_py_maquila_program_id", "=", self.id)],
            "context": {"default_l10n_py_maquila_program_id": self.id},
        }

    def action_view_productions(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Productions",
            "res_model": "mrp.production",
            "view_mode": "list,form",
            "domain": [("l10n_py_maquila_program_id", "=", self.id)],
        }

    def action_view_waste(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Waste Records",
            "res_model": "l10n_py.maquila.waste",
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id)],
            "context": {"default_program_id": self.id},
        }
