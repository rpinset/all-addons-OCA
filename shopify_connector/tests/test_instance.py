import base64
import hashlib
import hmac
from contextlib import contextmanager
from datetime import timedelta
from unittest.mock import Mock, patch

import psycopg2
from lxml import etree

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger
from odoo.tools.safe_eval import safe_eval

from odoo.addons.queue_job.exception import RetryableJobError

from ..lib.client import ShopifyUserError
from ..lib.operability import REQUIRED_ADMIN_SCOPES
from ..lib.webhook import verify_webhook_hmac
from ..models import instance as instance_module
from ..models.field_mapping import (
    DEFAULT_CUSTOMER_FIELD_OWNERS,
    DEFAULT_PRODUCT_FIELD_OWNERS,
    PRODUCT_FIELDS,
)
from ..models.instance import REQUIRED_WEBHOOK_TOPICS
from .common import assert_shopify_models_have_company_rules

CLIENT_ID = "dev-dashboard-client-id"
CLIENT_SECRET = "dev-dashboard-client-secret"


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
                "client_id": "test-client-id",
                "access_token_expires_at": "2026-01-01 00:00:00",
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
        self.assertFalse(duplicate.client_id)
        self.assertFalse(duplicate.access_token)
        self.assertFalse(duplicate.access_token_expires_at)
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


