# Copyright Cetmix OU 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    @api.model
    def _get_compatible_providers(
        self, company_id, partner_id, amount, currency_id=None, **kwargs
    ):
        # All providers matching state (enabled|test)
        all_providers = self.search([("state", "in", ["enabled", "test"])])
        order_id = kwargs.get("order_id") or kwargs.get("sale_order_id")
        mode = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_acquirer_settings.product_acquirer_restriction_mode")
        )

        # No order => always return all providers
        if not order_id:
            return all_providers

        # Otherwise get standard (partner) filtering
        providers = super()._get_compatible_providers(
            company_id, partner_id, amount, currency_id=currency_id, **kwargs
        )

        # Blank mode => fallback to partner restrictions
        if not mode:
            return providers

        # First-product mode
        if mode == "first":
            first_pps = (
                self.env["sale.order"]
                .browse(order_id)
                .order_line[:1]
                .mapped("product_id.allowed_payment_provider_ids")
            )
            return first_pps or providers

        # All-products mode
        if mode == "all":
            allowed = False
            for line in self.env["sale.order"].browse(order_id).order_line:
                pps = line.product_id.allowed_payment_provider_ids
                allowed = (allowed & pps) if allowed else pps
            return allowed or providers

        # Fallback
        return providers
