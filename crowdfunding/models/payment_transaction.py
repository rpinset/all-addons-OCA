# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    crowdfunding_challenge_id = fields.Many2one(
        related="invoice_ids.crowdfunding_challenge_id"
    )

    def _post_process(self):
        for this in self:
            if not this.crowdfunding_challenge_id or this.state != "done":
                continue
            this._post_process_crowdfunding()
        return super()._post_process()

    def _post_process_crowdfunding(self):
        pass
