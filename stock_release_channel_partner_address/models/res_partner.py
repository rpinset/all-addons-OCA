# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models
from odoo.osv.expression import AND, OR


class ResPartner(models.Model):
    _inherit = "res.partner"

    @property
    def _release_channel_possible_candidate_domain(self):
        # OVERRIDE: allow only channels matching the partner's address
        # For both country and state, a match is achieved if:
        # - the partner's country or state is included in the channel's ones
        # - the partner's country or state is not defined
        domain = super()._release_channel_possible_candidate_domain
        country_domain = [("country_ids", "=", False)]
        if self.country_id:
            country_domain = OR(
                [country_domain, [("country_ids", "in", self.country_id.ids)]]
            )
        state_domain = [("state_ids", "=", False)]
        if self.state_id:
            state_domain = OR([state_domain, [("state_ids", "in", self.state_id.ids)]])
        return AND([domain, country_domain, state_domain])
