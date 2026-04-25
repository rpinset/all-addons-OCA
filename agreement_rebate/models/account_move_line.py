# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import format_date


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    agreement_rebate_settlement_line_ids = fields.Many2many(
        comodel_name="agreement.rebate.settlement.line",
        relation="agreement_rebate_settlement_line_account_invoice_line_rel",
        column1="invoice_line_id",
        column2="settlement_line_id",
        string="Settlement lines",
    )

    @api.depends("agreement_rebate_settlement_line_ids.settlement_id")
    def _compute_name(self):
        res = super()._compute_name()
        for line in self:
            if not line.name:
                continue
            settlements = line.agreement_rebate_settlement_line_ids.settlement_id
            if len(settlements) == 1:
                date_from = format_date(self.env, settlements.date_from)
                date_to = format_date(self.env, settlements.date_to)
                line.name += " - " + self.env._("Period: %s - %s", date_from, date_to)
        return res
