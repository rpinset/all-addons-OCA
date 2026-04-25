# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import werkzeug

from odoo import http
from odoo.http import request

from odoo.addons.crowdfunding.controllers import main as crowdfunding_main


class CrowdfundingController(crowdfunding_main.CrowdfundingController):
    @http.route(
        ["/crowdfunding/<model('crowdfunding.challenge'):challenge>/claim"],
        type="http",
        auth="user",
        website=True,
    )
    def claim(self, challenge):
        if challenge._can_claim(request.env.user.partner_id):
            challenge.sudo()._claim(request.env.user.partner_id)
            values = self._detail_render_context(challenge)
            values["hide_discuss"] = True
            return request.render("crowdfunding.template_challenge_detail", values)
        else:
            # TODO nicer error
            raise werkzeug.exceptions.NotFound()
