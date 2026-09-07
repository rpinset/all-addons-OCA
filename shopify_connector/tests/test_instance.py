from unittest.mock import Mock, patch

from odoo.tests.common import TransactionCase

from ..lib.operability import REQUIRED_ADMIN_SCOPES
from ..models.field_mapping import (
    DEFAULT_CUSTOMER_FIELD_OWNERS,
    DEFAULT_PRODUCT_FIELD_OWNERS,
    PRODUCT_FIELDS,
)
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

    def _shop_payload(self):
        return {
            "shop": {
                "name": "Test Shop",
                "currencyCode": self.instance.company_id.currency_id.name,
            }
        }

    @staticmethod
    def _scopes_payload(handles):
        return {
            "currentAppInstallation": {
                "accessScopes": [{"handle": handle} for handle in handles]
            }
        }

    def test_connection_marks_instance_connected(self):
        client = Mock()
        client.execute.side_effect = [
            self._shop_payload(),
            self._scopes_payload(REQUIRED_ADMIN_SCOPES),
        ]
        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            action = self.instance.action_test_connection()

        self.assertEqual(self.instance.state, "connected")
        self.assertEqual(action["tag"], "display_notification")
        self.assertEqual(action["params"]["type"], "success")
        self.assertEqual(
            self.env["shopify.log"].search_count(
                [
                    ("instance_id", "=", self.instance.id),
                    ("level", "=", "info"),
                ]
            ),
            1,
        )

    def test_connection_warns_about_missing_access_scopes(self):
        client = Mock()
        granted = set(REQUIRED_ADMIN_SCOPES) - {"read_draft_orders"}
        client.execute.side_effect = [
            self._shop_payload(),
            self._scopes_payload(sorted(granted)),
        ]
        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            action = self.instance.action_test_connection()

        self.assertEqual(self.instance.state, "connected")
        self.assertEqual(action["params"]["type"], "warning")
        self.assertIn("read_draft_orders", action["params"]["message"])
        warning = self.env["shopify.log"].search(
            [
                ("instance_id", "=", self.instance.id),
                ("level", "=", "warning"),
            ]
        )
        self.assertEqual(len(warning), 1)
        self.assertIn("read_draft_orders", warning.message)

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

    def test_field_ownership_selection_is_translated_for_the_client(self):
        mapping = self.env["shopify.field.mapping"].with_context(lang="en_US")

        selection = mapping.fields_get(["field"])["field"]["selection"]

        self.assertEqual(
            [value for value, __ in selection],
            [value for value, __ in PRODUCT_FIELDS],
        )
        self.assertTrue(all(label for __, label in selection))

    def test_field_ownership_lists_are_split_per_page(self):
        self.assertEqual(
            set(self.instance.product_field_mapping_ids.mapped("field")),
            set(DEFAULT_PRODUCT_FIELD_OWNERS),
        )
        self.assertEqual(
            set(self.instance.customer_field_mapping_ids.mapped("field")),
            set(DEFAULT_CUSTOMER_FIELD_OWNERS),
        )

    def test_archived_instance_job_returns_before_processing(self):
        self.instance.active = False

        result = self.env["shopify.order"]._job_import_order(
            self.instance.id, {"not": "an order"}
        )

        self.assertFalse(result)
