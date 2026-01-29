# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www

from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = "crm.team"

    enable_zip_auto_assignment = fields.Boolean(
        string="Enable Auto ZIP Assignment",
        default=False,
        help="If checked, this team will be considered for automatic assignment "
        "based on ZIP code patterns.",
    )

    country_ids = fields.Many2many(
        "res.country",
        string="Countries",
        help="Countries where this team operates",
        default=lambda self: self.env.company.country_id.ids,
    )
    state_ids = fields.Many2many(
        "res.country.state", string="States", help="States where this team operates"
    )

    zip_regex_ids = fields.One2many(
        comodel_name="crm.team.zip.pattern",
        inverse_name="team_id",
        string="ZIP Regex",
        help="Regular expression patterns to match partner ZIP codes",
    )

    zip_assignment_priority = fields.Integer(
        string="Assignment Priority",
        default=0,
        help="Higher priority teams will be preferred when multiple teams "
        "match the same ZIP code. Higher number = higher priority.",
    )

    pre_zip_match_condition = fields.Char(
        string="Pre-Zip Match Condition",
        help=(
            "If present, this condition must be satisfied before "
            "matching the zip regular expression."
        ),
    )

    @api.onchange("country_ids")
    def _onchange_countries(self):
        if self.country_ids:
            domain = [("country_id", "in", self.country_ids.ids)]
            self.state_ids = [Command.clear()]
        else:
            domain = []
        return {"domain": {"state_ids": domain}}

    @api.onchange("company_id")
    def _onchange_company_id(self):
        self.country_ids = [Command.clear()]
        self.state_ids = [Command.clear()]
        if self.company_id:
            self.country_ids = [Command.set([self.company_id.country_id.id])]

    @api.constrains("enable_zip_auto_assignment", "company_id")
    def _check_enable_zip_auto_assignment(self):
        for team in self:
            if team.enable_zip_auto_assignment and not team.company_id:
                raise ValidationError(
                    _(
                        "A company must be set if "
                        "'Enable Auto ZIP Assignment' is checked."
                    )
                )
