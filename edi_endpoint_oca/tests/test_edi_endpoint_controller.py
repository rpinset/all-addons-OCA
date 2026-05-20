# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
import os
import unittest

from odoo.tests import HttpCase, RecordCapturer

from .common import EDIEndpointTestMixin


@unittest.skipIf(os.getenv("SKIP_HTTP_CASE"), "EDIEndpointHttpCase skipped")
class EDIEndpointHttpCase(HttpCase, EDIEndpointTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()
        # Sync only the endpoints under test to avoid re-registering unrelated
        # demo routes that may already exist in the route registry.
        (cls.endpoint | cls.endpoint_create_record)._handle_registry_sync()

    def tearDown(self):
        # Clear routing cache so each test starts clean
        self.env.registry.clear_cache("routing")
        super().tearDown()

    def _make_request(self, route, headers=None, data=None):
        headers = dict(headers or {})
        return self.url_open(route, headers=headers, data=data, timeout=60)

    def test_call1(self):
        endpoint = "/edi/demo/try"
        response = self._make_request(endpoint)
        self.assertEqual(response.status_code, 401)
        # Let's login now
        self.authenticate("admin", "admin")
        response = self._make_request(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Created record:", response.content.decode())

    def test_handle_exec_create_exchange_record(self):
        self.authenticate("admin", "admin")
        body = json.dumps({"hello": "world"}).encode()
        with RecordCapturer(self.env["edi.exchange.record"], []) as capture:
            response = self._make_request(
                "/edi/demo/create",
                headers={"Content-Type": "application/json"},
                data=body,
            )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "queued")
        self.assertEqual(len(capture.records), 1)
        record = capture.records
        self.assertEqual(record.identifier, payload["id"])
        self.assertEqual(record.edi_exchange_state, "input_received")
        self.assertEqual(base64.b64decode(record.exchange_file), body)
