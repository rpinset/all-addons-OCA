"""Pure-Python Shopify GraphQL Admin API client."""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from typing import Any

import requests

API_VERSION = "2026-01"
OAUTH_TOKEN_PATH = "/admin/oauth/access_token"


class ShopifyError(Exception):
    """Base error for Shopify API failures."""


class ShopifyThrottled(ShopifyError):
    """Raised when Shopify keeps throttling after all retries."""


class ShopifyUserError(ShopifyError):
    """Raised for invalid requests and GraphQL user errors."""


class ShopifyServerError(ShopifyError):
    """Raised for transport or Shopify server failures."""


class ShopifyClient:
    """Small GraphQL client with Shopify-aware throttling and retries."""

    def __init__(
        self,
        shop_url: str,
        access_token: str,
        *,
        api_version: str = API_VERSION,
        session: Any | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        max_backoff: float = 30.0,
        timeout: float = 30.0,
    ) -> None:
        self.shop_url = self._normalise_shop_url(shop_url)
        self.api_version = api_version
        self.endpoint = (
            f"https://{self.shop_url}/admin/api/{self.api_version}/graphql.json"
        )
        self.session = session or requests.Session()
        self.sleep = sleep
        self.clock = clock
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff
        self.timeout = timeout
        self._headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        }
        self.last_request_at: float | None = None

    @staticmethod
    def _normalise_shop_url(shop_url: str) -> str:
        value = (shop_url or "").strip().lower()
        for prefix in ("https://", "http://"):
            if value.startswith(prefix):
                value = value[len(prefix) :]
        return value.rstrip("/")

    def execute(
        self, query: str, variables: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """Execute one GraphQL operation and return its ``data`` mapping."""

        payload = {"query": query, "variables": dict(variables or {})}
        for attempt in range(self.max_retries + 1):
            self.last_request_at = self.clock()
            try:
                response = self.session.post(
                    self.endpoint,
                    headers=self._headers,
                    json=payload,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                if attempt >= self.max_retries:
                    raise ShopifyServerError(
                        "Shopify could not be reached after retries."
                    ) from exc
                self._backoff(attempt)
                continue

            if response.status_code == 429:
                if attempt >= self.max_retries:
                    raise ShopifyThrottled(
                        "Shopify throttled the request after retries."
                    )
                self._backoff(attempt)
                continue
            if response.status_code >= 500:
                if attempt >= self.max_retries:
                    raise ShopifyServerError(
                        f"Shopify returned HTTP {response.status_code} after retries."
                    )
                self._backoff(attempt)
                continue
            if response.status_code >= 400:
                raise ShopifyUserError(
                    f"Shopify rejected the request with HTTP {response.status_code}."
                )

            try:
                body = response.json()
            except (TypeError, ValueError) as exc:
                raise ShopifyServerError(
                    "Shopify returned a non-JSON response."
                ) from exc
            if not isinstance(body, dict):
                raise ShopifyServerError(
                    "Shopify returned an invalid GraphQL response."
                )

            self._apply_cost_throttle(body.get("extensions"))
            errors = body.get("errors") or []
            if self._is_throttled(errors):
                if attempt >= self.max_retries:
                    raise ShopifyThrottled(
                        "Shopify throttled the request after retries."
                    )
                self._backoff(attempt)
                continue
            if errors:
                raise ShopifyUserError(self._format_graphql_errors(errors))

            data = body.get("data")
            if not isinstance(data, dict):
                raise ShopifyServerError(
                    "Shopify response did not contain GraphQL data."
                )
            user_errors = self._collect_user_errors(data)
            if user_errors:
                raise ShopifyUserError("; ".join(user_errors))
            return data

        raise ShopifyServerError("Shopify request retry loop ended unexpectedly.")

    def _backoff(self, attempt: int) -> None:
        delay = min(self.max_backoff, self.backoff_factor * (2**attempt))
        self.sleep(delay)

    def _apply_cost_throttle(self, extensions: Any) -> None:
        if not isinstance(extensions, dict):
            return
        cost = extensions.get("cost")
        if not isinstance(cost, dict):
            return
        requested = cost.get("requestedQueryCost")
        throttle_status = cost.get("throttleStatus")
        if not isinstance(throttle_status, dict):
            return
        available = throttle_status.get("currentlyAvailable")
        restore_rate = throttle_status.get("restoreRate")
        if not all(
            isinstance(value, (int, float))
            for value in (requested, available, restore_rate)
        ):
            return
        if available < requested:
            if restore_rate <= 0:
                wait = self.max_backoff
            else:
                wait = (requested - available) / restore_rate
            self.sleep(min(self.max_backoff, max(0.0, wait)))

    @staticmethod
    def _is_throttled(errors: Any) -> bool:
        if not isinstance(errors, list):
            return False
        return any(
            isinstance(error, dict)
            and isinstance(error.get("extensions"), dict)
            and error["extensions"].get("code") == "THROTTLED"
            for error in errors
        )

    @staticmethod
    def _format_graphql_errors(errors: Any) -> str:
        if not isinstance(errors, list):
            return "Shopify returned a GraphQL error."
        messages = [
            str(error.get("message", "Unknown GraphQL error"))
            for error in errors
            if isinstance(error, dict)
        ]
        return "; ".join(messages) or "Shopify returned a GraphQL error."

    @classmethod
    def _collect_user_errors(cls, value: Any) -> list[str]:
        messages: list[str] = []
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "userErrors" and isinstance(child, list):
                    messages.extend(
                        str(error.get("message", "Unknown Shopify user error"))
                        for error in child
                        if isinstance(error, dict)
                    )
                else:
                    messages.extend(cls._collect_user_errors(child))
        elif isinstance(value, list):
            for child in value:
                messages.extend(cls._collect_user_errors(child))
        return messages


def request_access_token(
    shop_url: str,
    client_id: str,
    client_secret: str,
    *,
    session: Any | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Exchange Shopify app client credentials for an Admin API access token.

    Return the ``access_token`` and its ``expires_in`` lifetime in seconds.
    Errors never repeat credentials nor Shopify response bodies.
    """

    shop = ShopifyClient._normalise_shop_url(shop_url)
    if not shop:
        raise ShopifyUserError("A shop domain is required to request an access token.")
    if not client_id or not client_secret:
        raise ShopifyUserError("The Shopify app client credentials are incomplete.")
    http_session = session or requests.Session()
    try:
        response = http_session.post(
            f"https://{shop}{OAUTH_TOKEN_PATH}",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise ShopifyServerError(
            "Shopify could not be reached to request an access token."
        ) from exc

    if response.status_code >= 500:
        raise ShopifyServerError(
            f"Shopify returned HTTP {response.status_code} "
            "for the access token request."
        )
    if response.status_code >= 400:
        raise ShopifyUserError(
            f"Shopify rejected the access token request with HTTP "
            f"{response.status_code}."
        )
    try:
        body = response.json()
    except (TypeError, ValueError) as exc:
        raise ShopifyServerError(
            "Shopify returned a non-JSON access token response."
        ) from exc
    if not isinstance(body, dict):
        raise ShopifyServerError("Shopify returned an invalid access token response.")
    access_token = body.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise ShopifyServerError("Shopify did not return an access token.")
    return {
        "access_token": access_token,
        "expires_in": _access_token_lifetime(body.get("expires_in")),
    }


def _access_token_lifetime(value: Any) -> int:
    """Return ``expires_in`` as a strictly positive number of seconds."""

    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ShopifyServerError("Shopify returned an invalid access token lifetime.")
    try:
        lifetime = int(value)
    except ValueError as exc:
        raise ShopifyServerError(
            "Shopify returned an invalid access token lifetime."
        ) from exc
    if lifetime <= 0:
        raise ShopifyServerError("Shopify returned an invalid access token lifetime.")
    return lifetime
