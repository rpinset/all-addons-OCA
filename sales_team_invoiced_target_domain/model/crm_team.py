import ast

from odoo import fields, models
from odoo.osv import expression


class CrmTeam(models.Model):
    _inherit = "crm.team"

    def _prepare_invoice_domain(self):
        today = fields.Date.context_today(self.env.user)
        return [
            ("move_type", "in", ["out_invoice", "out_refund", "out_receipt"]),
            ("team_id", "in", self.ids),
            ("date", ">=", today.replace(day=1)),
            ("date", "<=", today),
        ]

    def _compute_invoiced(self):
        if not self:
            return
        domain_list = ast.literal_eval(self.env.company.sales_team_invoiced_domain)
        if not domain_list:
            return super()._compute_invoiced()
        invoiced_domain = expression.AND([self._prepare_invoice_domain(), domain_list])
        team_data = self.env["account.move"]._read_group(
            invoiced_domain,
            groupby=["team_id"],
            aggregates=["amount_untaxed_signed:sum"],
        )
        team_dict = dict(team_data)
        for team in self:
            team.invoiced = team_dict.get(team) or 0.0
