# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import hashlib
import secrets
from datetime import timedelta
from urllib.parse import urlencode

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError


class MercadoLibreBackend(models.Model):
    _name = "mercadolibre.backend"
    _inherit = ["connector.backend", "mail.thread", "mail.activity.mixin"]
    _description = "Mercado Libre Backend"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("connected", "Connected"),
            ("error", "Error"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    site_id = fields.Selection(
        selection="_select_sites",
        required=True,
    )
    seller_id = fields.Char(
        string="Seller ID",
        readonly=True,
        index=True,
        copy=False,
    )
    nickname = fields.Char(readonly=True, copy=False)
    versions = fields.Selection(
        selection="_select_versions",
        required=True,
        default="user_product",
    )
    client_id = fields.Char(string="Client ID", required=True)
    client_secret = fields.Char(
        required=True,
        groups="connector_mercadolibre.group_mercadolibre_manager",
        copy=False,
    )
    redirect_uri = fields.Char(required=True)
    code_verifier = fields.Char(
        groups="connector_mercadolibre.group_mercadolibre_manager",
        copy=False,
    )
    access_token = fields.Char(
        groups="connector_mercadolibre.group_mercadolibre_manager",
        copy=False,
    )
    refresh_token = fields.Char(
        groups="connector_mercadolibre.group_mercadolibre_manager",
        copy=False,
    )
    access_token_expires_at = fields.Datetime(copy=False)
    auth_error = fields.Text(readonly=True, copy=False)
    user_payload = fields.Json(
        readonly=True,
        groups="connector_mercadolibre.group_mercadolibre_manager",
        copy=False,
    )
    notification_ids = fields.One2many(
        comodel_name="mercadolibre.notification",
        inverse_name="backend_id",
    )
    notification_count = fields.Integer(compute="_compute_notification_count")

    @api.model
    def _select_sites(self):
        """Sites a backend can sell on. Addons may extend the list."""
        return [
            ("MLA", "Argentina"),
            ("MLB", "Brazil"),
            ("MLM", "Mexico"),
            ("MLC", "Chile"),
            ("MCO", "Colombia"),
            ("MLU", "Uruguay"),
            ("MPE", "Peru"),
            ("MEC", "Ecuador"),
            ("MLV", "Venezuela"),
        ]

    @api.model
    def _select_versions(self):
        """Component version key. Addons may add a version."""
        return [
            ("legacy_item", "Legacy items"),
            ("user_product", "User products"),
        ]

    @api.depends("notification_ids")
    def _compute_notification_count(self):
        counts = {
            backend.id: count
            for backend, count in self.env["mercadolibre.notification"]._read_group(
                domain=[("backend_id", "in", self.ids)],
                groupby=["backend_id"],
                aggregates=["__count"],
            )
        }
        for backend in self:
            backend.notification_count = counts.get(backend.id, 0)

    def write(self, vals):
        if "site_id" in vals:
            for backend in self.filtered("seller_id"):
                if vals["site_id"] != backend.site_id:
                    message = self.env._(
                        "The site cannot change after the seller is connected."
                    )
                    raise UserError(message)
        return super().write(vals)

    def button_connect(self):
        self.ensure_one()
        verifier, challenge = self._generate_pkce()
        self.code_verifier = verifier
        params = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "state": str(self.id),
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"https://auth.mercadolibre.com/authorization?{params}",
            "target": "self",
        }

    def button_disconnect(self):
        self.write(
            {
                "access_token": False,
                "refresh_token": False,
                "access_token_expires_at": False,
                "code_verifier": False,
                "seller_id": False,
                "nickname": False,
                "user_payload": False,
                "auth_error": False,
                "state": "draft",
            }
        )

    def button_refresh_token(self):
        for backend in self:
            description = self.env._(
                "Refresh Mercado Libre token for %(name)s",
                name=backend.display_name,
            )
            backend.with_delay(
                identity_key=f"refresh:{backend.id}",
                description=description,
            )._job_refresh_token()

    def action_view_notifications(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "connector_mercadolibre.action_mercadolibre_notification"
        )
        action["domain"] = [("backend_id", "=", self.id)]
        action["context"] = {"default_backend_id": self.id}
        return action

    def _component_usage_backend(self, usage, model_name=None):
        self.ensure_one()
        with self.work_on(model_name or self._name) as work:
            return work.component(usage=usage)

    def _generate_pkce(self):
        verifier = secrets.token_urlsafe(64)
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        return verifier, challenge

    def _lock(self):
        """Lock the backend row. The refresh token can be used only once."""
        self.ensure_one()
        self.env.cr.execute(
            "SELECT id FROM mercadolibre_backend WHERE id = %s FOR UPDATE",
            (self.id,),
        )
        self.invalidate_recordset()

    def _apply_token_payload(self, payload):
        expires_in = int(payload.get("expires_in") or 0)
        self.write(
            {
                "access_token": payload.get("access_token"),
                "refresh_token": payload.get("refresh_token"),
                "access_token_expires_at": fields.Datetime.now()
                + timedelta(seconds=expires_in),
            }
        )

    def _versions_from_user(self, user_payload):
        tags = user_payload.get("tags") or []
        if "user_product_seller" in tags:
            return "user_product"
        return "legacy_item"

    def _job_exchange_code(self, code):
        """Exchange an authorization code and store the seller account."""
        self.ensure_one()
        self._lock()
        adapter = self._component_usage_backend("backend.adapter")
        if not self.access_token:
            try:
                token = adapter.exchange_authorization_code(code)
            except RetryableJobError:
                raise
            except FailedJobError as error:
                self.write(
                    {
                        "state": "error",
                        "auth_error": str(error),
                        "code_verifier": False,
                    }
                )
                return
            self._apply_token_payload(token)
        user_payload = adapter.read("/users/me")
        self.write(
            {
                "seller_id": str(user_payload.get("id") or ""),
                "nickname": user_payload.get("nickname"),
                "user_payload": user_payload,
                "versions": self._versions_from_user(user_payload),
                "state": "connected",
                "auth_error": False,
                "code_verifier": False,
            }
        )

    def _job_refresh_token(self):
        """Rotate the access token. An invalid refresh token is not retried."""
        self.ensure_one()
        self._lock()
        if not self.refresh_token:
            self.write(
                {
                    "state": "error",
                    "auth_error": self.env._("Missing refresh token."),
                }
            )
            return
        adapter = self._component_usage_backend("backend.adapter")
        try:
            token = adapter.refresh_access_token(self.refresh_token)
        except RetryableJobError:
            raise
        except FailedJobError as error:
            if getattr(error, "error_code", None) == "invalid_grant":
                self.write({"state": "error", "auth_error": str(error)})
                return
            raise
        self._apply_token_payload(token)
        if self.state != "draft":
            self.write({"state": "connected", "auth_error": False})

    @api.model
    def cron_refresh_tokens(self):
        horizon = fields.Datetime.now() + timedelta(hours=1)
        backends = self.search(
            [
                ("state", "=", "connected"),
                ("access_token_expires_at", "!=", False),
                ("access_token_expires_at", "<=", horizon),
            ]
        )
        backends.button_refresh_token()
