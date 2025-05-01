# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import os

from passlib.utils import consteq
from werkzeug.exceptions import Unauthorized

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VerticalLiftController(http.Controller):
    @http.route(["/vertical-lift"], type="http", auth="public", csrf=False)
    def vertical_lift(self, answer, secret):
        if self._security_check(secret):
            rec = request.env["vertical.lift.command"].sudo().record_answer(answer)
            return str(rec.id)
        else:
            _logger.error("secret mismatch: %r", secret)
            return Unauthorized()

    def _security_check(self, secret):
        if not secret or not secret.strip():
            msg = "Vertical Lift secret not received."
            _logger.error(msg)
            return False
        server_secret = self._get_env_secret()
        param_secret = self._get_param_secret()
        if not server_secret and not param_secret:
            msg = (
                "Vertical Lift secret not configured. "
                "Please set it in Inventory/Settings/Vertical Lift "
                "or in the environment variable VERTICAL_LIFT_SECRET."
            )
            _logger.error(msg)
            return False
        # param secret takes precedence over env secret as it can be customized by DB
        if param_secret:
            return consteq(secret, param_secret)
        return consteq(secret, server_secret)

    def _get_env_secret(self):
        return os.getenv("VERTICAL_LIFT_SECRET", "")

    def _get_param_secret(self):
        secret = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("stock_vertical_lift.secret", None)
        )
        return secret
