# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo.addons.crowdfunding.controllers import payment as crowdfunding_payment


class Payment(crowdfunding_payment.Payment):
    def _crowdfunding_get_out_invoice_kwargs(self, challenge, partner, kwargs):
        args = super()._crowdfunding_get_out_invoice_kwargs(challenge, partner, kwargs)
        return dict(args, public=bool(kwargs.get("public")))
