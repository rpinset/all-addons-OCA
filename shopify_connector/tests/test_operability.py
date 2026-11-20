from unittest.mock import Mock, patch

from odoo.tests.common import TransactionCase

from odoo.addons.queue_job.job import Job

from ..lib.operability import REQUIRED_ADMIN_SCOPES
from ..models.instance import REQUIRED_WEBHOOK_TOPICS


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

    def test_dashboard_counts_the_failed_jobs_of_the_store(self):
        instance = self.instance.with_company(self.instance.company_id)
        job = Job(
            instance._job_import_locations,
            channel="root.shopify.import",
            identity_key=f"shopify.inventory.locations.{instance.id}",
        )
        job.set_failed(exc_message="Field 'isActive' doesn't exist")
        job.store()

        self.instance.invalidate_recordset(["dashboard_failed_jobs"])
        self.assertEqual(self.instance.dashboard_failed_jobs, 1)
        action = self.instance.action_open_failed_jobs()
        self.assertEqual(action["res_model"], "queue.job")
        self.assertEqual(
            self.env["queue.job"].search(action["domain"]), job.db_record()
        )

    def test_dashboard_leaves_out_the_failed_jobs_of_other_stores(self):
        other = self.env["shopify.instance"].create(
            {
                "name": "Other Operations Shop",
                "shop_url": "other-operations-shop.myshopify.com",
                "access_token": "token",
                "webhook_secret": "secret",
            }
        )
        other = other.with_company(other.company_id)
        # Keys of the other store whose later IDs equal this store's.
        for key in (
            f"shopify.customer.export.{other.id}.{self.instance.id}",
            f"shopify.inventory.delta.{other.id}.{self.instance.id}.7",
        ):
            job = Job(
                other._job_import_locations,
                channel="root.shopify.import",
                identity_key=key,
            )
            job.set_failed(exc_message="Throttled")
            job.store()

        self.instance.invalidate_recordset(["dashboard_failed_jobs"])
        self.assertEqual(self.instance.dashboard_failed_jobs, 0)
        action = self.instance.action_open_failed_jobs()
        self.assertFalse(self.env["queue.job"].search(action["domain"]))

    def test_dashboard_backlog_counts_only_the_jobs_of_the_store(self):
        other = self.env["shopify.instance"].create(
            {
                "name": "Other Backlog Shop",
                "shop_url": "other-backlog-shop.myshopify.com",
                "access_token": "token",
                "webhook_secret": "secret",
            }
        )
        instance = self.instance.with_company(self.instance.company_id)
        for store, key in (
            (instance, f"shopify.inventory.locations.{instance.id}"),
            (other, f"shopify.customer.export.{other.id}.{instance.id}"),
        ):
            Job(
                store.with_company(store.company_id)._job_import_locations,
                channel="root.shopify.import",
                identity_key=key,
            ).store()

        self.instance.invalidate_recordset(["dashboard_queue_backlog"])
        self.assertEqual(self.instance.dashboard_queue_backlog, 1)

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
                        f"shopify.retry.shopify.customer.{self.instance.id}."
                        f"{binding.id}.%",
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

    def test_dashboard_finds_webhooks_by_their_delivered_topic(self):
        self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": "dashboard-topic-1",
                "topic": "customers/create",
                "payload": {"id": 1},
            }
        )

        summary = self.instance._dashboard_webhook_summary()

        self.assertIn("customers/create: ", summary)
        self.assertNotIn("customers/create: never", summary)
        self.assertIn("orders/create: never", summary)
