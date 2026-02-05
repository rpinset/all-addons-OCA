# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import Annotated

from odoo.api import Environment

from odoo.addons.fastapi import context, dependencies

from fastapi import Depends


def odoo_env_with_context(
    company_id: Annotated[int | None, Depends(dependencies.company_id)],
    fastapi_endpoint_id: Annotated[int, Depends(dependencies.fastapi_endpoint_id)],
) -> Environment:
    # Add a per endpoint customizable odoo environment context
    env = context.odoo_env_ctx.get()
    endpoint = env["fastapi.endpoint"].browse(fastapi_endpoint_id)
    env = env(
        context=dict(
            env.context,
            **endpoint._get_app_context(),
            **({"allow_company_ids": [company_id]} if company_id else {}),
        )
    )
    yield env
