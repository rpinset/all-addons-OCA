# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


import werkzeug

from odoo import _, http
from odoo.http import request

from odoo.addons.payment.controllers.portal import WebsitePayment


class Payment(WebsitePayment):
    def _crowdfunding_get_partner(self):
        return (
            not request.env.user._is_public()
            and request.env.user.partner_id
            or request.env["res.partner"].browse(
                request.session.get("crowdfunding", {}).get("partner_id", [])
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
        request.session.setdefault("crowdfunding", {})["partner_id"] = partner.id
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
            PaymentLinkWizard = request.env["payment.link.wizard"]
            invoice = challenge.sudo()._out_invoice(
                partner,
                abs(float(kwargs["amount"])),
                **self._crowdfunding_get_out_invoice_kwargs(challenge, partner, kwargs)
            )
            invoice.action_post()

            wizard_vals = PaymentLinkWizard.with_context(
                active_model=invoice._name,
                active_id=invoice.id,
            ).default_get(PaymentLinkWizard._fields)

            payment_wizard = PaymentLinkWizard.new(wizard_vals)

            payment_wizard._compute_values()
            kwargs["amount"] = invoice.amount_total
            kwargs["access_token"] = payment_wizard.access_token
            kwargs["company_id"] = invoice.company_id.id
            kwargs["currency_id"] = challenge.currency_id.id
            kwargs["invoice_id"] = invoice.id
            kwargs["partner_id"] = partner.id
            kwargs["reference"] = "crowdfunding/%s/%s" % (
                challenge.id,
                partner.id,
            )
            result = self.pay(**kwargs)
        return result
