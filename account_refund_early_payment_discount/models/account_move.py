# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _early_payment_discount_move_types(self):
        res = super()._early_payment_discount_move_types()
        res += ("out_refund", "in_refund")
        return res
