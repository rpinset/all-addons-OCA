# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _search_get_details(self, search_type, order, options):
        result = super()._search_get_details(search_type, order, options)
        if search_type in ("crowdfunding", "all"):
            result.append(
                self.env["crowdfunding.challenge"]._search_get_detail(
                    self, order, options
                )
            )
        return result
