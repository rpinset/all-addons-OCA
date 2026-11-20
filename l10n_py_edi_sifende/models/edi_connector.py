# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import time

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

from ..services import event_key
from ..services.client import (
    RETRY_AFTER_CAP,
    RETRY_BACKOFF,
    TRANSIENT_SLUGS,
    TRANSIENT_STATUS,
    SifendeClient,
    SifendeTransportError,
    insecure_url_message,
    is_secure_url,
    mask_key,
)
from ..services.request_builder import SifendeRequestBuilder

DEFAULT_BASE_URL = "https://api.sifende.com.py"
PANEL_BILLING_URL = "https://app.sifende.com.py"
DEFAULT_SERIES = "AA"

KUDE_MAX_WAIT = 30
KUDE_DEFAULT_POLL = 5
SETUP_SLUGS = (
    "configuracion-incompleta",
    "timbrado-no-vigente",
    "certificado-no-vigente",
    "idempotency-key-reused",
)

APPROVED_STATES = ("APROBADO", "APROBADO_OBSERVACION")
PENDING_STATES = ("PENDIENTE", "EN_LOTE")
# estados de un evento (cancelación, inutilización): sólo APROBADO lo confirma
EVENT_APPROVED_STATES = ("APROBADO",)
EVENT_REJECTED_STATE = "RECHAZADO"

WEBHOOK_PATH = "/l10n_py_edi_sifende/webhook"

GROUP_READONLY = "account.group_account_readonly"
GROUP_BILLING = "account.group_account_invoice"
GROUP_MANAGER = "account.group_account_manager"
READ_GROUPS = (GROUP_READONLY, GROUP_BILLING)

SOFT_RELOAD = {"type": "ir.actions.client", "tag": "soft_reload"}

SANDBOX_KEY_PREFIX = "sk_sandbox_"
KEY_PREFIX_ENVIRONMENTS = {
    "sk_live_": "prod",
    SANDBOX_KEY_PREFIX: "test",
    "sk_test_": "test",
}


