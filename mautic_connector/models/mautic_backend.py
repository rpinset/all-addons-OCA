# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from datetime import timedelta
from urllib.parse import urlencode

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..exception import MauticApiError

_logger = logging.getLogger(__name__)

TOKEN_PATH = "/oauth/v2/token"
AUTHORIZE_PATH = "/oauth/v2/authorize"
TOKEN_SAFETY_MARGIN = timedelta(seconds=60)


class MauticBackend(models.Model):
    _name = "mautic.backend"
    _inherit = "connector.backend"
    _description = "Mautic Backend"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    api_url = fields.Char(
        string="Mautic URL",
        required=True,
        help="Base URL of the Mautic instance, without a trailing slash, "
        "e.g. https://mautic.example.com",
    )
    client_id = fields.Char(required=True)
    client_secret = fields.Char(required=True)
    redirect_url = fields.Char(
        string="Callback URL",
        compute="_compute_redirect_url",
        help="Register this URL as the 'Redirect URI' of the Mautic API "
        "credentials.",
    )
    access_token = fields.Char(copy=False, groups="base.group_system")
    refresh_token = fields.Char(copy=False, groups="base.group_system")
    token_expires_at = fields.Datetime(copy=False)
    state = fields.Selection(
        [("not_connected", "Not Connected"), ("connected", "Connected")],
        compute="_compute_state",
        store=True,
    )

    @api.depends("refresh_token")
    def _compute_state(self):
        for backend in self:
            backend.state = "connected" if backend.refresh_token else "not_connected"

    def _compute_redirect_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for backend in self:
            backend.redirect_url = f"{base_url}/mautic/oauth2/callback"

    def action_authorize(self):
        """Open the Mautic authorization page in a new window.

        Mautic will redirect back to the ``/mautic/oauth2/callback`` route
        with an authorization ``code``, identifying the backend through the
        ``state`` query parameter.
        """
        self.ensure_one()
        if not (self.api_url and self.client_id and self.client_secret):
            raise UserError(
                _("Please configure the Mautic URL, Client ID and Client Secret first.")
            )
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_url,
            "state": self.id,
        }
        url = f"{self.api_url.rstrip('/')}{AUTHORIZE_PATH}?{urlencode(params)}"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

    def action_test_connection(self):
        self.ensure_one()
        token = self._get_access_token()
        url = f"{self.api_url.rstrip('/')}/api/contacts"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(
                url, headers=headers, params={"limit": 1}, timeout=30
            )
        except requests.RequestException as exc:
            raise UserError(_("Could not reach Mautic: %s") % exc) from exc
        if not response.ok:
            raise UserError(
                _("Mautic API error %(code)s: %(body)s")
                % {"code": response.status_code, "body": response.text}
            )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Connection to Mautic successful."),
                "type": "success",
                "sticky": False,
            },
        }

    def _get_access_token(self, force_refresh=False):
        """Return a valid access token for this backend, refreshing it if needed."""
        self.ensure_one()
        if not self.refresh_token:
            raise UserError(
                _(
                    "Backend %s is not connected to Mautic yet. Use the "
                    "'Connect to Mautic' button first."
                )
                % self.name
            )
        if force_refresh or self._is_token_expired():
            self._refresh_access_token()
        return self.access_token

    def _is_token_expired(self):
        self.ensure_one()
        if not self.access_token or not self.token_expires_at:
            return True
        return fields.Datetime.now() >= (self.token_expires_at - TOKEN_SAFETY_MARGIN)

    def _refresh_access_token(self):
        """Exchange the current refresh token for a new access token.

        Locks the backend row so concurrent calls do not refresh (and thus
        invalidate) the token at the same time.
        """
        self.ensure_one()
        self.env.cr.execute(
            f"SELECT id FROM {self._table} WHERE id = %s FOR UPDATE",
            (self.id,),
        )
        self.invalidate_recordset(["access_token", "refresh_token", "token_expires_at"])
        if not self._is_token_expired():
            # another call already refreshed it while we were waiting on the lock
            return
        self._exchange_token(
            {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            }
        )

    def _exchange_authorization_code(self, code):
        """Exchange an OAuth authorization code for the first access token."""
        self.ensure_one()
        self._exchange_token(
            {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_url,
            }
        )

    def _exchange_token(self, payload):
        self.ensure_one()
        url = f"{self.api_url.rstrip('/')}{TOKEN_PATH}"
        try:
            response = requests.post(url, data=payload, timeout=30)
        except requests.RequestException as exc:
            raise MauticApiError(_("Could not reach Mautic: %s") % exc) from exc
        if not response.ok:
            raise MauticApiError(
                _("Mautic OAuth error (%(code)s): %(body)s")
                % {"code": response.status_code, "body": response.text},
                status_code=response.status_code,
            )
        data = response.json()
        expires_in = data.get("expires_in", 0)
        self.sudo().write(
            {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token", self.refresh_token),
                "token_expires_at": fields.Datetime.now()
                + timedelta(seconds=expires_in),
            }
        )
