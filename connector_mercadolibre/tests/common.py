# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from pathlib import Path

from odoo.tests import tagged
from odoo.tests.common import TransactionCase, new_test_user


class FakeResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.reason = "error"
        if payload is None:
            self.content = b""
            self._payload = None
        else:
            self._payload = payload
            self.content = b"{}"

    def json(self):
        if self._payload is None:
            raise ValueError("response has no JSON body")
        return self._payload


@tagged("post_install", "-at_install")
class MercadoLibreCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env["mercadolibre.backend"].create(
            {
                "name": "MLA Seller",
                "site_id": "MLA",
                "client_id": "app-client",
                "client_secret": "app-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
            }
        )
        cls.token_payload = cls._load("oauth_token.json")
        cls.user_payload = cls._load("users_me.json")
        cls.notification_payload = cls._load("notification_orders_v2.json")

    @classmethod
    def _load(cls, name):
        path = Path(__file__).parent / "fixtures" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def manager_user(self):
        return new_test_user(
            self.env,
            login="ml_manager",
            groups=(
                "base.group_user,connector_mercadolibre.group_mercadolibre_manager"
            ),
        )


class Transport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        if not self.responses:
            raise AssertionError(f"unexpected call {method} {url}")
        return self.responses.pop(0)
