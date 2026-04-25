# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class CrowdfundingChallenge(models.Model):
    _inherit = "crowdfunding.challenge"

    def _out_invoice_vals(self, partner, amount, **kwargs):
        vals = super()._out_invoice_vals(partner, amount, **kwargs)
        vals["crowdfunding_public"] = kwargs.get("public")
        return vals
