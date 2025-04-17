import logging

from werkzeug.exceptions import Unauthorized

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class VerticalLiftController(http.Controller):
    @http.route(["/vertical-lift"], type="http", auth="public", csrf=False)
    def vertical_lift(self, answer, secret):
        if secret == self._get_env_secret():
            rec = request.env["vertical.lift.command"].sudo().record_answer(answer)
            return str(rec.id)
        else:
            _logger.error("secret mismatch: %r", secret)
            return Unauthorized()

    def _get_env_secret(self):
        secret = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("stock_vertical_lift.secret", None)
        )
        if not secret:
            msg = self.env._(
                "Vertical Lift secret not set. "
                "Please set it in Inventory/Settings/Vertical Lift"
            )
            _logger.error(msg)
            raise UserError(msg)
        return secret
