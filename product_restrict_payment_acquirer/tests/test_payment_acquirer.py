# Copyright Cetmix OU 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPaymentProvider(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Initialize providers
        cls.paypal = cls.env.ref("payment.payment_provider_paypal")
        cls.paypal.write({"state": "test"})
        cls.providers = cls.env["payment.provider"].search(
            [("state", "in", ["enabled", "test"])]
        )
        cls.wire_transfer = cls.env.ref("payment.payment_provider_transfer")
        cls.wire_transfer.write({"state": "enabled"})

        # Initialize partner restrictions
        cls.res_partner_deco = cls.env.ref("base.res_partner_2")
        cls.res_partner_deco.write(
            {"allowed_payment_provider_ids": [(4, cls.wire_transfer.id)]}
        )

        # Create products with provider restrictions
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test Product 1",
                "allowed_payment_provider_ids": [
                    (4, cls.wire_transfer.id),
                    (4, cls.paypal.id),
                ],
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Test Product 2",
                "allowed_payment_provider_ids": [(4, cls.paypal.id)],
            }
        )

        # Create a sale order with two lines
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.res_partner_deco.id,
                "order_line": [
                    (0, 0, {"product_id": cls.product_1.id, "product_uom_qty": 1.0}),
                    (0, 0, {"product_id": cls.product_2.id, "product_uom_qty": 1.0}),
                ],
            }
        )

    def test_blank_mode(self):
        """Test blank mode falls back to partner restrictions"""
        self.env["ir.config_parameter"].set_param(
            "product_acquirer_settings.product_acquirer_restriction_mode", False
        )

        # With order - should respect partner restrictions
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
            order_id=self.order.id,
        )
        self.assertEqual(providers, self.wire_transfer)

        # Without order - should return all providers
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
        )
        self.assertEqual(providers, self.wire_transfer | self.paypal)

    def test_first_mode(self):
        """Test first product mode"""
        self.env["ir.config_parameter"].set_param(
            "product_acquirer_settings.product_acquirer_restriction_mode", "first"
        )

        # With order - should respect first product restrictions
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
            order_id=self.order.id,
        )
        self.assertEqual(providers, self.wire_transfer | self.paypal)

        # Without order - should return all providers
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
        )
        self.assertEqual(providers, self.wire_transfer | self.paypal)

    def test_all_mode(self):
        """Test all products mode"""
        self.env["ir.config_parameter"].set_param(
            "product_acquirer_settings.product_acquirer_restriction_mode", "all"
        )

        # With order - should respect common providers for all products
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
            order_id=self.order.id,
        )
        self.assertEqual(providers, self.paypal)

        # Without order - should return all providers
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
        )
        self.assertEqual(providers, self.wire_transfer | self.paypal)

    def test_fallback_behavior(self):
        """Test fallback behavior when no providers match restrictions"""
        # Set mode to 'all' but remove paypal from product 2
        self.env["ir.config_parameter"].set_param(
            "product_acquirer_settings.product_acquirer_restriction_mode", "all"
        )
        self.product_2.allowed_payment_provider_ids = False

        # Should fall back to partner restrictions
        providers = self.env["payment.provider"]._get_compatible_providers(
            company_id=self.env.company.id,
            partner_id=self.res_partner_deco.id,
            amount=100,
            order_id=self.order.id,
        )
        self.assertEqual(providers, self.wire_transfer)
