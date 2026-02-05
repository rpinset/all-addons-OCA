# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import Annotated

from requests import Response

from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.fastapi.routers import demo_router
from odoo.addons.fastapi.tests.common import FastAPITransactionCase

from fastapi import Depends, status


# Extend the demo router to have an endpoint that returns the odoo env context
@demo_router.get("/demo/context")
async def get_context(env: Annotated[Environment, Depends(odoo_env)]) -> dict:
    """Returns the odoo env context"""
    return env.context


class FastAPIEndpointContextCase(FastAPITransactionCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.default_fastapi_router = demo_router
        cls.default_fastapi_running_user = cls.env.ref("fastapi.my_demo_app_user")
        cls.endpoint = cls.env.ref("fastapi.fastapi_endpoint_demo")
        cls.default_fastapi_app = cls.endpoint._get_app()
        cls.default_fastapi_dependency_overrides = {
            k: v
            for k, v in cls.default_fastapi_app.dependency_overrides.items()
            if k.__name__ != "authenticated_partner_impl"
        }
        cls.default_fastapi_authenticated_partner = cls.env["res.partner"].create(
            {"name": "FastAPI Demo"}
        )

    def test_context(self) -> None:
        with self._create_test_client() as test_client:
            response: Response = test_client.get("/demo/context")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ctx = response.json()
        self.assertEqual(
            ctx.get("fastapi_endpoint_id"),
            self.env.ref("fastapi.fastapi_endpoint_demo").id,
        )
        self.assertEqual(ctx.get("fastapi_app"), "demo")
