from unittest.mock import Mock

import requests

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.client import (
    ShopifyAccessDenied,
    ShopifyClient,
    ShopifyServerError,
    ShopifyThrottled,
    ShopifyUserError,
    request_access_token,
)

CLIENT_SECRET = "top-secret-client-secret"


class FakeResponse:
    def __init__(self, status_code=200, body=None):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body


def make_client(responses, sleeps, **kwargs):
    session = Mock()
    session.post.side_effect = responses
    return (
        ShopifyClient(
            "https://Example.MyShopify.com/",
            "secret-token",
            session=session,
            sleep=sleeps.append,
            clock=lambda: 123.0,
            **kwargs,
        ),
        session,
    )


class TestShopifyLibClient(TransactionCase):
    def test_cost_throttle_sleeps_until_requested_capacity_is_available(self):
        sleeps = []
        response = FakeResponse(
            body={
                "data": {"shop": {"name": "Example"}},
                "extensions": {
                    "cost": {
                        "requestedQueryCost": 15,
                        "throttleStatus": {"currentlyAvailable": 5, "restoreRate": 5},
                    }
                },
            }
        )
        client, session = make_client([response], sleeps)
        assert client.execute("query { shop { name } }")["shop"]["name"] == "Example"
        assert sleeps == [2.0]
        assert client.last_request_at == 123.0
        assert (
            session.post.call_args.kwargs["headers"]["X-Shopify-Access-Token"]
            == "secret-token"
        )
        assert client.endpoint.endswith("/admin/api/2026-01/graphql.json")

    def test_throttled_error_retries_with_exponential_backoff(self):
        sleeps = []
        throttled = FakeResponse(
            body={
                "errors": [
                    {"message": "Throttled", "extensions": {"code": "THROTTLED"}}
                ]
            }
        )
        success = FakeResponse(body={"data": {"shop": {"name": "Example"}}})
        client, session = make_client([throttled, success], sleeps, backoff_factor=0.5)
        assert client.execute("query { shop { name } }")["shop"]["name"] == "Example"
        assert sleeps == [0.5]
        assert session.post.call_count == 2

    def test_persistent_throttling_raises_typed_exception(self):
        sleeps = []
        response = FakeResponse(
            body={
                "errors": [
                    {"message": "No capacity", "extensions": {"code": "THROTTLED"}}
                ]
            }
        )
        client, _session = make_client([response, response], sleeps, max_retries=1)
        with self.assertRaises(ShopifyThrottled):
            client.execute("query { shop { name } }")
        assert sleeps == [1.0]

    def test_http_rate_limit_retries_as_throttling(self):
        sleeps = []
        client, session = make_client(
            [FakeResponse(status_code=429), FakeResponse(body={"data": {"ok": True}})],
            sleeps,
            backoff_factor=0.25,
        )
        assert client.execute("query { shop { name } }") == {"ok": True}
        assert sleeps == [0.25]
        assert session.post.call_count == 2

    def test_server_errors_retry_with_capped_exponential_backoff(self):
        sleeps = []
        client, session = make_client(
            [
                FakeResponse(status_code=500),
                FakeResponse(status_code=503),
                FakeResponse(body={"data": {"ok": True}}),
            ],
            sleeps,
            backoff_factor=2,
            max_backoff=3,
        )
        assert client.execute("query { shop { name } }") == {"ok": True}
        assert sleeps == [2, 3]
        assert session.post.call_count == 3

    def test_transport_error_is_retried_and_redacted(self):
        sleeps = []
        client, _session = make_client(
            [requests.ConnectionError("secret-token")], sleeps, max_retries=0
        )
        with self.assertRaises(ShopifyServerError) as caught:
            client.execute("query { shop { name } }")
        assert "secret-token" not in str(caught.exception)

    def test_access_denied_errors_expose_the_missing_scopes(self):
        sleeps = []
        client, _session = make_client(
            [
                FakeResponse(
                    body={
                        "errors": [
                            {
                                "message": (
                                    "Access denied for draftOrders field. "
                                    "Required access: `read_draft_orders` "
                                    "access scope."
                                ),
                                "extensions": {"code": "ACCESS_DENIED"},
                            }
                        ]
                    }
                )
            ],
            sleeps,
        )

        with self.assertRaises(ShopifyAccessDenied) as caught:
            client.execute("query { draftOrders { nodes { id } } }")

        self.assertEqual(caught.exception.scopes, ("read_draft_orders",))
        self.assertIn("Access denied for draftOrders field", str(caught.exception))

    def test_graphql_and_mutation_user_errors_are_typed(self):
        sleeps = []
        graphql_client, _session = make_client(
            [FakeResponse(body={"errors": [{"message": "Invalid query"}]})], sleeps
        )
        with self.assertRaisesRegex(ShopifyUserError, "Invalid query"):
            graphql_client.execute("invalid")
        mutation_client, _session = make_client(
            [
                FakeResponse(
                    body={
                        "data": {
                            "webhookSubscriptionCreate": {
                                "userErrors": [{"message": "Invalid callback"}]
                            }
                        }
                    }
                )
            ],
            sleeps,
        )
        with self.assertRaisesRegex(ShopifyUserError, "Invalid callback"):
            mutation_client.execute("mutation")


