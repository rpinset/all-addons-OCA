import ast

from odoo import fields, models
from odoo.osv import expression


class CrmTeam(models.Model):
    _inherit = "crm.team"

    def _compute_invoiced(self):
        if not self:
            return

        sales_team_invoiced_domain = self.env.company.sales_team_invoiced_domain
        if not sales_team_invoiced_domain:
            return super()._compute_invoiced()
        today = fields.Date.today()
        invoiced_domain = [
            ("move_type", "in", ["out_invoice", "out_refund", "out_receipt"]),
            ("team_id", "in", self.ids),
            ("date", ">=", fields.Date.to_string(today.replace(day=1))),
            ("date", "<=", fields.Date.to_string(today)),
        ]
        domain_list = ast.literal_eval(sales_team_invoiced_domain)
        invoiced_domain = expression.AND([invoiced_domain, domain_list])
        for team in self:
            team.invoiced = 0.0
            moves = self.env["account.move"].search(invoiced_domain)
            for move in moves:
                if move.team_id == team:
                    team.invoiced += move.amount_untaxed_signed
