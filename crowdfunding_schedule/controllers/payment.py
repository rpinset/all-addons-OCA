# Copyright 2026 Nexusai Solutions (OPC) Private Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import http
from odoo.http import request

from odoo.addons.crowdfunding.controllers.payment import PaymentPortal


class Payment(PaymentPortal):
    @http.route()
    def crowdfunding_pay(self, challenge, **kwargs):
        if not challenge._is_scheduled_active():
            return request.render(
                "crowdfunding_schedule.challenge_payment_datetime_unavailable",
                {"object": challenge},
            )

        return super().crowdfunding_pay(challenge, **kwargs)
