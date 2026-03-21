# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    partner_street_number_regex = fields.Char(
        string="Parse regex",
        help="Regular expression to parse street_* fields from the street field. "
        "Should contain at least a (?P<street_name>...) group.",
    )
    partner_street_number_format = fields.Char(
        string="Format expression",
        help="Template expression to fill the street field from street_* fields. "
        "Should contain at least {{object.street_name}}.",
    )
    partner_street_number_test_value = fields.Char(
        "Full street (for testing)",
        store=False,
    )
    partner_street_number_test_result = fields.Html(
        compute="_compute_partner_street_number_test_result",
    )

    @api.depends(
        "partner_street_number_regex",
        "partner_street_number_format",
        "partner_street_number_test_value",
    )
    def _compute_partner_street_number_test_result(self):
        ResPartner = self.env["res.partner"]
        for this in self:
            partner_vals = {
                "street": self.partner_street_number_test_value,
                "country_id": this,
            }
            partner_regex = ResPartner.new(partner_vals)
            partner_regex._compute_street_data()
            partner_format = ResPartner.new(partner_regex._cache)
            partner_format._inverse_street_data()
            this.partner_street_number_test_result = self.env["ir.qweb"]._render(
                "partner_street_number.template_test_result",
                {
                    "partner_regex": partner_regex,
                    "partner_format": partner_format,
                },
            )
