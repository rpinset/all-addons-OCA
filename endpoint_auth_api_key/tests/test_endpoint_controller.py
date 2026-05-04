# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
import unittest

from odoo.tests.common import HttpCase
from odoo.tools.misc import mute_logger

from .common import EndpointAuthAPIKeyTestMixin


@unittest.skipIf(os.getenv("SKIP_HTTP_CASE"), "EndpointAuthApiKeyHttpCase skipped")
class EndpointAuthApiKeyHttpCase(HttpCase, EndpointAuthAPIKeyTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()
        # force sync for test records
        cls.env["endpoint.endpoint"].search([])._handle_registry_sync()

    def tearDown(self):
        # Clear cache for method ``ir.http.routing_map()``
        self.env.registry.clear_cache("routing")
        super().tearDown()

    def _make_request(self, route, api_key=None, headers=None):
        headers = dict(headers or {})
        if api_key:
            headers["API-KEY"] = api_key.key
        return self.url_open(route, headers=headers, timeout=60)

    @mute_logger("odoo.addons.auth_api_key.models.ir_http", "odoo.http")
    def test_call_no_key(self):
        response = self._make_request("/test/api/key")
        self.assertEqual(response.status_code, 401)

    def test_call_good_key(self):
        response = self._make_request("/test/api/key", api_key=self.api_key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    @mute_logger("endpoint.endpoint")
    def test_call_bad_key(self):
        response = self._make_request("/test/api/key", api_key=self.api_key2)
        self.assertEqual(response.status_code, 403)
