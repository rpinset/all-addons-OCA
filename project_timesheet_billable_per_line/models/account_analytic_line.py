# Copyright 2026 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, _, fields, models
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    is_billable = fields.Boolean("Billable")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line")

    def create_sale_orders(self):
        billable_lines = self.filtered(
            lambda x: x.is_billable and not x.sale_order_line_id
        )
        order_ids = []
        for account, lines in billable_lines.grouped("account_id").items():
            for partner, partner_lines in lines.grouped("partner_id").items():
                if not partner:
                    raise UserError(_("One or more lines have no customer set."))
                sale_order = self.env["sale.order"].create(
                    self.prepare_sale_order_vals(account, partner, partner_lines)
                )
                order_ids.append(sale_order.id)
                for order_line in sale_order.order_line:
                    product = order_line.product_id
                    partner_lines.filtered(
                        lambda line,
                        product=product: line.employee_id.timesheet_billable_product_id
                        == product
                    ).sale_order_line_id = order_line.id
        return {
            "type": "ir.actions.act_window",
            "name": _("Sales Orders"),
            "res_model": "sale.order",
            "view_mode": "tree,form",
            "domain": [("id", "in", order_ids)],
        }

    def prepare_sale_order_vals(self, account, partner, lines):
        line_vals = self.prepare_sale_order_line_vals(lines)
        return {
            "partner_id": partner.id,
            "analytic_account_id": account.id,
            "order_line": [Command.create(vals) for vals in line_vals],
        }

    def prepare_sale_order_line_vals(self, lines):
        vals = []
        for employee, emp_lines in lines.grouped("employee_id").items():
            if not employee.timesheet_billable_product_id:
                raise UserError(_(f"{employee} has no Timesheet Billable Product set."))
            description_parts = []
            for task, task_lines in emp_lines.grouped("task_id").items():
                descriptions = "\n".join(task_lines.mapped("name"))
                description_parts.append(f"{task.name}:\n{descriptions}")
            vals.append(
                {
                    "product_id": employee.timesheet_billable_product_id.id,
                    "product_uom_qty": sum(emp_lines.mapped("unit_amount")),
                    "name": "\n".join(description_parts),
                }
            )
        return vals
