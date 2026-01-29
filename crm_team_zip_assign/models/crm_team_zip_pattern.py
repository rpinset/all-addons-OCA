# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmTeamZipPattern(models.Model):
    _name = "crm.team.zip.pattern"
    _description = "CRM Team ZIP Pattern"
    _order = "team_id, id"

    name = fields.Char(compute="_compute_name", store=True)

    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="CRM Team",
        required=True,
        ondelete="cascade",
    )
    pattern = fields.Char(
        string="ZIP Pattern",
        required=True,
        help="Python regular expression pattern to match ZIP codes. "
        "Example: '^1[0-5].*' for ZIP codes starting with 10-15",
    )

    _sql_constraints = [
        (
            "unique_team_id_pattern_combination",
            "UNIQUE(team_id, pattern)",
            _("The pattern has already been assigned to this team."),
        )
    ]

    @api.depends("team_id", "pattern")
    def _compute_name(self):
        for record in self:
            name = f"{record.team_id.name} - {record.pattern}"
            record.name = name

    @api.constrains("pattern")
    def _check_pattern_validity(self):
        """Validate that the pattern is a valid Python regex."""
        for record in self:
            if record.pattern:
                try:
                    re.compile(record.pattern)
                except re.error as e:
                    raise ValidationError(
                        f"Invalid regex pattern '{record.pattern}': {str(e)}"
                    ) from e
