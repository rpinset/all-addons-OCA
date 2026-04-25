# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    crowdfunding_challenge_id = fields.Many2one("crowdfunding.challenge", index=True)
    crowdfunding_vendor_amount = fields.Monetary(
        related="crowdfunding_challenge_id.vendor_amount"
    )
    crowdfunding_target_amount = fields.Monetary(
        related="crowdfunding_challenge_id.target_amount"
    )
    crowdfunding_pledged_amount = fields.Monetary(
        related="crowdfunding_challenge_id.pledged_amount"
    )
