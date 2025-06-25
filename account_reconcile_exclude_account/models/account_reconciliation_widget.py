# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class AccountReconciliationWidget(models.AbstractModel):
    _inherit = "account.reconciliation.widget"

    @api.model
    def _domain_move_lines_for_reconciliation(
        self,
        st_line,
        aml_accounts,
        partner_id,
        excluded_ids=None,
        search_str=False,
        mode="rp",
    ):
        domain = super()._domain_move_lines_for_reconciliation(
            st_line,
            aml_accounts,
            partner_id,
            excluded_ids=excluded_ids,
            search_str=search_str,
            mode=mode,
        )
        excluded_accounts = st_line.journal_id.account_reconcile_exclude_account_ids
        if excluded_accounts:
            domain = expression.AND(
                [
                    domain,
                    [
                        ("account_id", "not in", excluded_accounts.ids),
                    ],
                ]
            )
        return domain
