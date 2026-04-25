# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import http
from odoo.http import request


class CrowdfundingController(http.Controller):
    @http.route(["/crowdfunding"], type="http", auth="public", website=True)
    def list(self):
        values = self._list_render_context()
        return request.render("crowdfunding.template_challenge_list", values)

    def _list_render_context(self):
        CrowdfundingChallenge = request.env["crowdfunding.challenge"]
        return {
            "results": CrowdfundingChallenge.search(
                request.env.user._is_public()
                and CrowdfundingChallenge._domain_website_access()
                or CrowdfundingChallenge._domain_portal_access()
            ),
        }

    @http.route(
        ["/crowdfunding/<model('crowdfunding.challenge'):challenge>"],
        type="http",
        auth="public",
        website=True,
    )
    def detail(self, challenge):
        values = self._detail_render_context(challenge)
        return request.render("crowdfunding.template_challenge_detail", values)

    def _detail_render_context(self, challenge, **kwargs):
        payment_access_token = None
        return {
            "object": challenge,
            "main_object": challenge,
            "payment_access_token": payment_access_token,
        }
