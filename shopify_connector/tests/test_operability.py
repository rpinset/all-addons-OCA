from unittest.mock import Mock, patch

from odoo.tests.common import TransactionCase

from ..models.instance import REQUIRED_WEBHOOK_TOPICS
from ..wizards.onboarding import REQUIRED_ADMIN_SCOPES


class TestShopifyOnboarding(TransactionCase):
    def test_scope_failure_lists_missing_and_stays_on_scope_step(self):
        client = Mock()
        client.execute.side_effect = [
            {
                "shop": {
                    "name": "Wizard Shop",
                    "currencyCode": self.env.company.currency_id.name,
                }
            },
            {"currentAppInstallation": {"accessScopes": [{"handle": "read_orders"}]}},
        ]
        wizard = self.env["shopify.instance.wizard"].create(
            {
                "name": "Wizard Shop",
                "shop_url": "wizard-shop.myshopify.com",
                "access_token": "token",
                "webhook_secret": "secret",
                "company_id": self.env.company.id,
            }
        )

        with patch.object(
            type(self.env["shopify.instance"]),
            "_shopify_client",
            return_value=client,
        ):
            wizard.action_test_connection()
            wizard.action_check_scopes()

        self.assertEqual(wizard.step, "scopes")
        self.assertFalse(wizard.scope_check_ok)
        self.assertIn("write_products", wizard.missing_scopes)
        self.assertEqual(
            set(wizard.missing_scopes.splitlines()),
            set(REQUIRED_ADMIN_SCOPES) - {"read_orders"},
        )

    def test_complete_wizard_queues_chained_initial_imports(self):
        callback_url = "https://odoo.example/shopify/webhook/wizard"
        client = Mock()
        client.execute.side_effect = [
            {
                "shop": {
                    "name": "Import Graph Shop",
                    "currencyCode": self.env.company.currency_id.name,
                }
            },
            {
                "currentAppInstallation": {
                    "accessScopes": [
                        {"handle": handle} for handle in REQUIRED_ADMIN_SCOPES
                    ]
                }
            },
            {
                "locations": {
                    "nodes": [],
                    "pageInfo": {
                        "hasNextPage": False,
                        "endCursor": None,
                    },
                }
            },
            {
                "shop": {
                    "taxesIncluded": False,
                    "taxShipping": False,
                    "shopAddress": {
                        "countryCodeV2": (self.env.company.country_id.code or "US")
                    },
                }
            },
            {
                "webhookSubscriptions": {
                    "nodes": [
                        {
                            "id": f"gid://shopify/WebhookSubscription/{index}",
                            "topic": topic,
                            "endpoint": {"callbackUrl": callback_url},
                        }
                        for index, topic in enumerate(REQUIRED_WEBHOOK_TOPICS, start=1)
                    ]
                }
            },
        ]
        wizard = self.env["shopify.instance.wizard"].create(
            {
                "name": "Import Graph Shop",
                "shop_url": "import-graph.myshopify.com",
                "access_token": "token",
                "webhook_secret": "secret",
                "company_id": self.env.company.id,
                "import_products": True,
                "import_customers": True,
                "import_orders": True,
            }
        )

        with (
            patch.object(
                type(self.env["shopify.instance"]),
                "_shopify_client",
                return_value=client,
            ),
            patch.object(
                type(self.env["shopify.instance"]),
                "_webhook_callback_url",
                return_value=callback_url,
            ),
        ):
            wizard.action_test_connection()
            wizard.action_check_scopes()
            wizard.action_apply_locations()
            wizard.action_continue_to_policies()
            wizard.action_apply_policies()
            wizard.action_setup_webhooks()
            wizard.action_finish()

        instance = wizard.instance_id
        self.assertEqual(wizard.step, "imports")
        self.assertEqual(instance.state, "connected")
        self.assertTrue(wizard.scope_check_ok)
        self.assertFalse(wizard.missing_scopes)
        jobs = (
            self.env["queue.job"]
            .sudo()
            .search(
                [
                    (
                        "identity_key",
                        "=like",
                        f"shopify.onboarding.{instance.id}.{wizard.id}.%",
                    )
                ]
            )
        )
        self.assertEqual(len(jobs), 3)
        self.assertEqual(len(jobs.filtered(lambda job: job.state == "pending")), 1)
        self.assertEqual(
            len(jobs.filtered(lambda job: job.state == "wait_dependencies")),
            2,
        )


class TestShopifyErrorOperations(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Operations Shop",
                "shop_url": "operations-shop.myshopify.com",
                "access_token": "token",
                "webhook_secret": "secret",
            }
        )
        cls.instance.state = "connected"

    def test_mass_retry_resets_and_enqueues_fresh_identity(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Retry Customer",
                "company_id": self.instance.company_id.id,
            }
        )
        binding = self.env["shopify.customer"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Customer/901",
                "odoo_id": partner.id,
                "state": "error",
                "error_message": "Temporary failure",
            }
        )

        binding.action_retry_sync()

        self.assertEqual(binding.state, "pending")
        self.assertFalse(binding.error_message)
        jobs = (
            self.env["queue.job"]
            .sudo()
            .search(
                [
                    (
                        "identity_key",
                        "=like",
                        f"shopify.retry.shopify.customer.{binding.id}.%",
                    )
                ]
            )
        )
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs.channel, "root.shopify.import")

    def test_webhook_retry_is_idempotent_once_requeued(self):
        event = self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": "retry-webhook-1",
                "topic": "UNKNOWN_TEST_TOPIC",
                "payload": {"id": 1},
                "state": "error",
                "error_message": "Temporary failure",
            }
        )

        event.action_retry_dispatch()
        event.action_retry_dispatch()

        self.assertEqual(event.state, "queued")
        jobs = (
            self.env["queue.job"]
            .sudo()
            .search(
                [
                    (
                        "identity_key",
                        "=",
                        (
                            "shopify.webhook.dispatch."
                            f"{self.instance.id}.{event.webhook_id}"
                        ),
                    )
                ]
            )
        )
        self.assertEqual(len(jobs), 1)
