# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    account_reconcile_exclude_account_ids = fields.Many2many(
        comodel_name="account.account",
        relation="journal_account_reconciliation_exclude_rel",
        string="Accounts excluded from reconciliation",
        help="Journal items that can be reconciled will not have these accounts.",
    )
