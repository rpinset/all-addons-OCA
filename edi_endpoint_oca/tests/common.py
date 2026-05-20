# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class EDIEndpointTestMixin:
    @classmethod
    def _setup_context(cls, **kw):
        return dict(cls.env.context, tracking_disable=True, **kw)

    @classmethod
    def _setup_env(cls, ctx=None):
        ctx = ctx or {}
        cls.env = cls.env(context=cls._setup_context(**ctx))

    @classmethod
    def _setup_records(cls):
        cls.BackendType = cls.env["edi.backend.type"]
        cls.Backend = cls.env["edi.backend"]
        cls.ExchangeType = cls.env["edi.exchange.type"]
        cls.Endpoint = cls.env["edi.endpoint"]
        cls.backend_type = (
            cls.BackendType.search([("code", "=", "demo_backend")], limit=1)
            or cls._get_backend_type()
        )
        cls.backend = (
            cls.Backend.search(
                [
                    ("backend_type_id", "=", cls.backend_type.id),
                ],
                limit=1,
            )
            or cls._get_backend()
        )
        cls.exchange_type = (
            cls.ExchangeType.search(
                [
                    ("code", "=", "demo_endpoint"),
                    ("backend_type_id", "=", cls.backend_type.id),
                ],
                limit=1,
            )
            or cls._get_exchange_type()
        )
        cls.endpoint = (
            cls.Endpoint.search(
                [
                    ("route", "=", "/edi/demo/try"),
                    ("backend_type_id", "=", cls.backend_type.id),
                    ("exchange_type_id", "=", cls.exchange_type.id),
                ],
                limit=1,
            )
            or cls._get_endpoint()
        )
        cls.endpoint_create_record = (
            cls.Endpoint.search(
                [
                    ("route", "=", "/edi/demo/create"),
                    ("backend_type_id", "=", cls.backend_type.id),
                    ("exchange_type_id", "=", cls.exchange_type.id),
                ],
                limit=1,
            )
            or cls._get_endpoint_create_record()
        )

    @classmethod
    def _get_backend_type(cls):
        return cls.env["edi.backend.type"].create(
            {
                "name": "Demo EDI backend type",
                "code": "demo_backend",
            }
        )

    @classmethod
    def _get_backend(cls):
        return cls.env["edi.backend"].create(
            {
                "name": "EDI backend with endpoints DEMO",
                "backend_type_id": cls.backend_type.id,
            }
        )

    @classmethod
    def _get_exchange_type(cls):
        return cls.env["edi.exchange.type"].create(
            {
                "name": "EDI exchange demo",
                "code": "demo_endpoint",
                "backend_type_id": cls.backend_type.id,
                "direction": "input",
            }
        )

    @classmethod
    def _get_endpoint(cls):
        return cls.env["edi.endpoint"].create(
            {
                "name": "EDI Demo Endpoint 1",
                "backend_id": cls.backend.id,
                "backend_type_id": cls.backend_type.id,
                "exchange_type_id": cls.exchange_type.id,
                "route": "/demo/try",
                "request_method": "GET",
                "exec_mode": "code",
                "code_snippet": (
                    "record = endpoint.create_exchange_record()\n"
                    'result = {"response": Response("'
                    'Created record: %s" % record.identifier)}'
                ),
            }
        )

    @classmethod
    def _get_endpoint_create_record(cls):
        return cls.env["edi.endpoint"].create(
            {
                "name": "EDI Demo Endpoint 2",
                "backend_id": cls.backend.id,
                "backend_type_id": cls.backend_type.id,
                "exchange_type_id": cls.exchange_type.id,
                "route": "/demo/create",
                "request_method": "POST",
                "request_content_type": "application/json",
                "exec_mode": "create_exchange_record",
            }
        )


class EDIEndpointCommonTestCase(TransactionCase, EDIEndpointTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()
