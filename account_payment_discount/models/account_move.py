# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _is_eligible_for_early_payment_discount(self, currency, reference_date):
        ret = super()._is_eligible_for_early_payment_discount(currency, reference_date)

        # If payment is set to be with dicount, move should
        # be computed as if it was an early payment discount
        has_payment_with_discount = self.line_ids.filtered(
            lambda line: line.display_type == "payment_term"
        ).payment_line_ids.pay_with_discount

        return ret or has_payment_with_discount

    def _early_payment_discount_move_types(self):
        """Enable computation of disount on refunds"""
        res = super()._early_payment_discount_move_types()
        res += ("out_refund", "in_refund")
        return res
