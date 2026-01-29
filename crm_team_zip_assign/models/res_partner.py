# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
import logging
import re

from odoo import api, fields, models
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    exclude_from_zip_assign = fields.Boolean(
        string="Exclude from ZIP Assignment",
        default=False,
        help="If checked, this partner will not be automatically assigned "
        "to a CRM team based on ZIP code patterns.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._process_zip_assignment()
        return partners

    def write(self, vals):
        result = super().write(vals)
        if "zip" in vals or "company_id" in vals or "exclude_from_zip_assign" in vals:
            self._process_zip_assignment()
        return result

    def _process_zip_assignment(self):
        """Process ZIP assignment for multiple partners."""
        partners = self.filtered(
            lambda partner: partner.zip
            and partner.company_id
            and not partner.exclude_from_zip_assign
            and partner.country_id
            and partner.state_id
            and partner.type == "contact"
        )
        if partners:
            teams = self.env["crm.team"].search(
                [
                    ("enable_zip_auto_assignment", "=", True),
                    ("zip_regex_ids", "!=", False),
                    ("company_id", "!=", False),
                    ("country_ids", "!=", False),
                    ("state_ids", "!=", False),
                ]
            )
            for partner in partners:
                selected_team = self._select_team_for_partner(partner, teams)
                if selected_team:
                    _logger.info(
                        "Auto-assigning partner '%s' (ZIP: %s) to team '%s'",
                        partner.name,
                        partner.zip,
                        selected_team.name,
                    )
                    partner.team_id = selected_team.id
        return True

    def _select_team_for_partner(self, partner, teams):
        """Select the best CRM team for a partner based on ZIP and location."""
        eligible_teams = teams.filtered(
            lambda team: (
                team.company_id == partner.company_id
                and team.country_ids & partner.country_id
                and team.state_ids & partner.state_id
            )
        )
        matching_teams = self.env["crm.team"]
        for team in eligible_teams:
            # Evaluate pre_zip_match_condition if present, else always match
            if team.pre_zip_match_condition:
                partner_domain = ast.literal_eval(ustr(team.pre_zip_match_condition))
                domain_match = bool(partner.filtered_domain(partner_domain))
            else:
                domain_match = True
            if domain_match:
                if any(
                    re.match(pattern.pattern, partner.zip or "")
                    for pattern in team.zip_regex_ids
                ):
                    matching_teams |= team
        if matching_teams:
            matching_teams = matching_teams.sorted(
                key=lambda t: (-t.zip_assignment_priority, t.id)
            )
            return matching_teams[:1]
        return False
