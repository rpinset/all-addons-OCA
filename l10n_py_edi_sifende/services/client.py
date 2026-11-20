# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import json
import time
from dataclasses import dataclass, field
from urllib.parse import urlsplit

import requests
from requests.structures import CaseInsensitiveDict

from odoo.exceptions import UserError

API_PREFIX = "/api/v1"
USER_AGENT = "odoo-l10n_py_edi_sifende/18.0"
LOCAL_HOSTS = ("localhost", "127.0.0.1", "0.0.0.0", "::1")

ENUM_CACHE_TTL = 24 * 3600
_ENUM_CACHE = {}

RETRY_BACKOFF = (1, 2)
RETRY_AFTER_CAP = 10
TRANSIENT_STATUS = (429, 500, 502, 503, 504)
TRANSIENT_SLUGS = ("idempotency-in-progress", "idempotency-upstream-unknown")


class SifendeTransportError(Exception):
    """Timeout o conexión caída: la solicitud pudo no haber llegado."""


@dataclass
class SifendeResponse:
    status_code: int
    headers: dict = field(default_factory=CaseInsensitiveDict)
    body: object = None
    content: bytes = b""

    @property
    def ok(self):
        return 200 <= self.status_code < 300

    @property
    def slug(self):
        problem_type = self.body.get("type") if isinstance(self.body, dict) else None
        return problem_type.rstrip("/").rsplit("/", 1)[-1] if problem_type else None

    @property
    def detail(self):
        if not isinstance(self.body, dict):
            return None
        return (
            self.body.get("detail") or self.body.get("title") or self.body.get("error")
        )

    @property
    def field_errors(self):
        errors = self.body.get("errores") if isinstance(self.body, dict) else None
        return errors if isinstance(errors, dict) else {}

    @property
    def retry_after(self):
        try:
            return int(self.headers.get("Retry-After"))
        except (TypeError, ValueError):
            return None

    def failure_message(self, env):
        if self.status_code == 401:
            return env._(
                "SIFENDE rechazó la API key (401). Verifique que sea válida y no "
                "esté vencida."
            )
        parts = [self.detail or env._("Error HTTP %(status)s", status=self.status_code)]
        parts.extend(
            f"{name}: {message}" for name, message in self.field_errors.items()
        )
        return "\n".join(parts)


def is_secure_url(url):
    parts = urlsplit(url or "")
    host = parts.hostname or ""
    if not host:
        return False
    return parts.scheme == "https" or (parts.scheme == "http" and host in LOCAL_HOSTS)


def insecure_url_message(env):
    return env._(
        "La URL de Sifende debe usar HTTPS; HTTP solo se admite para localhost."
    )


def mask_key(api_key):
    if not api_key:
        return ""
    parts = api_key.split("_")
    prefix = "_".join(parts[:2]) + "_" if len(parts) > 2 else ""
    return f"{prefix}****"


def clear_enum_cache():
    _ENUM_CACHE.clear()