class TestShopifyInstanceClientCredentials(TransactionCase):
    """Cover the Shopify Dev Dashboard client credentials authentication."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Dev Dashboard Shop",
                "shop_url": "dev-dashboard.myshopify.com",
                "client_id": CLIENT_ID,
                "webhook_secret": CLIENT_SECRET,
            }
        )

    def _patch_token_request(self, **kwargs):
        return patch.object(instance_module, "request_access_token", **kwargs)

    @contextmanager
    def _registry_test_mode(self):
        """Let Odoo 18 reuse this test transaction for nested cursors.

        The nested cursor therefore shares the transaction of the test, so the
        renewal lock is never actually contended here: these tests cover the
        statements and the branches around the lock, not the serialisation
        itself, which only a second database connection would exercise.
        """
        env = self.env
        env.flush_all()
        self.registry.enter_test_mode(self.cr)
        try:
            yield
        finally:
            self.registry.leave_test_mode()
            env.invalidate_all()

    def test_client_credentials_request_stores_and_uses_the_token(self):
        with self._patch_token_request(
            return_value={"access_token": "shpat-fresh", "expires_in": 3600}
        ) as request_token:
            client = self.instance._shopify_client()

        request_token.assert_called_once_with(
            "dev-dashboard.myshopify.com", CLIENT_ID, CLIENT_SECRET
        )
        self.assertEqual(self.instance.access_token, "shpat-fresh")
        self.assertGreater(
            self.instance.access_token_expires_at,
            fields.Datetime.now() + timedelta(seconds=3500),
        )
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-fresh")

    def test_connection_test_succeeds_without_a_manual_access_token(self):
        shopify_client = Mock()
        shopify_client.execute.side_effect = [
            {
                "shop": {
                    "name": "Dev Dashboard Shop",
                    "currencyCode": self.instance.company_id.currency_id.name,
                }
            },
            {
                "currentAppInstallation": {
                    "accessScopes": [
                        {"handle": scope} for scope in REQUIRED_ADMIN_SCOPES
                    ]
                }
            },
        ]
        with (
            self._patch_token_request(
                return_value={"access_token": "shpat-fresh", "expires_in": 86399}
            ) as request_token,
            patch.object(
                instance_module, "ShopifyClient", return_value=shopify_client
            ) as client_class,
        ):
            self.instance.action_test_connection()

        request_token.assert_called_once()
        self.assertEqual(client_class.call_args.args[1], "shpat-fresh")
        self.assertEqual(self.instance.state, "connected")

    def test_valid_access_token_is_reused_without_a_new_request(self):
        self.instance.write(
            {
                "access_token": "shpat-valid",
                "access_token_expires_at": fields.Datetime.now() + timedelta(hours=1),
            }
        )
        with self._patch_token_request() as request_token:
            client = self.instance._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-valid")

    def test_expired_access_token_is_replaced(self):
        self.instance.write(
            {
                "access_token": "shpat-expired",
                "access_token_expires_at": fields.Datetime.now() - timedelta(seconds=1),
            }
        )
        with self._patch_token_request(
            return_value={"access_token": "shpat-renewed", "expires_in": 86399}
        ) as request_token:
            client = self.instance._shopify_client()

        request_token.assert_called_once()
        self.assertEqual(self.instance.access_token, "shpat-renewed")
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-renewed")

    def test_token_expiring_inside_the_safety_margin_is_renewed(self):
        """Shopify must never receive a request with a token about to expire."""
        margin = instance_module.ACCESS_TOKEN_EXPIRY_MARGIN_SECONDS
        self.instance.write(
            {
                "access_token": "shpat-about-to-expire",
                "access_token_expires_at": fields.Datetime.now()
                + timedelta(seconds=margin // 2),
            }
        )
        requested_at = fields.Datetime.now()

        with self._patch_token_request(
            return_value={"access_token": "shpat-ahead-of-time", "expires_in": 3600}
        ) as request_token:
            client = self.instance._shopify_client()

        request_token.assert_called_once()
        self.assertEqual(
            client._headers["X-Shopify-Access-Token"], "shpat-ahead-of-time"
        )
        # The margin only shortens reuse: the stored expiry is Shopify's own.
        self.assertGreaterEqual(
            self.instance.access_token_expires_at,
            requested_at + timedelta(seconds=3600),
        )
        self.assertLessEqual(
            self.instance.access_token_expires_at,
            fields.Datetime.now() + timedelta(seconds=3600),
        )

    def test_token_outliving_the_safety_margin_is_reused(self):
        margin = instance_module.ACCESS_TOKEN_EXPIRY_MARGIN_SECONDS
        expires_at = fields.Datetime.now() + timedelta(seconds=2 * margin)
        self.instance.write(
            {
                "access_token": "shpat-still-good",
                "access_token_expires_at": expires_at,
            }
        )

        with self._patch_token_request() as request_token:
            client = self.instance._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-still-good")
        self.assertEqual(self.instance.access_token_expires_at, expires_at)

    def _store_a_valid_managed_token(self):
        self.instance.write(
            {
                "access_token": "shpat-managed",
                "access_token_expires_at": fields.Datetime.now() + timedelta(hours=1),
            }
        )

    def _create_legacy_instance(self):
        return self.env["shopify.instance"].create(
            {
                "name": "Legacy Shop",
                "shop_url": "legacy.myshopify.com",
                "access_token": "shpat-static",
                "webhook_secret": "legacy-webhook-secret",
            }
        )

    def _assert_the_stored_token_was_invalidated(self, instance):
        self.assertFalse(instance.access_token)
        self.assertFalse(instance.access_token_expires_at)

    def test_changing_the_client_id_invalidates_the_stored_token(self):
        self._store_a_valid_managed_token()

        self.instance.client_id = "rotated-client-id"

        self._assert_the_stored_token_was_invalidated(self.instance)

    def test_changing_the_client_secret_invalidates_the_stored_token(self):
        self._store_a_valid_managed_token()

        self.instance.webhook_secret = "rotated-client-secret"

        self._assert_the_stored_token_was_invalidated(self.instance)

    def test_changing_the_shop_domain_invalidates_the_stored_token(self):
        self._store_a_valid_managed_token()

        self.instance.shop_url = "moved-dashboard.myshopify.com"

        self._assert_the_stored_token_was_invalidated(self.instance)

    def test_changing_an_unrelated_field_keeps_the_stored_token(self):
        self._store_a_valid_managed_token()
        expires_at = self.instance.access_token_expires_at

        self.instance.write({"name": "Renamed Shop", "accept_webhooks": False})

        self.assertEqual(self.instance.access_token, "shpat-managed")
        self.assertEqual(self.instance.access_token_expires_at, expires_at)
        with self._patch_token_request() as request_token:
            self.instance._shopify_client()

        request_token.assert_not_called()

    def test_rewriting_the_same_credentials_keeps_the_stored_token(self):
        self._store_a_valid_managed_token()
        expires_at = self.instance.access_token_expires_at

        self.instance.write(
            {
                "shop_url": "HTTPS://Dev-Dashboard.myshopify.com/",
                "client_id": CLIENT_ID,
                "webhook_secret": CLIENT_SECRET,
            }
        )

        self.assertEqual(self.instance.access_token, "shpat-managed")
        self.assertEqual(self.instance.access_token_expires_at, expires_at)

    def test_invalidated_token_is_replaced_with_the_new_credentials(self):
        self._store_a_valid_managed_token()
        self.instance.client_id = "rotated-client-id"

        with self._patch_token_request(
            return_value={"access_token": "shpat-rotated", "expires_in": 86399}
        ) as request_token:
            client = self.instance._shopify_client()

        request_token.assert_called_once_with(
            "dev-dashboard.myshopify.com", "rotated-client-id", CLIENT_SECRET
        )
        self.assertEqual(self.instance.access_token, "shpat-rotated")
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-rotated")

    def test_legacy_static_token_survives_a_credentials_change(self):
        legacy = self._create_legacy_instance()

        legacy.write(
            {
                "shop_url": "legacy-renamed.myshopify.com",
                "webhook_secret": "rotated-webhook-secret",
            }
        )

        with self._patch_token_request() as request_token:
            client = legacy._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(legacy.access_token, "shpat-static")
        self.assertFalse(legacy.access_token_expires_at)
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-static")

    def test_switching_to_managed_credentials_never_reuses_the_static_token(self):
        legacy = self._create_legacy_instance()

        legacy.client_id = CLIENT_ID

        self._assert_the_stored_token_was_invalidated(legacy)
        with self._patch_token_request(
            return_value={"access_token": "shpat-issued", "expires_in": 86399}
        ) as request_token:
            client = legacy._shopify_client()

        request_token.assert_called_once_with(
            "legacy.myshopify.com", CLIENT_ID, "legacy-webhook-secret"
        )
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-issued")

    def test_managed_credentials_change_invalidates_a_token_written_with_them(self):
        """A token supplied with new credentials is no safer than the old one."""
        self._store_a_valid_managed_token()

        self.instance.write(
            {
                "client_id": "rotated-client-id",
                "access_token": "shpat-supplied",
                "access_token_expires_at": fields.Datetime.now() + timedelta(hours=1),
            }
        )

        self._assert_the_stored_token_was_invalidated(self.instance)

    def test_switching_to_a_supplied_static_token_keeps_it_without_an_expiry(self):
        self._store_a_valid_managed_token()

        self.instance.write(
            {
                "client_id": False,
                "access_token": "shpat-new-static",
            }
        )

        self.assertEqual(self.instance.access_token, "shpat-new-static")
        self.assertFalse(self.instance.access_token_expires_at)
        with self._patch_token_request() as request_token:
            client = self.instance._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-new-static")

    def test_switching_back_to_a_legacy_configuration_drops_the_managed_token(self):
        self._store_a_valid_managed_token()

        self.instance.client_id = False

        # A fetched token must never pass for a manually configured one.
        self._assert_the_stored_token_was_invalidated(self.instance)

    def _expire_the_stored_token(self):
        self.instance.write(
            {
                "access_token": "shpat-expired",
                "access_token_expires_at": fields.Datetime.now() - timedelta(seconds=1),
            }
        )

    def test_expired_token_is_renewed_in_its_own_locked_transaction(self):
        """The renewal commits on its own, so waiting workers can see it."""
        self._expire_the_stored_token()

        with (
            self._registry_test_mode(),
            self._patch_token_request(
                return_value={"access_token": "shpat-locked", "expires_in": 86399}
            ) as request_token,
        ):
            token = self.instance._shopify_access_token()
            # The renewing transaction stored the token before returning it.
            self.assertEqual(self.instance.access_token, "shpat-locked")

        request_token.assert_called_once()
        self.assertEqual(token, "shpat-locked")

    def test_token_stored_while_waiting_for_the_lock_is_reused(self):
        """A worker that waited for the lock checks the token again first."""
        self._expire_the_stored_token()
        take_the_lock = type(self.instance)._lock_for_access_token_renewal

        def renew_in_another_worker(instance, cr):
            self.instance.write(
                {
                    "access_token": "shpat-other-worker",
                    "access_token_expires_at": fields.Datetime.now()
                    + timedelta(hours=1),
                }
            )
            self.env.flush_all()
            return take_the_lock(instance, cr)

        with (
            self._registry_test_mode(),
            patch.object(
                type(self.instance),
                "_lock_for_access_token_renewal",
                renew_in_another_worker,
            ),
            self._patch_token_request() as request_token,
        ):
            token = self.instance._shopify_access_token()

        request_token.assert_not_called()
        self.assertEqual(token, "shpat-other-worker")

    def test_renewal_lock_statements_target_the_instance_row(self):
        cr = Mock()
        cr.rowcount = 1

        self.assertTrue(self.instance._lock_for_access_token_renewal(cr))

        timeout, visibility, lock = cr.execute.call_args_list
        self.assertEqual(
            timeout.args,
            (
                "SELECT set_config(%s, %s, true)",
                [
                    "lock_timeout",
                    f"{instance_module.ACCESS_TOKEN_LOCK_TIMEOUT_SECONDS}s",
                ],
            ),
        )
        self.assertEqual(visibility.args[1], [self.instance.id])
        self.assertIn("FROM shopify_instance", visibility.args[0])
        self.assertEqual(lock.args[1], [self.instance.id])
        self.assertIn("pg_advisory_xact_lock", lock.args[0])
        # A row lock would queue behind the pending write of the caller.
        for statement in (visibility, lock):
            self.assertNotIn("FOR UPDATE", statement.args[0])

    def test_instance_of_an_uncommitted_transaction_is_renewed_without_the_lock(self):
        """Nothing else can renew a row no other transaction can see yet."""
        cr = Mock()
        cr.rowcount = 0

        self.assertFalse(self.instance._lock_for_access_token_renewal(cr))

        for statement in cr.execute.call_args_list:
            self.assertNotIn("pg_advisory_xact_lock", statement.args[0])

    def _patch_the_lock_timing_out(self):
        return patch.object(
            type(self.instance),
            "_lock_for_access_token_renewal",
            side_effect=psycopg2.errors.LockNotAvailable("lock timeout"),
        )

    @mute_logger("odoo.addons.shopify_connector.models.instance")
    def test_lock_timeout_never_requests_a_second_token(self):
        """Waiting for another worker must not end in a renewal of our own."""
        self._expire_the_stored_token()

        with (
            self._registry_test_mode(),
            self._patch_the_lock_timing_out(),
            self._patch_token_request() as request_token,
        ):
            with self.assertRaises(UserError):
                self.instance._shopify_access_token()

        request_token.assert_not_called()
        self.assertEqual(self.instance.access_token, "shpat-expired")

    @mute_logger("odoo.addons.shopify_connector.models.instance")
    def test_lock_timeout_inside_a_job_is_retryable(self):
        self._expire_the_stored_token()

        with (
            self._registry_test_mode(),
            self._patch_the_lock_timing_out(),
            self._patch_token_request() as request_token,
        ):
            with self.assertRaises(RetryableJobError):
                self.instance.with_context(
                    job_uuid="fbf1a5b0-shopify-token"
                )._shopify_access_token()

        request_token.assert_not_called()
        self.assertEqual(self.instance.access_token, "shpat-expired")

    def test_uncommitted_credentials_are_renewed_by_the_current_transaction(self):
        """The onboarding wizard authenticates with what it is about to store."""
        self._expire_the_stored_token()

        with (
            self._registry_test_mode(),
            self._patch_token_request(
                return_value={"access_token": "shpat-rotated", "expires_in": 86399}
            ) as request_token,
        ):
            self.instance.webhook_secret = "rotated-client-secret"
            token = self.instance._shopify_access_token()

        request_token.assert_called_once_with(
            "dev-dashboard.myshopify.com", CLIENT_ID, "rotated-client-secret"
        )
        self.assertEqual(token, "shpat-rotated")

    def test_token_without_a_recorded_expiry_is_never_reused(self):
        self.instance.access_token = "shpat-unmanaged"

        self.assertFalse(self.instance.access_token_expires_at)
        with self._patch_token_request(
            return_value={"access_token": "shpat-managed", "expires_in": 86399}
        ) as request_token:
            client = self.instance._shopify_client()

        request_token.assert_called_once()
        self.assertEqual(self.instance.access_token, "shpat-managed")
        self.assertTrue(self.instance.access_token_expires_at)
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-managed")

    def test_static_access_token_instance_keeps_working_untouched(self):
        legacy = self.env["shopify.instance"].create(
            {
                "name": "Legacy Shop",
                "shop_url": "legacy.myshopify.com",
                "access_token": "shpat-static",
                "webhook_secret": "legacy-webhook-secret",
            }
        )
        with self._patch_token_request() as request_token:
            client = legacy._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-static")
        self.assertFalse(legacy.access_token_expires_at)
        payload = b'{"id": 1}'
        digest = base64.b64encode(
            hmac.new(b"legacy-webhook-secret", payload, hashlib.sha256).digest()
        ).decode("ascii")
        self.assertTrue(verify_webhook_hmac(payload, legacy.webhook_secret, digest))

    def test_client_id_without_client_secret_is_a_functional_error(self):
        self.instance.webhook_secret = False
        with self._patch_token_request() as request_token:
            with self.assertRaisesRegex(UserError, "Client Secret"):
                self.instance._shopify_client()

        request_token.assert_not_called()

    def test_client_secret_without_client_id_is_not_a_credentials_flow(self):
        self.instance.write({"client_id": False, "access_token": "shpat-static"})
        with self._patch_token_request() as request_token:
            client = self.instance._shopify_client()

        request_token.assert_not_called()
        self.assertEqual(client._headers["X-Shopify-Access-Token"], "shpat-static")
        self.assertEqual(self.instance.webhook_secret, CLIENT_SECRET)

    def test_token_request_failure_never_exposes_credentials(self):
        error = ShopifyUserError(
            "Shopify rejected the access token request with HTTP 401."
        )
        with (
            self._registry_test_mode(),
            self._patch_token_request(side_effect=error),
        ):
            caught = None
            try:
                self.instance.action_test_connection()
            except UserError as exception:
                caught = exception

        self.assertIsInstance(caught, UserError)
        self.assertNotIn(CLIENT_SECRET, str(caught))
        self.assertEqual(self.instance.state, "error")
        self.assertFalse(self.instance.access_token)
        logs = self.env["shopify.log"].search([("instance_id", "=", self.instance.id)])
        self.assertTrue(logs)
        for log in logs:
            self.assertNotIn(CLIENT_SECRET, log.message)
            self.assertNotIn(CLIENT_ID, log.message)


class TestShopifyInstanceCredentialsForm(TransactionCase):
    """The form only offers the credentials of the authentication in use."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        arch = cls.env["shopify.instance"].get_view(
            cls.env.ref("shopify_connector.shopify_instance_view_form").id, "form"
        )["arch"]
        cls.form = etree.fromstring(arch)

    def _field(self, name):
        nodes = self.form.xpath(f"//field[@name='{name}']")
        self.assertEqual(len(nodes), 1, f"{name} is not in the form exactly once")
        return nodes[0]

    def _modifier(self, name, modifier, client_id):
        expression = self._field(name).get(modifier)
        if not expression:
            return False
        return bool(safe_eval(expression, {"client_id": client_id}))

    def test_managed_instances_expose_no_editable_access_token(self):
        # The managed token is worth reading, never editing.
        self.assertFalse(self._modifier("access_token", "invisible", CLIENT_ID))
        self.assertTrue(self._modifier("access_token", "readonly", CLIENT_ID))
        # The password widget keeps masking the token once readonly.
        self.assertEqual(self._field("access_token").get("widget"), "password")
        self.assertFalse(
            self._modifier("access_token_expires_at", "invisible", CLIENT_ID)
        )
        self.assertEqual(self._field("access_token_expires_at").get("readonly"), "1")
        # The Dev Dashboard credentials themselves stay editable.
        self.assertFalse(self._modifier("client_id", "readonly", CLIENT_ID))
        self.assertFalse(self._modifier("webhook_secret", "readonly", CLIENT_ID))

    def test_legacy_instances_still_expose_the_static_access_token(self):
        self.assertFalse(self._modifier("access_token", "invisible", False))
        self.assertFalse(self._modifier("access_token", "readonly", False))
        self.assertEqual(self._field("access_token").get("widget"), "password")
        # A static token has no managed expiry to show.
        self.assertTrue(self._modifier("access_token_expires_at", "invisible", False))
