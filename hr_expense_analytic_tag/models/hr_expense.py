# Copyright 2023-2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import Command, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    analytic_tag_ids = fields.Many2many(
        comodel_name="account.analytic.tag",
        string="Analytic Tags",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    def _prepare_move_line_vals(self):
        vals = super()._prepare_move_line_vals()
        if self.analytic_tag_ids:
            vals.update(analytic_tag_ids=[Command.set(self.analytic_tag_ids.ids)])
        return vals


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _prepare_payment_vals(self):
        vals = super()._prepare_payment_vals()
        expense_model = self.env["hr.expense"]
        for line in vals["line_ids"]:
            if not line[2].get("expense_id"):
                continue
            expense = expense_model.browse(line[2]["expense_id"])
            if expense.analytic_tag_ids:
                line[2].update(
                    analytic_tag_ids=[Command.set(expense.analytic_tag_ids.ids)]
                )
        return vals