class SifendeClient:
    def __init__(self, env, base_url, api_key, timeout):
        self.env = env
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout or 30

    def request(
        self,
        method,
        path,
        *,
        operation,
        json_body=None,
        params=None,
        idempotency_key=None,
        retries=0,
        document=None,
        cdc=None,
        binary=False,
        authenticated=True,
        log=True,
    ):
        if authenticated and not self.api_key:
            raise UserError(
                self.env._(
                    "Configure la API key de Sifende en el conector EDI de la empresa."
                )
            )
        url = f"{self.base_url}{API_PREFIX}{path}"
        if authenticated and not is_secure_url(url):
            raise UserError(insecure_url_message(self.env))
        headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
        if authenticated:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        if binary:
            headers["Accept"] = "*/*"

        started = time.monotonic()
        attempt = 0
        transport_error = None
        response = None
        while True:
            transport_error = response = None
            try:
                raw = requests.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json_body,
                    timeout=self.timeout,
                )
                response = self._parse(raw, binary)
            except (requests.Timeout, requests.ConnectionError) as e:
                transport_error = e
            if attempt >= retries or not self._should_retry(response, transport_error):
                break
            time.sleep(self._backoff(attempt, response))
            attempt += 1

        # log puede ser una función que decide a partir de la respuesta; una
        # llamada fallida se registra siempre
        if callable(log):
            log = transport_error is not None or not response.ok or log(response)
        if log:
            self._log(
                operation,
                method,
                url,
                json_body,
                response,
                transport_error,
                started,
                attempt,
                document,
                cdc,
                headers,
            )
        if transport_error is not None:
            raise SifendeTransportError(self._transport_message(transport_error))
        return response

    def enums(self):
        cached = _ENUM_CACHE.get(self.base_url)
        if cached and cached[0] > time.monotonic():
            return cached[1]
        try:
            response = self.request(
                "GET",
                "/public/enums",
                operation="validate",
                authenticated=False,
                log=False,
            )
        except SifendeTransportError as e:
            raise UserError(
                self.env._(
                    "No se pudo obtener el catálogo de SIFENDE: %(error)s", error=e
                )
            ) from e
        if not (response.ok and isinstance(response.body, dict)):
            raise UserError(response.failure_message(self.env))
        _ENUM_CACHE[self.base_url] = (time.monotonic() + ENUM_CACHE_TTL, response.body)
        return response.body

    @staticmethod
    def _should_retry(response, transport_error):
        if transport_error is not None:
            return True
        return (
            response.status_code in TRANSIENT_STATUS or response.slug in TRANSIENT_SLUGS
        )

    @staticmethod
    def _backoff(attempt, response):
        if response is not None and response.retry_after:
            return min(response.retry_after, RETRY_AFTER_CAP)
        return RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]

    @staticmethod
    def _parse(raw, binary):
        headers = CaseInsensitiveDict(raw.headers or {})
        content = raw.content or b""
        body = None
        content_type = (headers.get("Content-Type") or "").lower()
        if "json" in content_type or not binary:
            try:
                body = raw.json()
            except ValueError:
                body = None
        return SifendeResponse(
            raw.status_code, headers, body, content if binary else b""
        )

    def _transport_message(self, error):
        if isinstance(error, requests.Timeout):
            return self.env._("tiempo de espera agotado")
        return self.env._("conexión rechazada o interrumpida")

    @staticmethod
    def _redact(body):
        if isinstance(body, dict) and body.get("secreto"):
            return {**body, "secreto": "whsec_****"}
        return body

    @staticmethod
    def _body_cdc(response):
        body = response.body if response is not None else None
        return body.get("cdc") if isinstance(body, dict) else None

    def _log(
        self,
        operation,
        method,
        url,
        json_body,
        response,
        transport_error,
        started,
        attempt,
        document,
        cdc,
        headers,
    ):
        logged_headers = {
            name: (
                f"Bearer {mask_key(self.api_key)}" if name == "Authorization" else value
            )
            for name, value in headers.items()
        }
        failed = transport_error is not None or (
            response is not None and not response.ok
        )
        if response is not None and response.body is not None:
            response_data = self._redact(response.body)
        elif response is not None and response.content:
            response_data = f"<{len(response.content)} bytes>"
        else:
            response_data = None
        error_message = None
        if failed:
            error_message = (
                self._transport_message(transport_error)
                if transport_error is not None
                else response.failure_message(self.env)
            )
        self.env["l10n_py.edi.log"].log_operation(
            operation_type=operation,
            provider="sifende",
            document=document or None,
            request_data=json_body,
            response_data=response_data,
            execution_time=(time.monotonic() - started) * 1000,
            success=not failed,
            error_message=error_message,
            endpoint=url,
            method=method,
            request_headers=json.dumps(logged_headers, ensure_ascii=False),
            status_code=response.status_code if response is not None else 0,
            retry_count=attempt,
            cdc=cdc
            or self._body_cdc(response)
            or (document.l10n_py_cdc if document else False),
        )
