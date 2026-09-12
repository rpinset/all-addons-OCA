from datetime import timedelta
from unittest.mock import Mock, patch

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

from ..lib.client import ShopifyClient
from ..models import instance as instance_module

CLIENT_ID = "dev-dashboard-client-id"
CLIENT_SECRET = "dev-dashboard-client-secret"


class TestShopifyOnboardingCredentials(TransactionCase):
    """Cover both authentication modes offered by the onboarding wizard."""

    def _create_wizard(self, **values):
        return self.env["shopify.instance.wizard"].create(
            {
                "name": "Wizard Shop",
                "shop_url": "wizard-shop.myshopify.com",
                "webhook_secret": CLIENT_SECRET,
                "company_id": self.env.company.id,
                **values,
            }
        )

    def _patch_shopify_client(self):
        """Replace the HTTP client, leaving the access token flow untouched."""
        client = Mock()
        client.execute.return_value = {
            "shop": {
                "name": "Wizard Shop",
                "currencyCode": self.env.company.currency_id.name,
            }
        }
        client_class = Mock(return_value=client)
        # The model normalises shop domains through the real class method.
        client_class._normalise_shop_url = ShopifyClient._normalise_shop_url
        return patch.object(instance_module, "ShopifyClient", client_class)

    def _patch_token_request(self, **kwargs):
        return patch.object(instance_module, "request_access_token", **kwargs)

    def test_dev_dashboard_onboarding_needs_no_access_token(self):
        wizard = self._create_wizard(client_id=CLIENT_ID)

        with (
            self._patch_token_request(
                return_value={"access_token": "shpat-managed", "expires_in": 86399}
            ) as request_token,
            self._patch_shopify_client() as client_class,
        ):
            wizard.action_test_connection()

        instance = wizard.instance_id
        request_token.assert_called_once_with(
            "wizard-shop.myshopify.com", CLIENT_ID, CLIENT_SECRET
        )
        self.assertEqual(instance.client_id, CLIENT_ID)
        self.assertEqual(instance.access_token, "shpat-managed")
        self.assertTrue(instance.access_token_expires_at)
        self.assertEqual(client_class.call_args.args[1], "shpat-managed")
        self.assertEqual(instance.state, "connected")
        self.assertEqual(wizard.step, "scopes")

    def test_legacy_onboarding_keeps_requiring_a_static_token(self):
        wizard = self._create_wizard(access_token="shpat-static")

        with (
            self._patch_token_request() as request_token,
            self._patch_shopify_client() as client_class,
        ):
            wizard.action_test_connection()

        instance = wizard.instance_id
        request_token.assert_not_called()
        self.assertFalse(instance.client_id)
        self.assertEqual(instance.access_token, "shpat-static")
        self.assertFalse(instance.access_token_expires_at)
        self.assertEqual(client_class.call_args.args[1], "shpat-static")
        self.assertEqual(instance.state, "connected")
        self.assertEqual(wizard.step, "scopes")

    def test_onboarding_without_authentication_credentials_is_refused(self):
        wizard = self._create_wizard()

        with self._patch_token_request() as request_token:
            with self.assertRaises(UserError):
                wizard.action_test_connection()

        request_token.assert_not_called()
        self.assertFalse(wizard.instance_id)
        self.assertEqual(wizard.step, "credentials")

    def test_loading_a_managed_instance_keeps_its_fetched_token(self):
        instance = self.env["shopify.instance"].create(
            {
                "name": "Managed Shop",
                "shop_url": "managed-shop.myshopify.com",
                "client_id": CLIENT_ID,
                "webhook_secret": CLIENT_SECRET,
                "access_token": "shpat-fetched",
                "access_token_expires_at": fields.Datetime.now() + timedelta(hours=1),
            }
        )

        wizard = (
            self.env["shopify.instance.wizard"]
            .with_context(active_id=instance.id)
            .create({})
        )

        self.assertEqual(wizard.instance_id, instance)
        self.assertEqual(wizard.client_id, CLIENT_ID)
        self.assertEqual(wizard.webhook_secret, CLIENT_SECRET)
        # The fetched token is not a credential to confirm in the wizard.
        self.assertFalse(wizard.access_token)

        with (
            self._patch_token_request() as request_token,
            self._patch_shopify_client() as client_class,
        ):
            wizard.action_test_connection()

        request_token.assert_not_called()
        self.assertEqual(instance.client_id, CLIENT_ID)
        self.assertEqual(instance.access_token, "shpat-fetched")
        self.assertEqual(client_class.call_args.args[1], "shpat-fetched")
