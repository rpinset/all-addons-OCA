from unittest.mock import Mock, patch

from odoo.tests.common import TransactionCase

from ..models.instance import REQUIRED_WEBHOOK_TOPICS
from .common import assert_shopify_models_have_company_rules


class TestShopifyInstance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Test Shop",
                "shop_url": "test-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )

    def test_connection_marks_instance_connected(self):
        client = Mock()
        client.execute.return_value = {
            "shop": {
                "name": "Test Shop",
                "currencyCode": self.instance.company_id.currency_id.name,
            }
        }
        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            action = self.instance.action_test_connection()

        self.assertEqual(self.instance.state, "connected")
        self.assertEqual(action["tag"], "display_notification")
        self.assertEqual(
            self.env["shopify.log"].search_count(
                [
                    ("instance_id", "=", self.instance.id),
                    ("level", "=", "info"),
                ]
            ),
            1,
        )

    def test_repair_creates_all_missing_subscriptions(self):
        client = Mock()
        client.execute.side_effect = [
            {"webhookSubscriptions": {"nodes": []}},
            *[
                {
                    "webhookSubscriptionCreate": {
                        "webhookSubscription": {"id": str(index)}
                    }
                }
                for index, _topic in enumerate(REQUIRED_WEBHOOK_TOPICS)
            ],
        ]
        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            patch.object(
                type(self.instance),
                "_webhook_callback_url",
                return_value="https://odoo.example/shopify/webhook/1",
            ),
        ):
            self.instance.action_repair_webhook_subscriptions()

        self.assertEqual(client.execute.call_count, len(REQUIRED_WEBHOOK_TOPICS) + 1)

    def test_every_shopify_model_has_a_company_record_rule(self):
        assert_shopify_models_have_company_rules(self)

    def test_duplicate_copies_configuration_without_credentials_or_bindings(self):
        self.instance.write(
            {
                "inventory_import_enabled": True,
                "customer_export_enabled": True,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Bound Before Copy",
                "company_id": self.instance.company_id.id,
            }
        )
        self.env["shopify.product.template"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Product/880",
                "odoo_id": product.product_tmpl_id.id,
            }
        )

        action = self.instance.action_duplicate_configuration()
        duplicate = self.env["shopify.instance"].browse(action["res_id"])

        self.assertEqual(duplicate.state, "draft")
        self.assertTrue(duplicate.active)
        self.assertFalse(duplicate.access_token)
        self.assertFalse(duplicate.webhook_secret)
        self.assertNotEqual(duplicate.shop_url, self.instance.shop_url)
        self.assertNotEqual(
            duplicate.product_pricelist_id,
            self.instance.product_pricelist_id,
        )
        self.assertNotEqual(
            duplicate.guest_partner_id,
            self.instance.guest_partner_id,
        )
        self.assertTrue(duplicate.inventory_import_enabled)
        self.assertTrue(duplicate.customer_export_enabled)
        self.assertEqual(
            duplicate._product_field_owners(),
            self.instance._product_field_owners(),
        )
        self.assertFalse(
            self.env["shopify.product.template"].search(
                [("instance_id", "=", duplicate.id)]
            )
        )

    def test_archived_instance_job_returns_before_processing(self):
        self.instance.active = False

        result = self.env["shopify.order"]._job_import_order(
            self.instance.id, {"not": "an order"}
        )

        self.assertFalse(result)
