# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import http
from odoo.exceptions import AccessError, UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class MercadoLibreController(http.Controller):
    @http.route(
        "/mercadolibre/oauth/callback",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def oauth_callback(self, code=None, state=None, error=None, **kwargs):
        if not request.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                request.env._("Only Mercado Libre managers can connect a seller.")
            )
        try:
            backend_id = int(state)
        except (TypeError, ValueError) as exc:
            raise UserError(
                request.env._("The Mercado Libre callback is missing the backend.")
            ) from exc
        backend = request.env["mercadolibre.backend"].browse(backend_id).exists()
        if not backend:
            raise UserError(request.env._("Mercado Libre backend not found."))
        backend.check_access("write")
        if error or not code:
            backend.write(
                {
                    "state": "error",
                    "auth_error": error or request.env._("Missing authorization code."),
                }
            )
        else:
            description = request.env._(
                "Exchange Mercado Libre authorization code for %(name)s",
                name=backend.display_name,
            )
            backend.with_delay(
                identity_key=f"exchange:{backend.id}",
                description=description,
            )._job_exchange_code(code)
        return request.redirect(f"/odoo/mercadolibre.backend/{backend.id}")

    @http.route(
        "/mercadolibre/notification/<int:backend_id>",
        type="http",
        auth="public",
        methods=["GET", "POST"],
        csrf=False,
        save_session=False,
    )
    def notification(self, backend_id, **kwargs):
        """Acknowledge Mercado Libre before any call to its API."""
        if request.httprequest.method == "POST":
            payload = request.httprequest.get_json(silent=True)
            try:
                request.env["mercadolibre.notification"].sudo().receive(
                    backend_id, payload
                )
            except Exception:
                _logger.exception(
                    "Mercado Libre notification failed for backend %s",
                    backend_id,
                )
        return ""
