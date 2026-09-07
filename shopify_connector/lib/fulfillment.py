"""Odoo-free Shopify fulfillment allocation and tracking helpers."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from typing import Any


class FulfillmentAllocationError(ValueError):
    """Raised when a delivery cannot be mapped to Shopify fulfillment lines."""


def _quantity(value: Any) -> Decimal:
    try:
        quantity = Decimal(str(value or 0))
    except (InvalidOperation, ValueError) as exc:
        raise FulfillmentAllocationError(
            f"Invalid fulfillment quantity: {value!r}."
        ) from exc
    if quantity < 0:
        raise FulfillmentAllocationError(
            f"Fulfillment quantities cannot be negative: {value!r}."
        )
    return quantity


def _shopify_quantity(value: Decimal) -> int:
    integral = value.to_integral_value()
    if value != integral:
        raise FulfillmentAllocationError(
            f"Shopify fulfillment quantities must be whole units, got {value}."
        )
    return int(integral)


def allocate_fulfillment_lines(  # noqa: C901
    moves: Iterable[dict[str, Any]],
    fulfillment_orders: Iterable[dict[str, Any]],
    *,
    target_location_id: str,
) -> dict[str, Any]:
    """Allocate delivered moves against Shopify's remaining quantities.

    Matching-location fulfillment orders are consumed first. A fulfillment
    order at another location is only eligible when Shopify reports ``MOVE`` as
    a supported action. Delivered quantities beyond Shopify's remaining amount
    are clamped and returned as warnings.
    """
    orders = [dict(item) for item in fulfillment_orders]
    remaining: dict[str, Decimal] = {}
    candidates_by_line: dict[str, list[dict[str, Any]]] = defaultdict(list)
    order_by_id = {}
    for order in orders:
        order_id = str(order.get("id") or "")
        if not order_id:
            continue
        order_by_id[order_id] = order
        if order.get("held") or str(order.get("status") or "").upper() in {
            "CLOSED",
            "CANCELLED",
            "INCOMPLETE",
        }:
            continue
        for line in order.get("line_items") or []:
            line_id = str(line.get("id") or "")
            order_line_id = str(line.get("line_id") or "")
            if not line_id or not order_line_id:
                continue
            quantity = _quantity(line.get("remaining_quantity"))
            if quantity <= 0:
                continue
            key = f"{order_id}:{line_id}"
            remaining[key] = quantity
            candidates_by_line[order_line_id].append(
                {
                    "order": order,
                    "line": line,
                    "remaining_key": key,
                }
            )

    allocations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    warnings = []
    move_orders = set()
    for move in moves:
        move_name = str(move.get("name") or move.get("move_id") or "delivery move")
        order_line_id = str(move.get("line_id") or "")
        if not order_line_id:
            raise FulfillmentAllocationError(
                f"{move_name} has no Shopify order-line binding."
            )
        delivered = _quantity(move.get("quantity"))
        if delivered <= 0:
            continue
        candidates = list(candidates_by_line.get(order_line_id) or [])
        if not candidates:
            raise FulfillmentAllocationError(
                f"{move_name} has no remaining Shopify fulfillment-order line."
            )
        candidates.sort(
            key=lambda candidate: (
                candidate["order"].get("location_id") != target_location_id,
                str(candidate["order"].get("id") or ""),
            )
        )
        requested = delivered
        for candidate in candidates:
            if delivered <= 0:
                break
            order = candidate["order"]
            available = remaining[candidate["remaining_key"]]
            if available <= 0:
                continue
            location_id = str(order.get("location_id") or "")
            if location_id != target_location_id:
                supported = {
                    str(action).upper()
                    for action in (order.get("supported_actions") or [])
                }
                if "MOVE" not in supported:
                    continue
                move_orders.add(str(order["id"]))
            allocated = min(delivered, available)
            allocations[str(order["id"])].append(
                {
                    "id": str(candidate["line"]["id"]),
                    "quantity": _shopify_quantity(allocated),
                    "line_id": order_line_id,
                    "move_id": move.get("move_id"),
                }
            )
            remaining[candidate["remaining_key"]] -= allocated
            delivered -= allocated
        if delivered > 0:
            blocked_locations = sorted(
                {
                    str(candidate["order"].get("location_id") or "")
                    for candidate in candidates
                    if remaining[candidate["remaining_key"]] > 0
                    and str(candidate["order"].get("location_id") or "")
                    != target_location_id
                    and "MOVE"
                    not in {
                        str(action).upper()
                        for action in (
                            candidate["order"].get("supported_actions") or []
                        )
                    }
                }
            )
            if blocked_locations:
                raise FulfillmentAllocationError(
                    f"{move_name} cannot be fulfilled from Shopify location "
                    f"{target_location_id}; remaining quantity is assigned to "
                    f"{', '.join(blocked_locations)} and MOVE is unavailable."
                )
            fulfilled = requested - delivered
            if fulfilled <= 0:
                locations = sorted(
                    {
                        str(candidate["order"].get("location_id") or "")
                        for candidate in candidates
                    }
                )
                raise FulfillmentAllocationError(
                    f"{move_name} cannot be fulfilled from Shopify location "
                    f"{target_location_id}; available locations: "
                    f"{', '.join(locations) or 'none'}."
                )
            warnings.append(
                f"{move_name}: delivered {_shopify_quantity(requested)}, but "
                f"Shopify only allows {_shopify_quantity(fulfilled)}; clamped "
                "to Shopify's remaining quantity."
            )

    groups = []
    for order_id, lines in allocations.items():
        order = order_by_id[order_id]
        groups.append(
            {
                "fulfillment_order_id": order_id,
                "location_id": str(order.get("location_id") or ""),
                "move_required": order_id in move_orders,
                "line_items": [
                    {"id": line["id"], "quantity": line["quantity"]} for line in lines
                ],
            }
        )
    groups.sort(key=lambda group: group["fulfillment_order_id"])
    return {
        "groups": groups,
        "move_fulfillment_order_ids": sorted(move_orders),
        "warnings": warnings,
    }


def build_tracking_payload(
    number: Any = None,
    company: Any = None,
    url: Any = None,
) -> dict[str, str]:
    """Build Shopify ``trackingInfo``, omitting blank values."""
    values = {
        "number": str(number or "").strip(),
        "company": str(company or "").strip(),
        "url": str(url or "").strip(),
    }
    return {key: value for key, value in values.items() if value}
