import base64
import hashlib
import hmac
from types import SimpleNamespace
from unittest.mock import patch

from odoo.tests.common import TransactionCase

from ..controllers import webhook as webhook_controller


class FakeHttpRequest:
    def __init__(self, payload, headers, content_length=None):
        self.payload = payload
        self.headers = headers
        self.content_length = len(payload) if content_length is None else content_length

    def get_data(self, cache=False):
        del cache
        return self.payload


class TestShopifyWebhookController(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Webhook Shop",
                "shop_url": "webhook-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )

    def _request(
        self,
        payload,
        signature,
        webhook_id="webhook-1",
        content_length=None,
    ):
        return SimpleNamespace(
            env=self.env,
            httprequest=FakeHttpRequest(
                payload,
                {
                    "X-Shopify-Hmac-Sha256": signature,
                    "X-Shopify-Webhook-Id": webhook_id,
                    "X-Shopify-Topic": "ORDERS_CREATE",
                },
                content_length=content_length,
            ),
        )

    @staticmethod
    def _signature(payload):
        digest = hmac.new(b"test-secret", payload, hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def test_valid_webhook_is_deduplicated_and_enqueued_once(self):
        payload = b'{"id": 123}'
        fake_request = self._request(payload, self._signature(payload))
        controller = webhook_controller.ShopifyWebhookController()
        event_model_class = type(self.env["shopify.webhook.event"])

        with (
            patch.object(webhook_controller, "request", fake_request),
            patch.object(
                event_model_class, "_enqueue_dispatch", autospec=True
            ) as enqueue,
        ):
            first = controller.shopify_webhook(self.instance.id)
            second = controller.shopify_webhook(self.instance.id)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(enqueue.call_count, 1)
        self.assertEqual(
            self.env["shopify.webhook.event"].search_count(
                [("instance_id", "=", self.instance.id)]
            ),
            1,
        )

    def test_bad_hmac_returns_unauthorized_without_persisting(self):
        payload = b'{"id": 123}'
        fake_request = self._request(payload, "invalid")
        controller = webhook_controller.ShopifyWebhookController()

        with patch.object(webhook_controller, "request", fake_request):
            response = controller.shopify_webhook(self.instance.id)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(
            self.env["shopify.webhook.event"].search(
                [("instance_id", "=", self.instance.id)]
            )
        )

    def test_kill_switch_rejects_without_reading_payload(self):
        self.instance.accept_webhooks = False
        payload = b'{"id": 123}'
        fake_request = self._request(payload, self._signature(payload))
        controller = webhook_controller.ShopifyWebhookController()

        with patch.object(webhook_controller, "request", fake_request):
            response = controller.shopify_webhook(self.instance.id)

        self.assertEqual(response.status_code, 404)

    def test_oversized_payload_is_rejected_before_hmac(self):
        self.instance.webhook_max_payload_bytes = 8
        payload = b'{"id": 123}'
        fake_request = self._request(payload, self._signature(payload))
        controller = webhook_controller.ShopifyWebhookController()

        with (
            patch.object(webhook_controller, "request", fake_request),
            patch.object(
                webhook_controller,
                "verify_webhook_hmac",
            ) as verify,
        ):
            response = controller.shopify_webhook(self.instance.id)

        self.assertEqual(response.status_code, 413)
        verify.assert_not_called()
