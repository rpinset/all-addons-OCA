# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

# pylint: disable=consider-merging-classes-inherited
from urllib.parse import urlsplit

from odoo import models
from odoo.exceptions import UserError

from ..services.client import LOCAL_HOSTS, SifendeTransportError
from .edi_connector import SOFT_RELOAD, WEBHOOK_PATH

WEBHOOK_EVENTS = ("documento.aprobado", "documento.rechazado", "documento.cancelado")


class EDIConnectorWebhook(models.Model):
    _inherit = "l10n_py.edi.connector"

    def action_sifende_register_webhook(self):
        self.ensure_one()
        self._sifende_check_webhook_provider()
        url = self._sifende_public_webhook_url()
        existing = self._sifende_find_webhook(url)
        if existing:
            self.sudo().sifende_webhook_id = existing["id"]
            if existing.get("activo") is False:
                message = self.env._(
                    "El webhook está desactivado en Sifende y no avisará a Odoo. "
                    "Actívelo en el panel de Sifende, o pulse «Quitar webhook» y "
                    "regístrelo de nuevo."
                )
                return self._sifende_notify(message, "warning")
            if self.sudo().sifende_webhook_secret:
                message = self.env._("El webhook ya está registrado en Sifende.")
            else:
                message = self.env._(
                    "La URL ya estaba registrada en Sifende, pero el secreto solo se "
                    "muestra al crearlo. Use «Rotar secreto» para obtener uno nuevo."
                )
            return self._sifende_notify(message, "warning")
        response = self._sifende_webhook_call(
            "POST", "", json_body={"url": url, "eventos": list(WEBHOOK_EVENTS)}
        )
        if not (response.ok and isinstance(response.body, dict)):
            raise UserError(response.failure_message(self.env))
        self._sifende_store_webhook(response.body)
        return self._sifende_notify(
            self.env._("Webhook registrado en Sifende: %(url)s", url=url), "success"
        )

    def action_sifende_rotate_webhook_secret(self):
        self.ensure_one()
        self._sifende_check_webhook_provider()
        webhook_id = self._sifende_require_webhook_id()
        response = self._sifende_webhook_call("POST", f"/{webhook_id}/rotar")
        if response.status_code == 404:
            # sin excepción: el rollback del RPC deshacería la limpieza
            self._sifende_forget_webhook()
            return self._sifende_notify(
                self._sifende_webhook_missing_message(), "warning"
            )
        if not (response.ok and isinstance(response.body, dict)):
            raise UserError(response.failure_message(self.env))
        self._sifende_store_webhook(response.body)
        return self._sifende_notify(
            self.env._("Secreto del webhook rotado y guardado."), "success"
        )

    def action_sifende_remove_webhook(self):
        self.ensure_one()
        self._sifende_check_webhook_provider()
        webhook_id = self._sifende_require_webhook_id()
        response = self._sifende_webhook_call("DELETE", f"/{webhook_id}")
        if not (response.ok or response.status_code == 404):
            raise UserError(response.failure_message(self.env))
        self._sifende_forget_webhook()
        return self._sifende_notify(
            self.env._("Webhook eliminado de Sifende."), "success"
        )

    def _sifende_check_webhook_provider(self):
        if self.provider_type != "sifende":
            raise UserError(self.env._("El conector no es de Sifende."))
        if not self.env.is_system():
            raise UserError(
                self.env._("Solo un administrador puede gestionar el webhook.")
            )

    def _sifende_public_webhook_url(self):
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        ).rstrip("/")
        parts = urlsplit(base_url)
        if parts.scheme != "https" or (parts.hostname or "") in LOCAL_HOSTS:
            raise UserError(
                self.env._(
                    "Sifende exige una URL pública con HTTPS y la URL base de Odoo "
                    "(web.base.url) es «%(url)s». Configúrela en Ajustes > Técnico > "
                    "Parámetros del sistema.",
                    url=base_url,
                )
            )
        return f"{base_url}{WEBHOOK_PATH}/{self.id}"

    def _sifende_find_webhook(self, url):
        response = self._sifende_webhook_call("GET", "")
        if not (response.ok and isinstance(response.body, list)):
            raise UserError(response.failure_message(self.env))
        for webhook in response.body:
            if (webhook.get("url") or "").rstrip("/") == url:
                return webhook
        return None

    def _sifende_webhook_call(self, method, suffix, json_body=None):
        try:
            return self._sifende_client().request(
                method,
                f"/contribuyente/webhooks{suffix}",
                operation="event",
                json_body=json_body,
            )
        except SifendeTransportError as e:
            raise UserError(
                self.env._("No se pudo contactar a SIFENDE: %(error)s", error=e)
            ) from e

    def _sifende_store_webhook(self, body):
        self.sudo().write(
            {
                "sifende_webhook_id": (body.get("endpoint") or {}).get("id"),
                "sifende_webhook_secret": body.get("secreto"),
            }
        )

    def _sifende_forget_webhook(self):
        self.sudo().write({"sifende_webhook_id": 0, "sifende_webhook_secret": False})

    def _sifende_require_webhook_id(self):
        webhook_id = self.sudo().sifende_webhook_id
        if not webhook_id:
            raise UserError(self.env._("El conector no tiene un webhook registrado."))
        return webhook_id

    def _sifende_webhook_missing_message(self):
        return self.env._("El webhook ya no existe en Sifende. Regístrelo de nuevo.")

    def _sifende_notify(self, message, notification_type):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Webhook de Sifende"),
                "message": message,
                "type": notification_type,
                "sticky": notification_type != "success",
                "next": SOFT_RELOAD,
            },
        }
