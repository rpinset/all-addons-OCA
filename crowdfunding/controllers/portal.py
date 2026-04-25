# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import http

from odoo.addons.account.controllers import portal


class Portal(portal.PortalAccount):
    def _get_account_searchbar_filters(self):
        result = super()._get_account_searchbar_filters()
        result["crowdfunding_pledge"] = {
            "label": http.request.env._("Crowdfunding pledges"),
            "domain": [
                ("move_type", "=", "out_invoice"),
                ("crowdfunding_challenge_id", "!=", False),
            ],
        }
        return result