class EDIConnector(models.Model):
    _inherit = "l10n_py.edi.connector"

    provider_type = fields.Selection(
        selection_add=[("sifende", "Sifende")],
        ondelete={"sifende": "cascade"},
    )
    company_id = fields.Many2one(string="Empresa")
    environment = fields.Selection(string="Ambiente")
    timeout = fields.Integer(string="Tiempo de espera (segundos)")
    active = fields.Boolean(string="Activo")
    sifende_api_key = fields.Char(
        string="API key de Sifende",
        groups="base.group_system",
        copy=False,
    )
    sifende_base_url = fields.Char(
        string="URL de Sifende",
        default=DEFAULT_BASE_URL,
        groups="base.group_system",
    )
    sifende_ambiente = fields.Char(
        string="Ambiente de la API key",
        readonly=True,
        copy=False,
    )

    sifende_webhook_url = fields.Char(
        string="URL del webhook",
        compute="_compute_sifende_webhook_url",
    )
    sifende_webhook_id = fields.Integer(
        string="Webhook en Sifende",
        groups="base.group_system",
        readonly=True,
        copy=False,
    )
    sifende_webhook_secret = fields.Char(
        string="Secreto del webhook",
        groups="base.group_system",
        copy=False,
    )

    @api.depends("provider_type")
    def _compute_sifende_webhook_url(self):
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        ).rstrip("/")
        for connector in self:
            connector.sifende_webhook_url = (
                f"{base_url}{WEBHOOK_PATH}/{connector.id}"
                if connector.id and connector.provider_type == "sifende"
                else False
            )

    @api.constrains("sifende_base_url")
    def _check_sifende_base_url(self):
        for connector in self.sudo():
            if connector.sifende_base_url and not is_secure_url(
                connector.sifende_base_url
            ):
                raise ValidationError(insecure_url_message(self.env))

    @api.constrains("environment", "sifende_api_key")
    def _check_sifende_environment(self):
        for connector in self.sudo():
            if connector.provider_type == "sifende":
                connector._sifende_check_environment(ValidationError)

    def _sifende_key_environment(self):
        key = self.sudo().sifende_api_key or ""
        for prefix, environment in KEY_PREFIX_ENVIRONMENTS.items():
            if key.startswith(prefix):
                return environment
        return None

    def _sifende_is_sandbox(self):
        self.ensure_one()
        connector = self.sudo()
        return connector.sifende_ambiente == "SANDBOX" or (
            connector.sifende_api_key or ""
        ).startswith(SANDBOX_KEY_PREFIX)

    def _sifende_check_environment(self, error=UserError):
        self.ensure_one()
        key_environment = self._sifende_key_environment()
        if key_environment and key_environment != self.environment:
            labels = dict(self._fields["environment"].selection)
            raise error(
                self.env._(
                    "El conector está en ambiente «%(local)s» pero la API key es de "
                    "«%(remote)s» (prefijo %(prefix)s). Cambie el ambiente del "
                    "conector o use una API key del mismo ambiente.",
                    local=labels[self.environment],
                    remote=labels[key_environment],
                    prefix=mask_key(self.sudo().sifende_api_key),
                )
            )

    def write(self, vals):
        if "sifende_api_key" in vals and "sifende_ambiente" not in vals:
            vals = {**vals, "sifende_ambiente": False}
        return super().write(vals)

    # === Interfaz pública del conector ===

    def _sifende_check_access(self, *groups):
        self.ensure_one()
        # OCA llama con sudo(): se valida al usuario real, no al superusuario
        connector = self.sudo(False)
        if connector.env.su:
            return
        connector.check_access("read")
        if not any(connector.env.user.has_group(group) for group in groups):
            raise AccessError(
                self.env._("No tiene permisos para operar el conector de Sifende.")
            )

    @api.private
    def send_document(self, invoice_data):
        if self.provider_type != "sifende":
            return super().send_document(invoice_data)
        self._sifende_check_access(GROUP_BILLING)
        self._sifende_check_environment()
        return self._sifende_send_document(invoice_data)

    @api.private
    def check_status(self, document_id):
        if self.provider_type != "sifende":
            return super().check_status(document_id)
        self._sifende_check_access(*READ_GROUPS)
        return self._sifende_check_status(document_id)

    @api.private
    def cancel_document(self, document_id, reason=""):
        if self.provider_type != "sifende":
            return super().cancel_document(document_id, reason)
        self._sifende_check_access(GROUP_BILLING)
        self._sifende_check_environment()
        return self._sifende_cancel_document(document_id, reason)

    @api.private
    def inutilize_range(self, data):
        if self.provider_type != "sifende":
            return super().inutilize_range(data)
        self._sifende_check_access(GROUP_MANAGER)
        self._sifende_check_environment()
        return self._sifende_inutilize_range(data)

    @api.private
    def preview_document(self, invoice_data):
        if self.provider_type != "sifende":
            return super().preview_document(invoice_data)
        raise UserError(self._sifende_no_preview_message())

    @api.private
    def preview_qr(self, invoice_data):
        if self.provider_type != "sifende":
            return super().preview_qr(invoice_data)
        raise UserError(self._sifende_no_preview_message())

    def test_connection(self):
        if self.provider_type != "sifende":
            return super().test_connection()
        self._sifende_check_access(GROUP_MANAGER)
        self._sifende_check_environment()
        return self._sifende_test_connection()

    def _sifende_fetch_xml(self, cdc, document=None):
        self.ensure_one()
        response = self._sifende_client().request(
            "GET",
            f"/documento-electronico/{cdc}/xml",
            operation="download_xml",
            document=document,
            cdc=cdc,
            binary=True,
        )
        if response.ok and response.content:
            return response.content
        if response.status_code == 409:
            raise UserError(
                self.env._("SIFENDE todavía no tiene el XML de este documento.")
            )
        raise UserError(response.failure_message(self.env))

    def _sifende_fetch_kude(self, cdc, document=None, max_wait=KUDE_MAX_WAIT):
        self.ensure_one()
        params = None
        waited = 0
        while True:
            response = self._sifende_client().request(
                "GET",
                f"/documento-electronico/{cdc}/kude",
                operation="download_pdf",
                document=document,
                cdc=cdc,
                params=params,
                binary=True,
            )
            if response.status_code == 200 and response.content:
                return response.content
            if response.status_code != 202:
                raise UserError(response.failure_message(self.env))
            wait = max(
                1, min(response.retry_after or KUDE_DEFAULT_POLL, RETRY_AFTER_CAP)
            )
            if waited + wait > max_wait:
                raise UserError(
                    self.env._(
                        "SIFENDE sigue preparando el KuDE; se reintentará más tarde."
                    )
                )
            time.sleep(wait)
            waited += wait
            params = {"soloConsulta": "true"}

    # === Operaciones ===

    def _sifende_send_document(self, invoice_data):
        self.ensure_one()
        extra = invoice_data.get("sifende") or {}
        payload = SifendeRequestBuilder(self.env, self._sifende_enum_name).build(
            invoice_data
        )
        key = extra.get("idempotencyKey")
        document = (
            self.env["account.move"].browse(extra["moveId"])
            if extra.get("moveId")
            else None
        )
        try:
            response = self._sifende_client().request(
                "POST",
                "/documento-electronico",
                operation="send",
                json_body=payload,
                idempotency_key=key,
                retries=len(RETRY_BACKOFF) if key else 0,
                document=document,
            )
        except SifendeTransportError as e:
            return {
                "success": False,
                "edi_status": "error",
                "transient": True,
                "error": self.env._(
                    "No se pudo contactar a SIFENDE (%(error)s). Al reintentar se "
                    "usará la misma clave de idempotencia: no se duplica el documento.",
                    error=e,
                ),
            }
        if response.status_code in (200, 201, 202) and isinstance(response.body, dict):
            body = response.body
            return {
                "success": True,
                "result": {
                    "cdc": body.get("cdc"),
                    "qr": body.get("qrUrl"),
                    "numero": body.get("numeroFormateado")
                    or body.get("numeroDocumento"),
                    "estado": body.get("estado") or "PENDIENTE",
                },
            }
        return self._sifende_send_failure(response)

    def _sifende_send_failure(self, response):
        slug = response.slug
        failure = {"success": False, "edi_status": "error", "transient": False}
        if slug in ("document-number-in-use", "document-number-voided"):
            body = response.body if isinstance(response.body, dict) else {}
            failure["number_conflict"] = True
            failure["existing_cdc"] = body.get("cdc") or body.get("cdcExistente")
            failure["error"] = self._sifende_number_conflict_message(response)
        elif slug in TRANSIENT_SLUGS or response.status_code in TRANSIENT_STATUS:
            failure["transient"] = True
            failure["error"] = self.env._(
                "SIFENDE no pudo procesar el envío ahora (HTTP %(status)s). "
                "Reintente: se usará la misma clave de idempotencia, "
                "sin duplicar el documento.",
                status=response.status_code,
            )
        elif slug == "timbrado-mismatch":
            failure["error"] = self.env._(
                "El timbrado de Odoo no coincide con el de SIFENDE. %(detail)s",
                detail=response.detail or "",
            )
        elif slug == "document-number-requires-voiding":
            failure["edi_status"] = "rejected"
            failure["error"] = self.env._(
                "El número de este documento ya pertenece a uno rechazado por SIFEN "
                "y no se puede reenviar. Inutilice el número desde Facturación "
                "Electrónica > Inutilización de números, cancele este documento "
                "(Restablecer a borrador y Cancelar) y emita uno nuevo. %(detail)s",
                detail=response.detail or "",
            )
        elif slug in (
            "document-quota-exceeded",
            "emission-suspended",
            "plan-operation-not-allowed",
        ):
            failure["error"] = self.env._(
                "Su plan de SIFENDE no permite emitir ahora: %(detail)s Revise la "
                "facturación en %(url)s.",
                detail=response.detail or "",
                url=PANEL_BILLING_URL,
            )
        elif slug in SETUP_SLUGS:
            failure["error"] = self._sifende_setup_message(slug, response)
        elif response.status_code in (400, 422):
            failure["edi_status"] = "rejected"
            failure["error"] = response.failure_message(self.env)
        else:
            failure["error"] = response.failure_message(self.env)
        return failure

    def _sifende_setup_message(self, slug, response):
        url = PANEL_BILLING_URL
        if slug == "configuracion-incompleta":
            message = self.env._(
                "Falta completar la configuración del contribuyente en Sifende "
                "(dirección, actividad económica, certificado o CSC). Complétela en "
                "el panel de Sifende (%(url)s) y pulse «Reintentar».",
                url=url,
            )
        elif slug == "timbrado-no-vigente":
            message = self.env._(
                "El timbrado no está vigente en Sifende. Cárguelo o renuévelo en el "
                "panel de Sifende (%(url)s) y pulse «Reintentar».",
                url=url,
            )
        elif slug == "certificado-no-vigente":
            message = self.env._(
                "El certificado digital del contribuyente no está vigente en "
                "Sifende. Cargue uno vigente en el panel de Sifende (%(url)s) y "
                "pulse «Reintentar».",
                url=url,
            )
        else:
            message = self.env._(
                "Sifende ya había recibido esta clave de envío con otros datos. "
                "Pulse «Reintentar»: se enviará con una clave nueva."
            )
        return f"{message}\n{response.detail}" if response.detail else message

    def _sifende_number_conflict_message(self, response):
        body = response.body if isinstance(response.body, dict) else {}
        cdc = body.get("cdc") or body.get("cdcExistente")
        if response.slug == "document-number-voided":
            message = self.env._(
                "El número está inutilizado en SIFENDE y no se puede usar. %(detail)s",
                detail=response.detail or "",
            )
        else:
            message = self.env._("El número de documento ya está en uso en SIFENDE.")
            if cdc:
                message += " " + self.env._("CDC existente: %(cdc)s.", cdc=cdc)
        return (
            message
            + " "
            + self.env._(
                "Suba «Número Desde» del timbrado al siguiente número libre del punto "
                "(panel de Sifende > Numeración) y pulse «Renumerar» en este documento."
            )
        )

    def _sifende_check_status(self, cdc, log=True):
        self.ensure_one()
        try:
            response = self._sifende_client().request(
                "GET",
                f"/documento-electronico/status/{cdc}",
                operation="status",
                cdc=cdc,
                log=log,
            )
        except SifendeTransportError as e:
            return {"success": False, "error": str(e)}
        if not (response.ok and isinstance(response.body, dict)):
            return {"success": False, "error": response.failure_message(self.env)}
        body = response.body
        estado = body.get("estado")
        result = dict(body)
        message = body.get("mensajeRechazo")
        if estado in APPROVED_STATES:
            result["status"] = "Aprobado"
            return {"success": True, "result": result}
        if estado == "RECHAZADO":
            result["status"] = "Rechazado"
            return {"success": False, "result": result, "error": message or estado}
        return {"success": False, "result": result, "error": message or estado}

    def _sifende_cancel_document(self, cdc, reason):
        self.ensure_one()
        reason = (reason or self.env.context.get("l10n_py_cancel_motive") or "").strip()
        if len(reason) < 5:
            reason = self.env._("Cancelación solicitada desde Odoo")
        move = (
            self.env["account.move"]
            .sudo()
            .search(
                [("l10n_py_cdc", "=", cdc), ("company_id", "=", self.company_id.id)],
                limit=1,
            )
        )
        return self._sifende_event(
            "cancel",
            f"/documento-electronico/{cdc}/cancelar",
            {"motivo": reason[:500]},
            cdc,
            record=move,
        )

    def _sifende_inutilize_range(self, data):
        self.ensure_one()
        try:
            timbrado = int(data["timbrado"])
        except (TypeError, ValueError) as e:
            raise UserError(self.env._("El timbrado debe ser numérico.")) from e
        inutilization = self.env["l10n_py.number.inutilization"].browse(
            self.env.context.get("l10n_py_inutilization_id")
        )
        authorization = inutilization.authorization_id
        code = authorization.l10n_latam_document_type_id.code
        payload = {
            "numeroTimbrado": timbrado,
            "establecimiento": data["establecimiento"],
            "puntoExpedicion": data["punto"],
            "numeroInicio": data["numeroDesde"],
            "numeroFin": data["numeroHasta"],
            "tipoDocumento": int(code or data["tipoDocumento"]),
            "motivo": (data.get("motivo") or "").strip()[:500],
        }
        # OCA propone «AA» en todo timbrado y no lo muestra: no es una serie real
        if authorization.series and authorization.series != DEFAULT_SERIES:
            payload["serie"] = authorization.series
        return self._sifende_event(
            "event", "/documento-electronico/inutilizar", payload, record=inutilization
        )

    def _sifende_event(self, operation, path, payload, cdc=None, record=None):
        key = event_key.get_or_create(record)
        try:
            response = self._sifende_client().request(
                "POST",
                path,
                operation=operation,
                json_body=payload,
                idempotency_key=key,
                retries=len(RETRY_BACKOFF),
                cdc=cdc,
            )
        except SifendeTransportError as e:
            return {"success": False, "error": str(e)}
        body = response.body if isinstance(response.body, dict) else {}
        if not response.ok:
            if self._sifende_is_definitive(response):
                event_key.forget(record, committed=True)
            return {"success": False, "error": response.failure_message(self.env)}
        state = body.get("estadoEvento")
        if state in EVENT_APPROVED_STATES:
            event_key.forget(record, committed=False)
            return {"success": True, "result": body}
        if state == EVENT_REJECTED_STATE:
            event_key.forget(record, committed=True)
            return {
                "success": False,
                "result": body,
                "error": body.get("mensajeRespuesta")
                or self.env._("SIFEN rechazó el evento."),
            }
        # sin estado, pendiente o desconocido: no está aprobado; se conserva la clave
        return {
            "success": False,
            "result": body,
            "error": self.env._(
                "SIFEN no confirmó la aprobación del evento (estado: %(state)s). "
                "Vuelva a intentarlo en unos minutos.",
                state=state or self.env._("sin estado"),
            ),
        }

    @staticmethod
    def _sifende_is_definitive(response):
        # un fallo transitorio o un evento ya pendiente se retoma con la misma clave
        return not (
            response.status_code in TRANSIENT_STATUS
            or response.status_code == 409
            or response.slug in TRANSIENT_SLUGS
        )

    def _sifende_test_connection(self):
        self.ensure_one()
        try:
            response = self._sifende_client().request(
                "GET", "/contribuyente", operation="validate"
            )
        except SifendeTransportError as e:
            raise UserError(
                self.env._("No se pudo contactar a SIFENDE: %(error)s", error=e)
            ) from e
        if not (response.ok and isinstance(response.body, dict)):
            raise UserError(response.failure_message(self.env))
        taxpayer = response.body
        environment = taxpayer.get("ambiente")
        self.sudo().sifende_ambiente = environment
        expected = ("PROD",) if self.environment == "prod" else ("DEV", "SANDBOX")
        if environment not in expected:
            raise UserError(
                self.env._(
                    "El conector está en ambiente «%(local)s» pero la API key es del "
                    "ambiente %(remote)s de SIFENDE.",
                    local=dict(self._fields["environment"].selection)[self.environment],
                    remote=environment,
                )
            )
        ready = (taxpayer.get("estadoConfiguracion") or {}).get("listoParaEmitir")
        warnings = self._sifende_config_warnings(taxpayer)
        lines = [
            self.env._("Razón social: %(name)s", name=taxpayer.get("razonSocial")),
            self.env._("Ambiente: %(env)s", env=environment),
            self.env._(
                "Listo para emitir: %(ready)s",
                ready=self.env._("Sí") if ready else self.env._("No"),
            ),
            *warnings,
        ]
        ok = ready and not warnings
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Conexión con SIFENDE")
                if ok
                else self.env._("Conexión con SIFENDE: revise la configuración"),
                "message": " ".join(
                    line if line.endswith(".") else f"{line}." for line in lines
                ),
                "type": "success" if ok else "warning",
                "sticky": not ok,
                "next": SOFT_RELOAD,
            },
        }

    def _sifende_config_warnings(self, taxpayer):
        warnings = []
        # el timbrado de Sandbox es sintético: no se compara con el de Odoo
        remote_stamp = (
            None
            if taxpayer.get("ambiente") == "SANDBOX"
            else (taxpayer.get("timbrado") or {}).get("numero")
        )
        points = {}
        for est in taxpayer.get("establecimientos") or []:
            for point in est.get("puntosExpedicion") or []:
                points[(est["numeroEstablecimiento"], point["puntoExpedicion"])] = (
                    est.get("activo") is not False and point.get("activo") is not False
                )
        authorizations = (
            self.env["account.authorization"]
            .sudo()
            .search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("date_to", ">=", fields.Date.context_today(self)),
                ]
            )
        )
        for auth in authorizations:
            if (
                remote_stamp is not None
                and str(remote_stamp) != (auth.name or "").strip()
            ):
                warnings.append(
                    self.env._(
                        "El timbrado %(odoo)s de Odoo no coincide con el de SIFENDE "
                        "(%(remote)s).",
                        odoo=auth.name,
                        remote=remote_stamp,
                    )
                )
            try:
                key = (int(auth.establishment), int(auth.expedition_point))
            except (TypeError, ValueError):
                continue
            if key in points and not points[key]:
                warnings.append(
                    self.env._(
                        "El establecimiento %(est)s / punto %(point)s del timbrado "
                        "%(stamp)s está inactivo en SIFENDE: actívelo en el panel de "
                        "Sifende.",
                        est=auth.establishment,
                        point=auth.expedition_point,
                        stamp=auth.name,
                    )
                )
            elif points and key not in points:
                warnings.append(
                    self.env._(
                        "El establecimiento %(est)s / punto %(point)s del timbrado "
                        "%(stamp)s "
                        "no existe en SIFENDE.",
                        est=auth.establishment,
                        point=auth.expedition_point,
                        stamp=auth.name,
                    )
                )
        return list(dict.fromkeys(warnings))

    def _sifende_no_preview_message(self):
        return self.env._(
            "SIFENDE no genera una vista previa sin emitir el documento. "
            "Use «Enviar a EDI» para emitirlo."
        )

    def _sifende_enum_name(self, category, code):
        for value in self._sifende_client().enums().get(category) or []:
            if value.get("val") is not None and int(value["val"]) == int(code):
                return value["name"]
        return None

    def _sifende_base_url(self):
        return (self.sudo().sifende_base_url or DEFAULT_BASE_URL).rstrip("/")

    def _sifende_client(self):
        self.ensure_one()
        return SifendeClient(
            self.env,
            self._sifende_base_url(),
            self.sudo().sifende_api_key,
            self.timeout,
        )
