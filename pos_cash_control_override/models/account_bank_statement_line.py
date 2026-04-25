# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get(
            "override_cash_control_permissions"
        ) and self.user_has_groups("point_of_sale.group_pos_user"):
            self = self.sudo()
        return super().create(vals_list)
