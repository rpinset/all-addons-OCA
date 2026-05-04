# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


import werkzeug

from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger

from .common import EndpointAuthAPIKeyTestMixin


class TestEndpoint(TransactionCase, EndpointAuthAPIKeyTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()

    @mute_logger("endpoint.endpoint")
    def test_endpoint_validate_request_no_key(self):
        endpoint = self.endpoint.copy(
            {
                "route": "/api-key-test",
                "request_method": "GET",
            }
        )
        with self.assertRaises(werkzeug.exceptions.Forbidden):
            with self._get_mocked_request(
                httprequest={"method": "GET"},
            ) as req:
                endpoint._validate_request(req)

    @mute_logger("endpoint.endpoint")
    def test_endpoint_validate_request_bad_key(self):
        endpoint = self.endpoint.copy(
            {
                "route": "/api-key-test",
                "request_method": "GET",
            }
        )
        with self.assertRaises(werkzeug.exceptions.Forbidden):
            with self._get_mocked_request(
                httprequest={"method": "GET"},
                request_attrs={"auth_api_key_id": self.api_key2.id},
            ) as req:
                endpoint._validate_request(req)

    def test_endpoint_validate_request_good_key(self):
        endpoint = self.endpoint.copy(
            {
                "route": "/api-key-test",
                "request_method": "GET",
            }
        )
        with self._get_mocked_request(
            httprequest={"method": "GET"},
            request_attrs={"auth_api_key_id": self.api_key.id},
        ) as req:
            endpoint._validate_request(req)
