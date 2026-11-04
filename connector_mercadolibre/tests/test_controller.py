# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.exceptions import AccessError, UserError
from odoo.tests.common import new_test_user

from odoo.addons.connector_mercadolibre.controllers.main import MercadoLibreController

from .common import MercadoLibreCommon


class TestMercadoLibreController(MercadoLibreCommon):
    def _call(
        self, method_name, *args, env=None, http_method="GET", payload=None, **kwargs
    ):
        httprequest = MagicMock()
        httprequest.method = http_method
        httprequest.get_json.return_value = payload
        req = MagicMock()
        req.env = env or self.env
        req.httprequest = httprequest
        req.redirect.side_effect = lambda url, *_args, **_kwargs: url
        controller = MercadoLibreController()
        method = getattr(controller, method_name)
        endpoint = getattr(method, "original_endpoint", method)
        with patch(
            "odoo.addons.connector_mercadolibre.controllers.main.request",
            req,
        ):
            return endpoint(controller, *args, **kwargs)

    def test_callback_requires_a_manager(self):
        user = new_test_user(
            self.env,
            login="ml_callback_user",
            groups="base.group_user,connector_mercadolibre.group_mercadolibre_user",
        )
        with self.assertRaises(AccessError):
            self._call(
                "oauth_callback",
                code="auth-code",
                state=str(self.backend.id),
                env=self.env(user=user),
            )

    def test_callback_rejects_a_missing_backend(self):
        env = self.env(user=self.manager_user())
        with self.assertRaises(UserError):
            self._call("oauth_callback", code="auth-code", state=None, env=env)
        with self.assertRaises(UserError):
            self._call("oauth_callback", code="auth-code", state="abc", env=env)
        with self.assertRaises(UserError):
            self._call("oauth_callback", code="auth-code", state="999999", env=env)

    def test_callback_records_an_authorization_error(self):
        env = self.env(user=self.manager_user())
        self._call(
            "oauth_callback",
            state=str(self.backend.id),
            error="access_denied",
            env=env,
        )
        self.backend.invalidate_recordset()
        self.assertEqual(self.backend.state, "error")
        self.assertEqual(self.backend.auth_error, "access_denied")

    def test_callback_enqueues_the_authorization_code(self):
        env = self.env(user=self.manager_user())
        url = self._call(
            "oauth_callback",
            code="auth-code",
            state=str(self.backend.id),
            env=env,
        )
        self.assertIn(f"/odoo/mercadolibre.backend/{self.backend.id}", url)
        jobs = self.env["queue.job"].search(
            [("method_name", "=", "_job_exchange_code")]
        )
        self.assertEqual(len(jobs), 1)

    def test_callback_without_a_code_is_an_error(self):
        env = self.env(user=self.manager_user())
        self._call("oauth_callback", state=str(self.backend.id), env=env)
        self.backend.invalidate_recordset()
        self.assertEqual(self.backend.state, "error")
        self.assertIn("Missing authorization code", self.backend.auth_error)

    def test_get_notification_is_acknowledged(self):
        self.assertEqual(self._call("notification", self.backend.id), "")
        self.assertFalse(self.env["mercadolibre.notification"].search([]))

    def test_post_notification_is_stored(self):
        self.backend.seller_id = str(self.notification_payload["user_id"])
        self._call(
            "notification",
            self.backend.id,
            http_method="POST",
            payload=self.notification_payload,
        )
        notification = self.env["mercadolibre.notification"].search([])
        self.assertEqual(notification.topic, "orders_v2")

    def test_post_notification_failure_is_still_acknowledged(self):
        with patch.object(
            type(self.env["mercadolibre.notification"]),
            "receive",
            side_effect=RuntimeError("boom"),
        ):
            result = self._call(
                "notification",
                self.backend.id,
                http_method="POST",
                payload=self.notification_payload,
            )
        self.assertEqual(result, "")
