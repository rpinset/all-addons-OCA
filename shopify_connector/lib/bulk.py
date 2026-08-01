"""Shopify GraphQL bulk-operation runner."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

import requests

from .product import ShopifyProductPayloadError, parse_jsonl
from .queries import BULK_OPERATION_POLL, BULK_OPERATION_RUN


class ShopifyBulkError(Exception):
    """Raised when a Shopify bulk operation or result download fails."""


class ShopifyBulkRunner:
    """Submit, poll, and download a Shopify GraphQL bulk query."""

    PENDING_STATUSES = {"CREATED", "RUNNING", "CANCELING"}

    def __init__(
        self,
        client: Any,
        *,
        poll_interval: float = 2.0,
        sleep: Callable[[float], None] = time.sleep,
        download_session: Any | None = None,
        timeout: float = 60.0,
        max_polls: int | None = None,
    ) -> None:
        self.client = client
        self.poll_interval = poll_interval
        self.sleep = sleep
        self.download_session = download_session or requests.Session()
        self.timeout = timeout
        self.max_polls = max_polls

    def run(self, query: str) -> list[dict[str, Any]]:
        operation_id = self.submit(query)
        result_url = self.poll(operation_id)
        if result_url is None:
            return []
        return self.download(result_url)

    def submit(self, query: str) -> str:
        data = self.client.execute(BULK_OPERATION_RUN, {"query": query})
        operation = data.get("bulkOperationRunQuery", {}).get("bulkOperation")
        if not isinstance(operation, dict) or not operation.get("id"):
            raise ShopifyBulkError("Shopify did not create the bulk operation.")
        return str(operation["id"])

    def poll(self, operation_id: str) -> str | None:
        poll_count = 0
        while True:
            if self.max_polls is not None and poll_count >= self.max_polls:
                raise ShopifyBulkError("Bulk operation polling limit was reached.")
            data = self.client.execute(BULK_OPERATION_POLL, {"id": operation_id})
            operation = data.get("bulkOperation")
            if not isinstance(operation, dict):
                raise ShopifyBulkError("Shopify returned no bulk operation.")
            if operation.get("id") != operation_id:
                raise ShopifyBulkError("Shopify returned a different bulk operation.")
            status = operation.get("status")
            if status == "COMPLETED":
                if not operation.get("url"):
                    return None
                return str(operation["url"])
            if status not in self.PENDING_STATUSES:
                error_code = operation.get("errorCode") or "unknown error"
                raise ShopifyBulkError(
                    f"Bulk operation ended in {status}: {error_code}."
                )
            poll_count += 1
            self.sleep(self.poll_interval)

    def download(self, result_url: str) -> list[dict[str, Any]]:
        try:
            response = self.download_session.get(
                result_url, timeout=self.timeout, stream=True
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ShopifyBulkError("Could not download the bulk result.") from exc

        try:
            return parse_jsonl(response.iter_lines())
        except ShopifyProductPayloadError as exc:
            raise ShopifyBulkError("Bulk result contained invalid JSONL.") from exc
