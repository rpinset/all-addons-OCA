# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import contextlib

from odoo import Command
from odoo.tools import DotDict

from odoo.addons.http_routing.tests.common import MockRequest


def _setup_test_api_keys(env, user):
    """Create API keys for tests."""
    api_key_model = env["auth.api.key"]

    api_key_1 = api_key_model.create(
        {
            "name": "Endpoint API key test",
            "key": "tcZ6dF2UQwNcm",
            "user_id": user.id,
        }
    )
    api_key_2 = api_key_model.create(
        {
            "name": "Endpoint API key test 2",
            "key": "tV47QyOTC5mS",
            "user_id": user.id,
        }
    )
    return api_key_1, api_key_2


def _setup_test_api_key_group(env, api_key_1):
    """Create API key group for tests."""
    return env["auth.api.key.group"].create(
        {
            "name": "Test Group 1",
            "code": "test_group1",
            "auth_api_key_ids": [Command.set(api_key_1.ids)],
        }
    )


def _setup_test_endpoint(env, api_key_group):
    """Create endpoint for tests."""
    return env["endpoint.endpoint"].create(
        {
            "name": "Test Endpoint - auth api key",
            "route": "/test/api/key",
            "request_method": "GET",
            "auth_type": "api_key",
            "auth_api_key_group_ids": [Command.set(api_key_group.ids)],
            "exec_mode": "code",
            "code_snippet": 'result = {"response": Response("ok")}',
        }
    )


class EndpointAuthAPIKeyTestMixin:
    # Keep these helpers separately instead of inheriting from
    # endpoint.tests.common.CommonEndpoint. Importing that test class
    # from test_endpoint.py also pulls in the endpoint test asset bundle, which
    # makes these auth API key tests fail during asset loading.
    # WARNING odoo odoo.addons.base.models.assetsbundle:
    # Error: Undefined variable: "$black".
    @classmethod
    def _setup_env(cls):
        cls.env = cls.env(context=cls._setup_context())

    @classmethod
    def _setup_context(cls):
        return dict(
            cls.env.context,
            tracking_disable=True,
        )

    @classmethod
    def _setup_records(cls):
        cls.api_key, cls.api_key2 = _setup_test_api_keys(
            cls.env,
            cls.env.user,
        )
        cls.key_group = _setup_test_api_key_group(
            cls.env,
            cls.api_key,
        )
        cls.endpoint = _setup_test_endpoint(
            cls.env,
            cls.key_group,
        )

    @contextlib.contextmanager
    def _get_mocked_request(
        self, httprequest=None, extra_headers=None, request_attrs=None
    ):
        with MockRequest(self.env) as mocked_request:
            mocked_request.httprequest = (
                DotDict(httprequest) if httprequest else mocked_request.httprequest
            )
            headers = {}
            headers.update(extra_headers or {})
            mocked_request.httprequest.headers = headers
            request_attrs = request_attrs or {}
            for k, v in request_attrs.items():
                setattr(mocked_request, k, v)
            mocked_request.make_response = lambda data, **kw: data
            yield mocked_request
