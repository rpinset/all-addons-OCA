# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


import werkzeug

from odoo import _, http
from odoo.http import request

from odoo.addons.payment.controllers.portal import PaymentPortal
from odoo.addons.payment.utils import generate_access_token


class Payment(PaymentPortal):
    def _crowdfunding_get_partner(self):
        return (
            not request.env.user._is_public()
            and request.env.user.partner_id
            or request.env["res.partner"].browse(
                request.session.get("crowdfunding_partner_id", [])
            )
        )

    def _crowdfunding_create_partner_mandatory_fields(self, challenge):
        return ("name", "email", "street", "city", "zip", "country_id")

    def _crowdfunding_create_partner_optional_fields(self, challenge):
        return ()

    def _crowdfunding_create_partner_get_errors(self, challenge, values):
        errors = {}
        for key in self._crowdfunding_create_partner_mandatory_fields(challenge):
            if not values.get(key):
                errors[key] = _("Required field")
        if (
            not str(values.get("country_id")).isdigit()
            or not request.env["res.country"].browse(int(values["country_id"])).exists()
        ):
            errors["country_id"] = _("Invalid country")

        return errors

    def _crowdfunding_create_partner_get_values(self, challenge, values):
        result = {
            key: values[key]
            for key in (
                self._crowdfunding_create_partner_mandatory_fields(challenge)
                + self._crowdfunding_create_partner_optional_fields(challenge)
            )
            if key in values
        }
        result["country_id"] = int(result["country_id"])
        return result

    def _crowdfunding_create_partner(self, challenge, values):
        Partner = request.env["res.partner"]
        if self._crowdfunding_create_partner_get_errors(challenge, values):
            return Partner
        partner = Partner.sudo().create(
            self._crowdfunding_create_partner_get_values(challenge, values)
        )
        request.session["crowdfunding_partner_id"] = partner.id
        return partner

    def _crowdfunding_get_out_invoice_kwargs(self, challenge, partner, kwargs):
        return {}

    @http.route(
        ["/crowdfunding/<model('crowdfunding.challenge'):challenge>/pay"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def crowdfunding_pay(self, challenge, **kwargs):
        if not challenge._can_pay(request.env.user.partner_id):
            raise werkzeug.exceptions.NotFound()

        partner = self._crowdfunding_get_partner() or self._crowdfunding_create_partner(
            challenge, kwargs
        )
        if not partner:
            return request.render(
                "crowdfunding.pay_partner_details",
                {
                    "object": challenge,
                    "form_values": kwargs,
                    "form_errors": kwargs
                    and self._crowdfunding_create_partner_get_errors(challenge, kwargs)
                    or {},
                },
            )
        elif "amount" not in kwargs:
            result = request.render("crowdfunding.pay_details", {"object": challenge})
        else:
            invoice = challenge.sudo()._out_invoice(
                partner,
                abs(float(kwargs["amount"])),
                **self._crowdfunding_get_out_invoice_kwargs(challenge, partner, kwargs),
            )
            invoice.action_post()

            kwargs["amount"] = invoice.amount_total
            kwargs["access_token"] = generate_access_token(
                partner.id, invoice.amount_total, challenge.currency_id.id
            )
            kwargs["company_id"] = invoice.company_id.id
            kwargs["currency_id"] = challenge.currency_id.id
            kwargs["invoice_id"] = invoice.id
            kwargs["partner_id"] = partner.id
            result = self.payment_pay(**kwargs)
        return result
