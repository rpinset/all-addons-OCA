# Copyright 2025 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ShopfloorMenu(models.Model):
    _inherit = "shopfloor.menu"

    ignore_expiration_date_is_possible = fields.Boolean(
        compute="_compute_ignore_expiration_date_is_possible"
    )
    ignore_expiration_date = fields.Boolean(
        string="Ignore expiration date",
        default=False,
        help="Allow to reserve goods from expired lots.",
    )

    @api.depends("scenario_id")
    def _compute_ignore_expiration_date_is_possible(self):
        for menu in self:
            menu.ignore_expiration_date_is_possible = menu.scenario_id.has_option(
                "allow_ignore_expiration_date"
            )
