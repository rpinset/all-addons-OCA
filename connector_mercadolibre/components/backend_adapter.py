# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

import requests

from odoo.addons.component.core import Component
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

_logger = logging.getLogger(__name__)

API_URL = "https://api.mercadolibre.com"


class MercadoLibreAPIError(FailedJobError):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code


# pylint: disable=method-required-super
class MercadoLibreAdapter(Component):
    _name = "mercadolibre.adapter"
    _inherit = ["mercadolibre.backend.component", "base.backend.adapter.crud"]
    _usage = "backend.adapter"

    def _url(self, path):
        if path.startswith(("https://", "http://")):
            return path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{API_URL}{path}"

    def _send(self, method, path, params=None, json=None, data=None, oauth=False):
        headers = {"Accept": "application/json"}
        if not oauth:
            token = self.backend_record.access_token or ""
            headers["Authorization"] = f"Bearer {token}"
        url = self._url(path)
        _logger.info(
            "Mercado Libre %s %s backend %s",
            method,
            path,
            self.backend_record.id,
        )
        transport = self.env.context.get("mercadolibre_transport")
        if transport:
            return transport(
                method,
                url,
                params=params,
                json=json,
                data=data,
                headers=headers,
                timeout=30,
            )
        return requests.request(
            method,
            url,
            params=params,
            json=json,
            data=data,
            headers=headers,
            timeout=30,
        )

    def _safe_message(self, response, path):
        detail = response.reason or "error"
        body = self._json_body(response)
        if isinstance(body, dict):
            error = body.get("error")
            message = body.get("message")
            if message and error and str(error) not in str(message):
                detail = f"{error}: {message}"
            else:
                detail = message or error or detail
        return f"Mercado Libre HTTP {response.status_code} on {path}: {detail}"

    def _json_body(self, response):
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def _raise_for_status(self, response, path):
        status = response.status_code
        if 200 <= status < 300:
            return
        message = self._safe_message(response, path)
        if status == 429 or status >= 500:
            seconds = 60
            retry_after = response.headers.get("Retry-After")
            if retry_after and str(retry_after).isdigit():
                seconds = int(retry_after)
            raise RetryableJobError(message, seconds=seconds)
        error_code = None
        body = self._json_body(response)
        if isinstance(body, dict):
            error_code = body.get("error")
        raise MercadoLibreAPIError(message, error_code=error_code)

    def _request(
        self,
        method,
        path,
        params=None,
        json=None,
        data=None,
        oauth=False,
        allow_refresh=True,
    ):
        response = self._send(
            method, path, params=params, json=json, data=data, oauth=oauth
        )
        if response.status_code == 401 and allow_refresh and not oauth:
            self.backend_record._job_refresh_token()
            response = self._send(
                method,
                path,
                params=params,
                json=json,
                data=data,
                oauth=oauth,
            )
        self._raise_for_status(response, path)
        body = self._json_body(response)
        if isinstance(body, (dict, list)):
            return body
        return {}

    def search(
        self,
        path,
        params=None,
        offset=None,
        limit=None,
        search_type=None,
        scroll_id=None,
    ):
        query = dict(params or {})
        if offset is not None:
            query["offset"] = offset
        if limit is not None:
            query["limit"] = limit
        if search_type:
            query["search_type"] = search_type
        if scroll_id:
            query["scroll_id"] = scroll_id
        return self._request("GET", path, params=query)

    def read(self, path, params=None):
        return self._request("GET", path, params=params)

    def search_read(self, path, **kwargs):
        return self.search(path, **kwargs)

    def create(self, path, values):
        return self._request("POST", path, json=values)

    def write(self, path, values):
        return self._request("PUT", path, json=values)

    def read_multi(self, external_ids):
        joined = ",".join(str(external_id) for external_id in external_ids)
        return self._request("GET", "/items", params={"ids": joined})

    def exchange_authorization_code(self, code):
        backend = self.backend_record
        return self._request(
            "POST",
            "/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": backend.client_id,
                "client_secret": backend.client_secret,
                "code": code,
                "redirect_uri": backend.redirect_uri,
                "code_verifier": backend.code_verifier,
            },
            oauth=True,
        )

    def refresh_access_token(self, refresh_token):
        backend = self.backend_record
        return self._request(
            "POST",
            "/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": backend.client_id,
                "client_secret": backend.client_secret,
                "refresh_token": refresh_token,
            },
            oauth=True,
        )
