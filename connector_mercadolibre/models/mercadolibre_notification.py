# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, timezone

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

_logger = logging.getLogger(__name__)


class MercadoLibreNotification(models.Model):
    _name = "mercadolibre.notification"
    _description = "Mercado Libre Notification"
    _order = "id desc"
    _rec_name = "topic"

    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="backend_id.company_id",
        store=True,
        index=True,
    )
    topic = fields.Char(required=True, index=True)
    resource = fields.Char(required=True)
    user_id = fields.Char(string="Mercado Libre User")
    application_id = fields.Char()
    sent = fields.Datetime()
    attempts = fields.Integer()
    actions = fields.Char()
    payload = fields.Json()
    state = fields.Selection(
        selection=[
            ("received", "Received"),
            ("enqueued", "Enqueued"),
            ("done", "Done"),
            ("skipped", "Skipped"),
            ("error", "Error"),
        ],
        default="received",
        required=True,
        index=True,
    )
    error_message = fields.Text(readonly=True)

    _notification_unique = models.Constraint(
        "UNIQUE(backend_id, topic, resource, sent)",
        "This Mercado Libre notification was already received.",
    )

    @api.model
    def _parse_sent(self, value):
        if not value:
            return False
        if isinstance(value, datetime):
            parsed = value
        else:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed

    @api.model
    def receive(self, backend_id, payload):
        """Store a callback. This method does not call Mercado Libre."""
        backend = self.env["mercadolibre.backend"].browse(backend_id).exists()
        if not backend:
            _logger.info(
                "Mercado Libre notification ignored for unknown backend %s",
                backend_id,
            )
            return self.browse()
        if not isinstance(payload, dict):
            _logger.info(
                "Mercado Libre notification ignored for backend %s",
                backend_id,
            )
            return self.browse()
        return self.create_from_payload(backend, payload)

    @api.model
    def create_from_payload(self, backend, payload):
        sent = self._parse_sent(payload.get("sent"))
        topic = payload.get("topic") or ""
        resource = payload.get("resource") or ""
        user_id = payload.get("user_id")
        user_id = False if user_id in (None, False, "") else str(user_id)
        application_id = payload.get("application_id")
        application_id = (
            False if application_id in (None, False, "") else str(application_id)
        )
        existing = self.search(
            [
                ("backend_id", "=", backend.id),
                ("topic", "=", topic),
                ("resource", "=", resource),
                ("sent", "=", sent),
            ],
            limit=1,
        )
        if existing:
            return existing
        actions = payload.get("actions")
        if isinstance(actions, list):
            actions = ",".join(str(action) for action in actions)
        vals = {
            "backend_id": backend.id,
            "topic": topic,
            "resource": resource,
            "user_id": user_id,
            "application_id": application_id,
            "sent": sent,
            "attempts": payload.get("attempts") or 0,
            "actions": actions or False,
            "payload": payload,
        }
        if user_id and user_id != str(backend.seller_id or ""):
            vals["state"] = "skipped"
        notification = self.create(vals)
        if notification.state != "skipped":
            notification._enqueue_dispatch()
        return notification

    def _enqueue_dispatch(self):
        for notification in self:
            notification.write({"state": "enqueued"})
            description = notification.env._(
                "Mercado Libre notification %(topic)s %(resource)s",
                topic=notification.topic,
                resource=notification.resource,
            )
            identity_key = (
                f"notify:{notification.backend_id.id}:"
                f"{notification.topic}:{notification.resource}"
            )
            notification.with_delay(
                identity_key=identity_key,
                description=description,
            )._job_dispatch()

    def _select_handler(self, handlers):
        self.ensure_one()
        specific = [handler for handler in handlers if handler._topic == self.topic]
        if len(specific) > 1:
            names = ", ".join(handler._name for handler in specific)
            raise FailedJobError(
                self.env._(
                    "Several Mercado Libre handlers match topic %(topic)s: %(names)s",
                    topic=self.topic,
                    names=names,
                )
            )
        if specific:
            return specific[0]
        generic = [handler for handler in handlers if not handler._topic]
        if len(generic) == 1:
            return generic[0]
        return None

    def _job_dispatch(self):
        """Run the handler registered for this topic."""
        self.ensure_one()
        try:
            with self.backend_id.work_on(
                "mercadolibre.notification", notification=self
            ) as work:
                handlers = work.many_components(usage="notification.handler")
                handler = self._select_handler(handlers)
                if handler is None:
                    self.write({"state": "skipped", "error_message": False})
                    return
                handler.handle()
        except RetryableJobError:
            raise
        except Exception as error:
            message = str(error)
            self.write({"state": "error", "error_message": message})
            if isinstance(error, FailedJobError):
                raise
            raise FailedJobError(message) from error

    def button_requeue(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can requeue notifications.")
            )
        blocked = self.filtered(lambda note: note.state not in ("error", "skipped"))
        if blocked:
            raise UserError(
                self.env._("Only skipped or failed notifications can be requeued.")
            )
        self.write({"state": "received", "error_message": False})
        self._enqueue_dispatch()
