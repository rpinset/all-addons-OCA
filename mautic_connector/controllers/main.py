# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import http
from odoo.http import request

from ..exception import MauticApiError

_logger = logging.getLogger(__name__)


class MauticController(http.Controller):
    @http.route(
        "/mautic/oauth2/callback",
        type="http",
        auth="user",
        website=False,
    )
    def oauth2_callback(self, code=None, state=None, error=None, **kwargs):
        """Receive the OAuth2 redirect from Mautic and store the tokens.

        ``state`` carries the id of the ``mautic.backend`` record that
        started the authorization flow (see
        :meth:`MauticBackend.action_authorize`).
        """
        if error:
            return request.make_response(
                f"Mautic authorization was denied or failed: {error}", status=400
            )
        if not (code and state):
            return request.make_response(
                "Missing 'code' or 'state' parameter in Mautic callback.", status=400
            )
        backend = request.env["mautic.backend"].browse(int(state)).exists()
        if not backend:
            return request.make_response("Unknown Mautic backend.", status=404)
        try:
            backend._exchange_authorization_code(code)
        except MauticApiError as exc:
            _logger.exception("Mautic OAuth2 token exchange failed")
            return request.make_response(str(exc), status=502)
        return request.redirect(
            f"/web#model=mautic.backend&view_type=form&id={backend.id}"
        )
