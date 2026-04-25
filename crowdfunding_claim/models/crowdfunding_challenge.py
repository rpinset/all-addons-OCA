# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class CrowdfundingChallenge(models.Model):
    _inherit = "crowdfunding.challenge"

    def _claim(self, partner=None):
        partner = partner or self.env.user.partner_id
        can_claim = self.filtered(lambda x: x._can_claim(partner))
        can_claim.write(
            {
                "claimed_partner_id": partner.id,
            }
        )
        can_claim.action_claimed()

    def _can_claim(self, partner=None):
        self.ensure_one()
        return not self.claimed_partner_id and self.state == "open"
