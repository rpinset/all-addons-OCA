# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from contextlib import contextmanager
from unittest.mock import patch

from odoo.addons.connector_mercadolibre.components.backend_adapter import (
    MercadoLibreAPIError,
)
from odoo.addons.queue_job.exception import RetryableJobError

from .common import FakeResponse, MercadoLibreCommon, Transport


class TestMercadoLibreAdapter(MercadoLibreCommon):
    def test_unauthorized_refreshes_once_and_retries(self):
        self.backend.write(
            {
                "access_token": "old-access",
                "refresh_token": "old-refresh",
                "state": "connected",
            }
        )
        transport = Transport(
            [
                FakeResponse(
                    401,
                    {"message": "invalid_token", "error": "unauthorized"},
                ),
                FakeResponse(
                    200,
                    {
                        "access_token": "new-access",
                        "refresh_token": "new-refresh",
                        "expires_in": 21600,
                    },
                ),
                FakeResponse(200, {"id": "MLA1"}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.backend") as work:
            payload = work.component(usage="backend.adapter").read("/items/MLA1")
        self.assertEqual(payload["id"], "MLA1")
        self.assertEqual(len(transport.calls), 3)
        self.assertEqual(
            transport.calls[0]["headers"]["Authorization"],
            "Bearer old-access",
        )
        self.assertEqual(
            transport.calls[1]["data"]["grant_type"],
            "refresh_token",
        )
        self.assertEqual(transport.calls[1]["data"]["refresh_token"], "old-refresh")
        self.assertNotIn("Authorization", transport.calls[1]["headers"])
        self.assertEqual(
            transport.calls[2]["headers"]["Authorization"],
            "Bearer new-access",
        )
        self.assertEqual(self.backend.access_token, "new-access")

    def test_too_many_requests_is_retryable(self):
        self.backend.access_token = "old-access"
        transport = Transport(
            [
                FakeResponse(
                    429,
                    {"message": "too many requests"},
                    headers={"Retry-After": "15"},
                )
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.backend") as work:
            adapter = work.component(usage="backend.adapter")
            with self.assertRaises(RetryableJobError) as caught:
                adapter.read("/items/MLA1")
        self.assertEqual(caught.exception.seconds, 15)
        self.assertNotIn("old-access", str(caught.exception))
        self.assertEqual(len(transport.calls), 1)

    def test_search_sends_scan_cursor(self):
        self.backend.access_token = "old-access"
        transport = Transport([FakeResponse(200, {"results": [], "scroll_id": "s2"})])
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.backend") as work:
            work.component(usage="backend.adapter").search(
                "/orders/search",
                params={"seller": "123"},
                search_type="scan",
                scroll_id="s1",
                limit=50,
            )
        query = transport.calls[0]["params"]
        self.assertEqual(query["seller"], "123")
        self.assertEqual(query["search_type"], "scan")
        self.assertEqual(query["scroll_id"], "s1")
        self.assertEqual(query["limit"], 50)

    @contextmanager
    def _adapter(self, responses):
        self.backend.access_token = "tok"
        transport = Transport(responses)
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.backend") as work:
            yield work.component(usage="backend.adapter"), transport

    def test_relative_path_is_prefixed_with_the_api_host(self):
        with self._adapter([FakeResponse(200, {"id": 1})]) as (adapter, transport):
            self.assertEqual(adapter.read("users/me"), {"id": 1})
        self.assertEqual(
            transport.calls[0]["url"], "https://api.mercadolibre.com/users/me"
        )

    def test_absolute_url_is_left_unchanged(self):
        response = FakeResponse(200, {"id": "MLA1"})
        self.backend.access_token = "tok"
        with patch(
            "odoo.addons.connector_mercadolibre.components.backend_adapter.requests.request",
            return_value=response,
        ) as request:
            with self.backend.work_on("mercadolibre.backend") as work:
                payload = work.component(usage="backend.adapter").read(
                    "https://api.mercadolibre.com/items/MLA1"
                )
        self.assertEqual(payload["id"], "MLA1")
        self.assertEqual(request.call_args.args[0], "GET")
        self.assertEqual(
            request.call_args.args[1], "https://api.mercadolibre.com/items/MLA1"
        )
        self.assertEqual(
            request.call_args.kwargs["headers"]["Authorization"], "Bearer tok"
        )

    def test_empty_or_invalid_body_returns_an_empty_dict(self):
        empty = FakeResponse(200)
        invalid = FakeResponse(200, {"ignored": True})
        invalid.content = b"not-json"

        def _invalid_json():
            raise ValueError("bad json")

        invalid.json = _invalid_json
        with self._adapter([empty, invalid]) as (adapter, _transport):
            self.assertEqual(adapter.read("/empty"), {})
            self.assertEqual(adapter.read("/invalid"), {})

    def test_server_error_without_retry_after_waits_one_minute(self):
        response = FakeResponse(
            503,
            {"message": "unavailable"},
            headers={"Retry-After": "soon"},
        )
        with self._adapter([response]) as (adapter, _transport):
            with self.assertRaises(RetryableJobError) as caught:
                adapter.read("/items/MLA1")
        self.assertEqual(caught.exception.seconds, 60)

    def test_client_error_hides_token_and_keeps_the_error_code(self):
        responses = [
            FakeResponse(400, ["not-an-object"]),
            FakeResponse(400, {}),
            FakeResponse(400, {"error": "invalid_client"}),
            FakeResponse(
                400,
                {"error": "invalid_grant", "message": "invalid_grant already"},
            ),
        ]
        with self._adapter(responses) as (adapter, _transport):
            with self.assertRaises(MercadoLibreAPIError) as listed:
                adapter.read("/items/MLA1")
            self.assertIn("HTTP 400", str(listed.exception))
            self.assertIsNone(listed.exception.error_code)
            with self.assertRaises(MercadoLibreAPIError) as empty:
                adapter.read("/items/MLA1")
            self.assertIn(": error", str(empty.exception))
            with self.assertRaises(MercadoLibreAPIError) as coded:
                adapter.read("/items/MLA1")
            self.assertEqual(coded.exception.error_code, "invalid_client")
            self.assertIn("invalid_client", str(coded.exception))
            with self.assertRaises(MercadoLibreAPIError) as repeated:
                adapter.read("/items/MLA1")
        self.assertIn("invalid_grant already", str(repeated.exception))
        self.assertNotIn("invalid_grant: invalid_grant", str(repeated.exception))

    def test_crud_helpers_map_onto_http_methods(self):
        responses = [
            FakeResponse(200, {"results": []}),
            FakeResponse(200, {"results": [1]}),
            FakeResponse(200, {"id": "MLA9"}),
            FakeResponse(200, {"id": "MLA9"}),
            FakeResponse(200, [{"id": "MLA1"}, {"id": "MLA2"}]),
        ]
        with self._adapter(responses) as (adapter, transport):
            self.assertEqual(
                adapter.search("/orders/search", offset=0), {"results": []}
            )
            self.assertEqual(transport.calls[0]["params"], {"offset": 0})
            self.assertEqual(
                adapter.search_read("/orders/search", params={"seller": "1"}),
                {"results": [1]},
            )
            self.assertEqual(adapter.create("/items", {"title": "Hat"}), {"id": "MLA9"})
            self.assertEqual(transport.calls[2]["method"], "POST")
            self.assertEqual(transport.calls[2]["json"], {"title": "Hat"})
            self.assertEqual(
                adapter.write("/items/MLA9", {"title": "Cap"}), {"id": "MLA9"}
            )
            self.assertEqual(transport.calls[3]["method"], "PUT")
            self.assertEqual(
                adapter.read_multi(["MLA1", "MLA2"]),
                [{"id": "MLA1"}, {"id": "MLA2"}],
            )
            self.assertEqual(transport.calls[4]["params"], {"ids": "MLA1,MLA2"})
