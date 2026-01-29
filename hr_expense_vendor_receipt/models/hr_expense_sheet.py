# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import models


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _prepare_bills_vals(self):
        result = super()._prepare_bills_vals()
        if self.journal_id.receipts:
            result.update({"move_type": "in_receipt"})
        return result

    def _do_reverse_moves(self):
        moves_receipts_sudo = self.sudo().account_move_ids.filtered_domain(
            [
                ("state", "=", "posted"),
                ("journal_id.receipts", "=", True),
            ]
        )
        moves_receipts_sudo.button_draft()
        # These draft receipts will be deleted when "_do_reverse_moves" happen
        return super()._do_reverse_moves()
