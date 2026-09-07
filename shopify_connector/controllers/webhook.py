import json

from psycopg2 import IntegrityError
from werkzeug.wrappers import Response

from odoo import http
from odoo.http import request

from ..lib.webhook import verify_webhook_hmac


class ShopifyWebhookController(http.Controller):
    @http.route(
        "/shopify/webhook/<int:instance_id>",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        save_session=False,
    )
    def shopify_webhook(self, instance_id, **_kwargs):
        instance = request.env["shopify.instance"].sudo().browse(instance_id).exists()
        if not instance or not instance.active or not instance.accept_webhooks:
            return Response(status=404)

        payload_limit = instance.webhook_max_payload_bytes
        content_length = request.httprequest.content_length
        if content_length is not None and content_length > payload_limit:
            return Response(status=413)
        raw_payload = request.httprequest.get_data(cache=False)
        if len(raw_payload) > payload_limit:
            return Response(status=413)
        provided_hmac = request.httprequest.headers.get("X-Shopify-Hmac-Sha256")
        if not verify_webhook_hmac(raw_payload, instance.webhook_secret, provided_hmac):
            return Response(status=401)

        webhook_id = request.httprequest.headers.get("X-Shopify-Webhook-Id")
        topic = request.httprequest.headers.get("X-Shopify-Topic")
        if not webhook_id or not topic:
            return Response(status=400)
        try:
            payload = json.loads(raw_payload)
        except (TypeError, ValueError):
            return Response(status=400)

        event_model = request.env["shopify.webhook.event"].sudo()
        event = event_model.search(
            [
                ("instance_id", "=", instance.id),
                ("webhook_id", "=", webhook_id),
            ],
            limit=1,
        )
        is_new = not event
        if is_new:
            try:
                with request.env.cr.savepoint():
                    event = event_model.create(
                        {
                            "instance_id": instance.id,
                            "webhook_id": webhook_id,
                            "topic": topic,
                            "payload": payload,
                        }
                    )
            except IntegrityError:
                event = event_model.search(
                    [
                        ("instance_id", "=", instance.id),
                        ("webhook_id", "=", webhook_id),
                    ],
                    limit=1,
                )
                is_new = False
        if is_new:
            event._enqueue_dispatch()
        return Response(status=200)
