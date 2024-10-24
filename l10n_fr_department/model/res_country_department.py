# Copyright 2013-2022 GRAP (http://www.grap.coop)
# Copyright 2015-2022 Akretion France (http://www.akretion.com)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Alexis de Lattre (alexis.delattre@akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCountryDepartment(models.Model):
    _description = "Department"
    _name = "res.country.department"
    _order = "country_id, code"

    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        required=True,
        help="State related to the current department",
    )
    country_id = fields.Many2one(
        "res.country",
        related="state_id.country_id",
        string="Country",
        store=True,
        help="Country of the related state",
    )
    name = fields.Char(string="Department Name", size=128, required=True)
    code = fields.Char(
        string="Department Code",
        size=3,
        required=True,
        help="The department code (ISO 3166-2 codification)",
    )

    _sql_constraints = [
        (
            "code_uniq",
            "unique (code)",
            "You cannot have two departments with the same code!",
        )
    ]

    @api.depends("name", "code")
    def _compute_display_name(self):
        for rec in self:
            dname = f"{rec.name} ({rec.code})"
            rec.display_name = dname

    @api.model
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        if domain is None:
            domain = []
        if name and operator == "ilike":
            ids = list(
                self._search([("code", "=", name)] + domain, limit=limit, order=order)
            )
            if ids:
                return ids
        return super()._name_search(
            name, domain=domain, operator=operator, limit=limit, order=order
        )
