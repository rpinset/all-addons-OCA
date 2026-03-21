# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import re

from odoo import api, models
from odoo.tools.rendering_tools import parse_inline_template, render_inline_template


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("country_id")
    def _compute_street_data(self):
        without_country = self.browse([])
        for this in self:
            if not this.country_id.partner_street_number_regex:
                without_country += this
                continue
            this._partner_street_number_parse()
        return super(ResPartner, without_country)._compute_street_data()

    def _partner_street_number_parse(self):
        """
        Parse street into split fields for one record
        """
        self.ensure_one()
        try:
            match = re.match(
                self.country_id.partner_street_number_regex or "",
                (self.street or "").strip(),
            )
        except re.error:
            match = False
        self.update(
            match.groupdict()
            if match
            else {
                "street_name": self.street,
                "street_number": False,
                "street_number2": False,
            }
        )
        return match

    def _inverse_street_data(self):
        without_country = self.browse([])
        for this in self:
            if not this.country_id.partner_street_number_format:
                without_country += this
                continue
            this._partner_street_number_format()
        return super(ResPartner, without_country)._inverse_street_data()

    def _partner_street_number_format(self):
        """
        Format street from split fields for one record
        """
        try:
            self.street = render_inline_template(
                parse_inline_template(self.country_id.partner_street_number_format),
                {"object": self},
            ).strip()
        except Exception:
            self.street = self.street_name or getattr(self, "_origin", self).street
