from odoo import fields, models

WEBHOOK_HANDLERS = {}


class ShopifyWebhookEvent(models.Model):
    _name = "shopify.webhook.event"
    _description = "Shopify Webhook Event"
    _order = "create_date desc, id desc"

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    webhook_id = fields.Char(required=True, index=True, readonly=True)
    topic = fields.Char(required=True, index=True, readonly=True)
    payload = fields.Json(string="Raw Payload", required=True, readonly=True)
    state = fields.Selection(
        [
            ("received", "Received"),
            ("queued", "Queued"),
            ("done", "Done"),
            ("error", "Error"),
        ],
        required=True,
        default="received",
        index=True,
        readonly=True,
    )
    error_message = fields.Text(readonly=True)

    _instance_webhook_id_unique = models.Constraint(
        "UNIQUE(instance_id, webhook_id)",
        "This Shopify webhook has already been received.",
    )

    def _enqueue_dispatch(self):
        for event in self:
            if event.state != "received":
                continue
            if not event.instance_id.active:
                event.write(
                    {
                        "state": "done",
                        "error_message": (
                            "Skipped because the Shopify instance is archived."
                        ),
                    }
                )
                continue
            event.state = "queued"
            event.with_delay(
                description=self.env._("Dispatch Shopify webhook %s", event.webhook_id),
                identity_key=(
                    f"shopify.webhook.dispatch."
                    f"{event.instance_id.id}.{event.webhook_id}"
                ),
            )._dispatch()

    def _dispatch(self):
        self.ensure_one()
        if self.state == "done":
            return
        if not self.instance_id.active:
            self.write(
                {
                    "state": "done",
                    "error_message": (
                        "Skipped because the Shopify instance is archived."
                    ),
                }
            )
            return
        handler_name = WEBHOOK_HANDLERS.get(self.topic)
        try:
            if handler_name:
                getattr(self, handler_name)()
            self.state = "done"
            self.instance_id._write_log(
                entity="webhook",
                direction="import",
                level="info",
                message=self.env._("Webhook %(topic)s dispatched.", topic=self.topic),
                record=self,
            )
        except Exception as exc:
            self.write(
                {
                    "state": "error",
                    "error_message": str(exc),
                }
            )
            self.instance_id._write_log(
                entity="webhook",
                direction="import",
                level="error",
                message=self.env._(
                    "Webhook %(topic)s dispatch failed: %(error)s",
                    topic=self.topic,
                    error=exc,
                ),
                record=self,
            )
            raise

    def action_retry_dispatch(self):
        retried = 0
        for event in self:
            if event.state != "error":
                continue
            event.write(
                {
                    "state": "received",
                    "error_message": False,
                }
            )
            event._enqueue_dispatch()
            retried += 1
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Webhook retries queued"),
                "message": self.env._(
                    "%s failed webhook events were requeued.", retried
                ),
                "type": "success",
                "sticky": False,
            },
        }
