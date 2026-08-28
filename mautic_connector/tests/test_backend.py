# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import UserError

from .common import MauticTestCase


class TestMauticBackend(MauticTestCase):
    def test_state_not_connected(self):
        backend = self.env["mautic.backend"].create(
            {
                "name": "Fresh Backend",
                "api_url": "https://mautic.test",
                "client_id": "id",
                "client_secret": "secret",
            }
        )
        self.assertEqual(backend.state, "not_connected")

    def test_state_connected(self):
        self.assertEqual(self.backend.state, "connected")

    def test_get_access_token_without_refresh_token_raises(self):
        backend = self.env["mautic.backend"].create(
            {
                "name": "Fresh Backend",
                "api_url": "https://mautic.test",
                "client_id": "id",
                "client_secret": "secret",
            }
        )
        with self.assertRaises(UserError):
            backend._get_access_token()

    def test_refresh_token_updates_backend(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.ok = True
            mock_post.return_value.json.return_value = {
                "access_token": "new-token",
                "refresh_token": "new-refresh-token",
                "expires_in": 3600,
            }
            self.backend.token_expires_at = False
            self.backend._get_access_token()
        self.assertEqual(self.backend.access_token, "new-token")
        self.assertEqual(self.backend.refresh_token, "new-refresh-token")

    def test_action_test_connection_success(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.ok = True
            action = self.backend.action_test_connection()
        self.assertEqual(action["params"]["type"], "success")

    def test_action_test_connection_failure(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.ok = False
            mock_get.return_value.status_code = 500
            mock_get.return_value.text = "Internal Server Error"
            with self.assertRaises(UserError):
                self.backend.action_test_connection()
