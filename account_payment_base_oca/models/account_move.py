# Copyright 2024-2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    bank_account_required = fields.Boolean(
        related="preferred_payment_method_line_id.payment_method_id.bank_account_required",
    )
    payment_method_code = fields.Char(
        related="preferred_payment_method_line_id.payment_method_id.code", store=True
    )

    @api.depends("bank_partner_id", "preferred_payment_method_line_id")
    def _compute_partner_bank_id(self):
        res = super()._compute_partner_bank_id()
        for invoice in self.filtered(
            lambda inv: inv.is_inbound()
            and inv.preferred_payment_method_line_id.journal_id.bank_account_id
        ):
            invoice.partner_bank_id = (
                invoice.preferred_payment_method_line_id.journal_id.bank_account_id
            )
        return res
