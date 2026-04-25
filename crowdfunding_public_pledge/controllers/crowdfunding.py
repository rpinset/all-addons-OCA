# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import werkzeug

from odoo import http
from odoo.http import request

from odoo.addons.crowdfunding.controllers import main


class CrowdfundingController(main.CrowdfundingController):
    @http.route(
        [
            "/crowdfunding/<model('crowdfunding.challenge'):challenge>/pledge/<int:partner_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def pledge_detail(self, challenge, partner_id):
        partner = request.env["res.partner"].browse(partner_id).sudo()
        invoices = (
            challenge._filtered_access("read")
            .sudo()
            .invoice_ids.filtered(
                lambda x: x.payment_state == "paid"
                and x.crowdfunding_public
                and x.partner_id.commercial_partner_id == partner
            )
        )
        if not invoices:
            raise werkzeug.exceptions.NotFound()
        return request.render(
            "crowdfunding_public_pledge.pledge_detail",
            {
                "object": challenge,
                "partner": partner.sudo(),
                "pledge_amount": sum(invoices.mapped("amount_total")),
                "currency": invoices.currency_id[:1],
            },
        )
