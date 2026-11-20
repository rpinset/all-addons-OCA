import base64
import hashlib
import hmac

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.webhook import (
    verify_webhook_hmac,
    webhook_topic_header,
)


def make_hmac(payload, secret):
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


class TestShopifyLibWebhook(TransactionCase):
    def test_valid_hmac_is_accepted(self):
        payload = b'{"id": 42}'
        assert verify_webhook_hmac(
            payload, "webhook-secret", make_hmac(payload, "webhook-secret")
        )

    def test_bad_hmac_is_rejected(self):
        assert not verify_webhook_hmac(
            b'{"id": 42}', "webhook-secret", "not-the-right-signature"
        )

    def test_missing_hmac_is_rejected(self):
        assert not verify_webhook_hmac(b"{}", "webhook-secret", None)
        assert not verify_webhook_hmac(b"{}", "webhook-secret", "")

    def test_topic_header_matches_the_delivered_topic(self):
        assert webhook_topic_header("CUSTOMERS_CREATE") == "customers/create"
        assert webhook_topic_header("APP_UNINSTALLED") == "app/uninstalled"
        assert webhook_topic_header("DRAFT_ORDERS_UPDATE") == "draft_orders/update"
        assert (
            webhook_topic_header("INVENTORY_LEVELS_UPDATE") == "inventory_levels/update"
        )
        assert webhook_topic_header("ORDERS_UPDATED") == "orders/updated"