def request_token(response, **kwargs):
    session = Mock()
    session.post.side_effect = [response]
    return (
        request_access_token(
            "https://Example.MyShopify.com/",
            "client-id",
            CLIENT_SECRET,
            session=session,
            **kwargs,
        ),
        session,
    )


class TestShopifyLibAccessToken(TransactionCase):
    def test_client_credentials_grant_returns_the_token_and_its_lifetime(self):
        token, session = request_token(
            FakeResponse(body={"access_token": "shpat-new", "expires_in": "86399"})
        )
        assert token == {"access_token": "shpat-new", "expires_in": 86399}
        assert session.post.call_args.args == (
            "https://example.myshopify.com/admin/oauth/access_token",
        )
        assert session.post.call_args.kwargs["data"] == {
            "grant_type": "client_credentials",
            "client_id": "client-id",
            "client_secret": CLIENT_SECRET,
        }
        assert session.post.call_args.kwargs["timeout"] == 30.0

    def test_missing_shop_domain_or_credentials_is_a_user_error(self):
        session = Mock()
        with self.assertRaises(ShopifyUserError):
            request_access_token(" ", "client-id", CLIENT_SECRET, session=session)
        with self.assertRaises(ShopifyUserError):
            request_access_token("shop.myshopify.com", "", "", session=session)
        session.post.assert_not_called()

    def test_client_error_is_typed_without_leaking_credentials(self):
        with self.assertRaises(ShopifyUserError) as caught:
            request_token(FakeResponse(status_code=401, body={"error": "invalid"}))
        assert "HTTP 401" in str(caught.exception)
        assert CLIENT_SECRET not in str(caught.exception)

    def test_server_error_is_typed_without_leaking_credentials(self):
        with self.assertRaises(ShopifyServerError) as caught:
            request_token(FakeResponse(status_code=503))
        assert "HTTP 503" in str(caught.exception)
        assert CLIENT_SECRET not in str(caught.exception)

    def test_transport_error_is_typed_and_redacted(self):
        session = Mock()
        session.post.side_effect = requests.ConnectionError(CLIENT_SECRET)
        with self.assertRaises(ShopifyServerError) as caught:
            request_access_token(
                "shop.myshopify.com", "client-id", CLIENT_SECRET, session=session
            )
        assert CLIENT_SECRET not in str(caught.exception)

    def test_non_json_response_is_a_server_error(self):
        response = Mock()
        response.status_code = 200
        response.json.side_effect = ValueError("not json")
        with self.assertRaises(ShopifyServerError):
            request_token(response)

    def test_response_without_an_access_token_is_a_server_error(self):
        with self.assertRaises(ShopifyServerError):
            request_token(FakeResponse(body={"scope": "write_products"}))
        with self.assertRaises(ShopifyServerError):
            request_token(FakeResponse(body={"access_token": ""}))
        with self.assertRaises(ShopifyServerError):
            request_token(FakeResponse(body=["shpat-new"]))

    def test_invalid_token_lifetime_is_a_server_error(self):
        for lifetime in ("soon", None, 0, -1, True, {"seconds": 60}):
            with self.assertRaises(ShopifyServerError):
                request_token(
                    FakeResponse(
                        body={"access_token": "shpat-new", "expires_in": lifetime}
                    )
                )
