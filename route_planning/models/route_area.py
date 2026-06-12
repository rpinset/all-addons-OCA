# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models


class RouteArea(models.Model):
    _name = "route.area"
    _description = "Route Area"
    _rec_names_search = ["code", "name"]

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    user_id = fields.Many2one("res.users")
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    time_start = fields.Float()
    waiting_time = fields.Float(
        help="Average waiting time at each stop, expressed in minutes."
    )
    auto_assign = fields.Boolean(
        help="Automatically assign this area to partners matching its criteria, "
        "based on country, state, and zip code range."
    )
    country_ids = fields.Many2many(comodel_name="res.country")
    state_ids = fields.Many2many(
        comodel_name="res.country.state", domain="[('country_id', 'in', country_ids)]"
    )
    zip_ids = fields.One2many("route.area.zip", "route_area_id", string="Zip ranges")

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code, company_id)",
            "The code must be unique per company.",
        ),
    ]

    @api.onchange("country_ids")
    def _onchange_country_ids(self):
        self.state_ids -= self.state_ids.filtered(
            lambda state: state._origin.id not in self.country_ids.state_ids.ids
        )

    def _match_address(self, partner):
        self.ensure_one()
        if self.country_ids and partner.country_id not in self.country_ids:
            return False
        if self.state_ids and partner.state_id not in self.state_ids:
            return False
        # filter by zip code range
        if self.zip_ids:
            if not partner.zip:
                return False
            # Extract only numbers from the zip code
            partner_zip = re.sub(r"\D", "", partner.zip)
            if not partner_zip:
                return False
            partner_zip_int = int(partner_zip)
            # Check if partner ZIP matches ANY of the defined ranges
            matches_any_range = False
            for zip_range in self.zip_ids:
                zip_from = re.sub(r"\D", "", zip_range.zip_from)
                zip_to = re.sub(r"\D", "", zip_range.zip_to)
                # Check if partner ZIP is within this range
                in_range = True
                if zip_from and partner_zip_int < int(zip_from):
                    in_range = False
                if zip_to and partner_zip_int > int(zip_to):
                    in_range = False
                if in_range:
                    matches_any_range = True
                    break
            if not matches_any_range:
                return False
        return True

    def _get_specificity_score(self):
        """Calculate specificity score for area prioritization.
        Higher score = more specific area.
        """
        self.ensure_one()
        score = 0
        # ZIP range adds most specificity
        if self.zip_ids:
            score += 100
        # State adds medium specificity
        if self.state_ids:
            score += 10
        # Country adds basic specificity
        if self.country_ids:
            score += 1
        return score


class RouteAreaZip(models.Model):
    _name = "route.area.zip"
    _description = "Route Area Zip range"

    route_area_id = fields.Many2one(
        comodel_name="route.area",
        required=True,
        ondelete="cascade",
    )
    zip_from = fields.Char(required=True)
    zip_to = fields.Char(required=True)
