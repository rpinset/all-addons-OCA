"""Pure-Python helpers for inventory synchronization."""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

VALID_QUANTITY_BASES = {"free_qty", "qty_available"}


def quantity_for_basis(
    free_qty: Any,
    qty_available: Any,
    basis: str = "free_qty",
) -> int:
    """Select and integerize the configured Odoo stock quantity."""

    if basis not in VALID_QUANTITY_BASES:
        raise ValueError(f"Unsupported inventory quantity basis: {basis}")
    value = free_qty if basis == "free_qty" else qty_available
    return int(Decimal(str(value or 0)).quantize(Decimal("1"), ROUND_HALF_UP))


def apply_negative_policy(quantity: int, allow_negative: bool) -> tuple[int, bool]:
    """Return the export quantity and whether it had to be clamped."""

    normalized = int(quantity)
    if normalized < 0 and not allow_negative:
        return 0, True
    return normalized, False


def diff_inventory_levels(
    desired: Mapping[Hashable, int],
    remote: Mapping[Hashable, int],
) -> list[dict[str, Any]]:
    """Return deterministic corrections for levels present on both sides."""

    corrections = []
    for key in sorted(desired.keys() & remote.keys(), key=str):
        wanted = int(desired[key])
        current = int(remote[key])
        if wanted != current:
            corrections.append(
                {
                    "key": key,
                    "desired": wanted,
                    "remote": current,
                    "delta": wanted - current,
                }
            )
    return corrections


def build_inventory_set_payload(
    inventory_item_id: str,
    location_id: str,
    quantity: int,
    compare_quantity: int,
    *,
    reference_document_uri: str | None = None,
) -> dict[str, Any]:
    """Build an ``InventorySetQuantitiesInput`` using compare-and-set."""

    payload: dict[str, Any] = {
        "name": "available",
        "reason": "correction",
        "quantities": [
            {
                "inventoryItemId": inventory_item_id,
                "locationId": location_id,
                "quantity": int(quantity),
                "compareQuantity": int(compare_quantity),
            }
        ],
    }
    if reference_document_uri:
        payload["referenceDocumentUri"] = reference_document_uri
    return payload


def should_ignore_echo(
    incoming_quantity: int,
    last_pushed_quantity: int | None,
    last_pushed_at: datetime | str | None,
    *,
    now: datetime | None = None,
    window_seconds: int = 300,
) -> bool:
    """Whether a Shopify webhook is a recent acknowledgement of our push."""

    if last_pushed_quantity is None or not last_pushed_at:
        return False
    pushed_at = _as_utc(last_pushed_at)
    current = _as_utc(now or datetime.now(timezone.utc))
    age = current - pushed_at
    return int(incoming_quantity) == int(last_pushed_quantity) and timedelta(
        0
    ) <= age <= timedelta(seconds=max(0, window_seconds))


def available_quantity(level: Mapping[str, Any] | None) -> int | None:
    """Extract the Shopify ``available`` quantity from an inventory level."""

    if not level:
        return None
    for quantity in level.get("quantities") or []:
        if (
            isinstance(quantity, Mapping)
            and quantity.get("name") == "available"
            and quantity.get("quantity") is not None
        ):
            return int(quantity["quantity"])
    return None


def normalize_inventory_bulk_levels(
    records: list[dict[str, Any]],
) -> dict[tuple[str, str], int]:
    """Normalize bulk InventoryItem/InventoryLevel JSONL rows."""

    inventory_items = {
        str(row["id"])
        for row in records
        if str(row.get("id") or "").startswith("gid://shopify/InventoryItem/")
    }
    levels: dict[tuple[str, str], int] = {}
    for row in records:
        item_id = str(row.get("__parentId") or "")
        location = row.get("location") or {}
        location_id = str(location.get("id") or "")
        if item_id not in inventory_items or not location_id:
            continue
        quantity = available_quantity(row)
        if quantity is not None:
            levels[(item_id, location_id)] = quantity
    return levels


def is_stale_compare_error(error: Exception | str) -> bool:
    """Recognize Shopify's compare-and-set mismatch user errors."""

    message = str(error).casefold()
    return "compare" in message and (
        "quantity" in message or "persisted" in message or "stale" in message
    )


def _as_utc(value: datetime | str) -> datetime:
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
