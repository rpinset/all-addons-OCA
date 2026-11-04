# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timezone
from unittest.mock import patch

from odoo.exceptions import AccessError, UserError
from odoo.tests.common import new_test_user

from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

from .common import MercadoLibreCommon


class TestMercadoLibreNotification(MercadoLibreCommon):
    def test_orders_notification_is_stored_once(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        first = self.env["mercadolibre.notification"].create_from_payload(
            self.backend, self.notification_payload
        )
        second = self.env["mercadolibre.notification"].create_from_payload(
            self.backend, self.notification_payload
        )
        jobs = self.env["queue.job"].search(
            [
                ("model_name", "=", "mercadolibre.notification"),
                ("method_name", "=", "_job_dispatch"),
            ]
        )
        self.assertEqual(first, second)
        self.assertEqual(first.state, "enqueued")
        self.assertEqual(first.resource, "/orders/2195160686")
        self.assertEqual(first.actions, "order")
        self.assertEqual(
            self.env["mercadolibre.notification"].search_count([]),
            1,
        )
        self.assertEqual(len(jobs), 1)
        self.assertEqual(
            jobs.identity_key,
            f"notify:{self.backend.id}:orders_v2:/orders/2195160686",
        )

    def test_other_seller_is_stored_skipped(self):
        self.backend.seller_id = "1"
        payload = dict(self.notification_payload, user_id=2)
        notification = self.env["mercadolibre.notification"].create_from_payload(
            self.backend, payload
        )
        jobs = self.env["queue.job"].search([("method_name", "=", "_job_dispatch")])
        self.assertEqual(notification.state, "skipped")
        self.assertFalse(jobs)

    def test_unknown_topic_is_skipped(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        payload = dict(self.notification_payload, topic="questions")
        notification = (
            self.env["mercadolibre.notification"]
            .with_context(queue_job__no_delay=True)
            .create_from_payload(self.backend, payload)
        )
        self.assertEqual(notification.state, "skipped")
        self.assertFalse(notification.error_message)

    def test_receive_ignores_unknown_backend_and_invalid_payload(self):
        notifications = self.env["mercadolibre.notification"]
        self.assertFalse(notifications.receive(999999, self.notification_payload))
        self.assertFalse(notifications.receive(self.backend.id, None))
        self.assertFalse(
            notifications.receive(self.backend.id, ["not", "an", "object"])
        )
        self.assertFalse(notifications.search([]))

    def test_requeue_enqueues_again(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        payload = dict(self.notification_payload, topic="questions")
        notification = (
            self.env["mercadolibre.notification"]
            .with_context(queue_job__no_delay=True)
            .create_from_payload(self.backend, payload)
        )
        self.assertEqual(notification.state, "skipped")
        notification = self.env["mercadolibre.notification"].browse(notification.id)
        notification.with_user(self.manager_user()).button_requeue()
        self.assertEqual(notification.state, "enqueued")
        jobs = self.env["queue.job"].search([("method_name", "=", "_job_dispatch")])
        self.assertEqual(len(jobs), 1)

    def test_receive_stores_a_valid_payload(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        self.assertEqual(self.backend.notification_count, 0)
        payload = dict(self.notification_payload)
        payload.pop("actions")
        notification = self.env["mercadolibre.notification"].receive(
            self.backend.id, payload
        )
        self.assertEqual(notification.resource, "/orders/2195160686")
        self.assertFalse(notification.actions)
        self.assertEqual(self.backend.notification_count, 1)

    def test_parse_sent_accepts_blank_and_datetime_values(self):
        notifications = self.env["mercadolibre.notification"]
        self.assertFalse(notifications._parse_sent(False))
        self.assertFalse(notifications._parse_sent(""))
        naive = datetime(2020, 1, 2, 3, 4, 5)
        self.assertEqual(notifications._parse_sent(naive), naive)
        aware = datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        parsed = notifications._parse_sent(aware)
        self.assertEqual(parsed, naive)
        self.assertIsNone(parsed.tzinfo)

    def _notification(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        return self.env["mercadolibre.notification"].create_from_payload(
            self.backend, self.notification_payload
        )

    def test_select_handler_prefers_one_topic_handler(self):
        notification = self._notification()

        class Handler:
            def __init__(self, name, topic):
                self._name = name
                self._topic = topic

        topic = notification.topic
        with self.assertRaises(FailedJobError) as caught:
            notification._select_handler(
                [Handler("orders.a", topic), Handler("orders.b", topic)]
            )
        self.assertIn("orders.a", str(caught.exception))
        self.assertIn("orders.b", str(caught.exception))
        chosen = notification._select_handler(
            [Handler("orders.a", topic), Handler("generic", None)]
        )
        self.assertEqual(chosen._name, "orders.a")
        self.assertIsNone(
            notification._select_handler(
                [Handler("generic.a", None), Handler("generic.b", None)]
            )
        )

    def test_dispatch_without_a_handler_is_skipped(self):
        notification = self._notification()
        with patch.object(type(notification), "_select_handler", return_value=None):
            notification._job_dispatch()
        self.assertEqual(notification.state, "skipped")
        self.assertFalse(notification.error_message)

    def test_dispatch_retries_and_records_handler_failures(self):
        notification = self._notification()

        class RetryHandler:
            def handle(self):
                raise RetryableJobError("later", seconds=3)

        class FailedHandler:
            def handle(self):
                raise FailedJobError("nope")

        class BoomHandler:
            def handle(self):
                raise RuntimeError("boom")

        model = type(notification)
        with patch.object(model, "_select_handler", return_value=RetryHandler()):
            with self.assertRaises(RetryableJobError):
                notification._job_dispatch()
        self.assertEqual(notification.state, "enqueued")
        # Catch the error directly. assertRaises rolls back its savepoint and
        # would undo the state written just before the error is re-raised.
        try:
            with patch.object(model, "_select_handler", return_value=FailedHandler()):
                notification._job_dispatch()
        except FailedJobError as error:
            self.assertIn("nope", str(error))
        else:
            self.fail("handler failure must raise FailedJobError")
        self.assertEqual(notification.state, "error")
        try:
            with patch.object(model, "_select_handler", return_value=BoomHandler()):
                notification._job_dispatch()
        except FailedJobError as error:
            self.assertIn("boom", str(error))
        else:
            self.fail("unexpected handler errors must raise FailedJobError")
        self.assertIn("boom", notification.error_message)

    def test_user_cannot_requeue(self):
        notification = self._notification()
        notification.write({"state": "error"})
        user = new_test_user(
            self.env,
            login="ml_user_requeue",
            groups="base.group_user,connector_mercadolibre.group_mercadolibre_user",
        )
        with self.assertRaises(AccessError):
            notification.with_user(user).button_requeue()

    def test_only_skipped_or_failed_notifications_can_be_requeued(self):
        notification = self._notification()
        self.assertEqual(notification.state, "enqueued")
        with self.assertRaises(UserError):
            notification.with_user(self.manager_user()).button_requeue()
