"""Pure Shopify order normalisation and exact money helpers."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Iterable
from decimal import ROUND_DOWN, Decimal, InvalidOperation
from typing import Any


class ShopifyOrderPayloadError(ValueError):
    """Raised when an order cannot be represented without guessing."""


def shopify_gid(resource: str, value: Any) -> str:
    """Return a stable GraphQL ID for REST or GraphQL payload values."""
    if value in (None, ""):
        return ""
    text = str(value)
    if text.startswith("gid://"):
        return text
    return f"gid://shopify/{resource}/{text}"


def decimal_amount(value: Any) -> Decimal:
    """Parse a Shopify decimal without ever passing through float arithmetic."""
    if isinstance(value, Decimal):
        return value
    if value in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ShopifyOrderPayloadError(
            f"Invalid Shopify money amount: {value!r}."
        ) from exc


def money_bag(value: Any, *, fallback_currency: str = "") -> dict[str, dict[str, str]]:
    """Normalise REST ``*_set`` and GraphQL ``MoneyBag`` values."""
    value = value or {}
    if isinstance(value, (str, int, float, Decimal)):
        money = {"amount": str(value), "currency": fallback_currency}
        return {"shop": dict(money), "presentment": dict(money)}
    shop = value.get("shopMoney") or value.get("shop_money") or value.get("shop") or {}
    presentment = (
        value.get("presentmentMoney")
        or value.get("presentment_money")
        or value.get("presentment")
        or shop
    )
    if "amount" in value and not shop:
        shop = value
        presentment = value

    def normalise_money(item: Any) -> dict[str, str]:
        item = item or {}
        return {
            "amount": format(decimal_amount(item.get("amount")), "f"),
            "currency": str(
                item.get("currencyCode")
                or item.get("currency_code")
                or item.get("currency")
                or fallback_currency
                or ""
            ).upper(),
        }

    return {"shop": normalise_money(shop), "presentment": normalise_money(presentment)}


def selected_money(
    value: dict[str, dict[str, str]], use_presentment: bool
) -> dict[str, str]:
    """Select the configured side of a normalised money bag."""
    return value["presentment" if use_presentment else "shop"]


def _nodes(value: Any) -> list[dict[str, Any]]:
    if not value:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("nodes"), list):
            return _nodes(value["nodes"])
        if isinstance(value.get("edges"), list):
            return _nodes(
                [edge.get("node") for edge in value["edges"] if isinstance(edge, dict)]
            )
    return []


def _money(
    payload: dict[str, Any],
    *names: str,
    fallback_currency: str = "",
) -> dict[str, dict[str, str]]:
    for name in names:
        if payload.get(name) is not None:
            return money_bag(payload[name], fallback_currency=fallback_currency)
    return money_bag("0", fallback_currency=fallback_currency)


def _tax_line(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    return {
        "title": str(payload.get("title") or ""),
        "rate": format(
            decimal_amount(payload.get("rate") or payload.get("ratePercentage")),
            "f",
        ),
        "country_code": str(
            payload.get("countryCode") or payload.get("country_code") or ""
        ).upper(),
        "price": _money(
            payload,
            "priceSet",
            "price_set",
            "price",
            fallback_currency=currency,
        ),
    }


def _discount_allocation(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    application = payload.get("discountApplication") or {}
    return {
        "amount": _money(
            payload,
            "allocatedAmountSet",
            "amountSet",
            "amount_set",
            "amount",
            fallback_currency=currency,
        ),
        "code": str(application.get("code") or payload.get("code") or ""),
        "title": str(application.get("title") or payload.get("title") or ""),
        "target_type": str(
            application.get("targetType")
            or application.get("target_type")
            or payload.get("target_type")
            or ""
        ).upper(),
    }


def _normalise_line(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    quantity = int(
        payload.get("currentQuantity")
        if payload.get("currentQuantity") is not None
        else payload.get("current_quantity")
        if payload.get("current_quantity") is not None
        else payload.get("quantity") or 0
    )
    original_quantity = int(payload.get("quantity") or quantity)
    unit = _money(
        payload,
        "originalUnitPriceSet",
        "original_unit_price_set",
        "priceSet",
        "price_set",
        "price",
        fallback_currency=currency,
    )
    all_discount_unit = payload.get(
        "discountedUnitPriceAfterAllDiscountsSet"
    ) or payload.get("discounted_unit_price_after_all_discounts_set")
    has_discounted_total = any(
        payload.get(name) is not None
        for name in (
            "discountedTotalSet",
            "discounted_total_set",
            "currentTotalSet",
        )
    )
    if all_discount_unit:
        normalized_unit = money_bag(all_discount_unit, fallback_currency=currency)
        discounted_total = {
            side: {
                "amount": format(
                    decimal_amount(normalized_unit[side]["amount"]) * quantity,
                    "f",
                ),
                "currency": normalized_unit[side]["currency"],
            }
            for side in ("shop", "presentment")
        }
    else:
        discounted_total = _money(
            payload,
            "discountedTotalSet",
            "discounted_total_set",
            "currentTotalSet",
            fallback_currency=currency,
        )
    if not all_discount_unit and not has_discounted_total:
        discount_total = _money(
            payload,
            "totalDiscountSet",
            "total_discount_set",
            "total_discount",
            fallback_currency=currency,
        )
        discounted_total = {}
        for side in ("shop", "presentment"):
            amount = decimal_amount(unit[side]["amount"]) * quantity - decimal_amount(
                discount_total[side]["amount"]
            )
            discounted_total[side] = {
                "amount": format(amount, "f"),
                "currency": unit[side]["currency"],
            }
    variant = payload.get("variant") or {}
    product = payload.get("product") or {}
    return {
        "id": shopify_gid(
            "LineItem",
            payload.get("id") or payload.get("admin_graphql_api_id"),
        ),
        "variant_id": shopify_gid(
            "ProductVariant",
            variant.get("id") or payload.get("variant_id"),
        ),
        "product_id": shopify_gid(
            "Product", product.get("id") or payload.get("product_id")
        ),
        "title": str(payload.get("name") or payload.get("title") or ""),
        "sku": str(payload.get("sku") or variant.get("sku") or ""),
        "quantity": quantity,
        "original_quantity": original_quantity,
        "refundable_quantity": int(
            payload.get("refundableQuantity")
            if payload.get("refundableQuantity") is not None
            else payload.get("refundable_quantity")
            if payload.get("refundable_quantity") is not None
            else quantity
        ),
        "gift_card": bool(
            payload.get("isGiftCard")
            or payload.get("gift_card")
            or product.get("isGiftCard")
        ),
        "unit_price": unit,
        "discounted_total": discounted_total,
        "discount_allocations": [
            _discount_allocation(item, currency)
            for item in _nodes(
                payload.get("discountAllocations")
                or payload.get("discount_allocations")
            )
        ],
        "tax_lines": [
            _tax_line(item, currency)
            for item in _nodes(payload.get("taxLines") or payload.get("tax_lines"))
        ],
    }


def _normalise_shipping(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    return {
        "id": shopify_gid(
            "ShippingLine",
            payload.get("id") or payload.get("admin_graphql_api_id"),
        ),
        "title": str(payload.get("title") or payload.get("code") or "Shipping"),
        "code": str(payload.get("code") or ""),
        "original_total": _money(
            payload,
            "originalPriceSet",
            "original_price_set",
            "priceSet",
            "price_set",
            "price",
            fallback_currency=currency,
        ),
        "discounted_total": _money(
            payload,
            "currentDiscountedPriceSet",
            "current_discounted_price_set",
            "discountedPriceSet",
            "discounted_price_set",
            "priceSet",
            "price_set",
            "price",
            fallback_currency=currency,
        ),
        "tax_lines": [
            _tax_line(item, currency)
            for item in _nodes(payload.get("taxLines") or payload.get("tax_lines"))
        ],
    }


def _normalise_transaction(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    return {
        "id": shopify_gid(
            "OrderTransaction",
            payload.get("id") or payload.get("admin_graphql_api_id"),
        ),
        "gateway": str(payload.get("gateway") or payload.get("formattedGateway") or ""),
        "kind": str(payload.get("kind") or "").upper(),
        "status": str(payload.get("status") or "").upper(),
        "amount": _money(
            payload,
            "amountSet",
            "amount_set",
            "amount",
            fallback_currency=currency,
        ),
        "processed_at": payload.get("processedAt") or payload.get("processed_at"),
    }


def _normalise_refund_line(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    line = payload.get("lineItem") or payload.get("line_item") or {}
    return {
        "id": shopify_gid(
            "RefundLineItem",
            payload.get("id") or payload.get("admin_graphql_api_id"),
        ),
        "line_id": shopify_gid(
            "LineItem",
            line.get("id") or payload.get("line_item_id"),
        ),
        "quantity": int(payload.get("quantity") or 0),
        "restock_type": str(
            payload.get("restockType") or payload.get("restock_type") or "NO_RESTOCK"
        ).upper(),
        "subtotal": _money(
            payload,
            "subtotalSet",
            "subtotal_set",
            "subtotal",
            fallback_currency=currency,
        ),
        "tax": _money(
            payload,
            "totalTaxSet",
            "total_tax_set",
            "total_tax",
            fallback_currency=currency,
        ),
    }


def _normalise_refund(payload: dict[str, Any], currency: str) -> dict[str, Any]:
    refund_lines = _nodes(
        payload.get("refundLineItems") or payload.get("refund_line_items")
    )
    transactions = _nodes(payload.get("transactions"))
    adjustments = _nodes(
        payload.get("orderAdjustments") or payload.get("order_adjustments")
    )
    shipping = _nodes(
        payload.get("refundShippingLines") or payload.get("refund_shipping_lines")
    )
    return {
        "id": shopify_gid(
            "Refund", payload.get("id") or payload.get("admin_graphql_api_id")
        ),
        "created_at": payload.get("createdAt") or payload.get("created_at"),
        "note": str(payload.get("note") or ""),
        "total": _money(
            payload,
            "totalRefundedSet",
            "total_refunded_set",
            fallback_currency=currency,
        ),
        "lines": [_normalise_refund_line(item, currency) for item in refund_lines],
        "shipping": [
            {
                "id": shopify_gid("RefundShippingLine", item.get("id")),
                "amount": _money(
                    item,
                    "subtotalAmountSet",
                    "subtotal_amount_set",
                    "amountSet",
                    "amount",
                    fallback_currency=currency,
                ),
            }
            for item in shipping
        ],
        "adjustments": [
            {
                "id": shopify_gid("OrderAdjustment", item.get("id")),
                "reason": str(item.get("reason") or ""),
                "amount": _money(
                    item,
                    "amountSet",
                    "amount_set",
                    "amount",
                    fallback_currency=currency,
                ),
                "tax": _money(
                    item,
                    "taxAmountSet",
                    "tax_amount_set",
                    "tax_amount",
                    fallback_currency=currency,
                ),
            }
            for item in adjustments
        ],
        "transactions": [
            _normalise_transaction(item, currency) for item in transactions
        ],
    }


def _normalise_return(payload: dict[str, Any]) -> dict[str, Any]:
    return_lines = []
    for item in _nodes(payload.get("returnLineItems")):
        fulfillment_line = item.get("fulfillmentLineItem") or {}
        return_lines.append(
            {
                "id": shopify_gid("ReturnLineItem", item.get("id")),
                "line_id": shopify_gid(
                    "LineItem",
                    (fulfillment_line.get("lineItem") or {}).get("id"),
                ),
                "quantity": int(item.get("quantity") or 0),
                "refundable_quantity": int(item.get("refundableQuantity") or 0),
                "refunded_quantity": int(item.get("refundedQuantity") or 0),
                "reason_note": str(item.get("returnReasonNote") or ""),
            }
        )
    exchange_lines = [
        {
            "id": shopify_gid("ExchangeLineItem", item.get("id")),
            "line_id": shopify_gid("LineItem", (item.get("lineItem") or {}).get("id")),
            "variant_id": shopify_gid("ProductVariant", item.get("variantId")),
            "quantity": int(item.get("quantity") or 0),
        }
        for item in _nodes(payload.get("exchangeLineItems"))
    ]
    return {
        "id": shopify_gid("Return", payload.get("id")),
        "name": str(payload.get("name") or ""),
        "status": str(payload.get("status") or "").upper(),
        "created_at": payload.get("createdAt"),
        "closed_at": payload.get("closedAt"),
        "total_quantity": int(payload.get("totalQuantity") or 0),
        "lines": return_lines,
        "exchange_lines": exchange_lines,
        "raw": payload,
    }


def _risk_level(payload: dict[str, Any]) -> str:
    summary = payload.get("risk") or {}
    assessments = _nodes(summary.get("assessments"))
    values = [
        str(item.get("riskLevel") or item.get("risk_level") or "").upper()
        for item in assessments
    ]
    if payload.get("risk_level"):
        values.append(str(payload["risk_level"]).upper())
    priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0, "UNKNOWN": 0}
    return max(values or ["UNKNOWN"], key=lambda value: priority.get(value, 0))


def normalize_order_payload(
    payload: dict[str, Any], *, is_draft: bool = False
) -> dict[str, Any]:
    """Normalise GraphQL orders, REST webhooks, and draft orders."""
    if not isinstance(payload, dict):
        raise ShopifyOrderPayloadError("Shopify order payload must be an object.")
    resource = "DraftOrder" if is_draft else "Order"
    identifier = shopify_gid(
        resource, payload.get("id") or payload.get("admin_graphql_api_id")
    )
    if not identifier:
        raise ShopifyOrderPayloadError("Shopify order payload has no ID.")
    currency = str(
        payload.get("currencyCode")
        or payload.get("currency")
        or payload.get("presentmentCurrencyCode")
        or payload.get("presentment_currency")
        or ""
    ).upper()
    source_name = str(
        payload.get("sourceName")
        or payload.get("source_name")
        or ("shopify_draft_order" if is_draft else "web")
    )
    source = (
        "draft"
        if is_draft or source_name == "shopify_draft_order"
        else "pos"
        if source_name == "pos"
        else "online"
    )
    retail_location = (
        payload.get("retailLocation") or payload.get("retail_location") or {}
    )
    cash_rounding = (
        payload.get("totalCashRoundingAdjustment")
        or payload.get("total_cash_rounding_adjustment")
        or {}
    )
    line_source = payload.get("lineItems") or payload.get("line_items")
    shipping_source = (
        [payload["shippingLine"]]
        if payload.get("shippingLine")
        else payload.get("shippingLines") or payload.get("shipping_lines")
    )
    discount_codes = payload.get("discountCodes") or payload.get("discount_codes") or []
    codes = [
        str(item.get("code") if isinstance(item, dict) else item)
        for item in discount_codes
        if item
    ]
    order = {
        "id": identifier,
        "name": str(payload.get("name") or ""),
        "number": str(payload.get("orderNumber") or payload.get("order_number") or ""),
        "created_at": payload.get("createdAt") or payload.get("created_at"),
        "updated_at": payload.get("updatedAt") or payload.get("updated_at"),
        "cancelled_at": payload.get("cancelledAt") or payload.get("cancelled_at"),
        "financial_status": str(
            payload.get("displayFinancialStatus")
            or payload.get("financial_status")
            or ("PENDING" if is_draft else "")
        ).upper(),
        "fulfillment_status": str(
            payload.get("displayFulfillmentStatus")
            or payload.get("fulfillment_status")
            or "UNFULFILLED"
        ).upper(),
        "source": source,
        "source_name": source_name,
        "source_identifier": str(
            payload.get("sourceIdentifier") or payload.get("source_identifier") or ""
        ),
        "retail_location_id": shopify_gid(
            "Location",
            retail_location.get("id") or payload.get("location_id"),
        ),
        "cash_rounding": {
            "payment": _money(
                cash_rounding,
                "paymentSet",
                "payment_set",
                fallback_currency=currency,
            ),
            "refund": _money(
                cash_rounding,
                "refundSet",
                "refund_set",
                fallback_currency=currency,
            ),
        },
        "is_draft": is_draft,
        "draft_status": str(payload.get("status") or "").upper() if is_draft else "",
        "completed_order_id": shopify_gid(
            "Order", (payload.get("order") or {}).get("id")
        ),
        "customer_id": shopify_gid(
            "Customer",
            (payload.get("customer") or {}).get("id") or payload.get("customer_id"),
        ),
        "tax_country_code": str(
            (payload.get("shippingAddress") or {}).get("countryCodeV2")
            or (payload.get("shipping_address") or {}).get("country_code")
            or (payload.get("billingAddress") or {}).get("countryCodeV2")
            or (payload.get("billing_address") or {}).get("country_code")
            or ""
        ).upper(),
        "email": str(payload.get("email") or payload.get("contactEmail") or ""),
        "note": str(payload.get("note2") or payload.get("note") or ""),
        "tags": [
            str(tag).strip()
            for tag in (
                payload.get("tags")
                if isinstance(payload.get("tags"), list)
                else str(payload.get("tags") or "").split(",")
            )
            if str(tag).strip()
        ],
        "discount_codes": codes,
        "taxes_included": bool(
            payload.get("taxesIncluded") or payload.get("taxes_included")
        ),
        "risk_level": _risk_level(payload),
        "subtotal": _money(
            payload,
            "currentSubtotalPriceSet",
            "subtotalPriceSet",
            "current_subtotal_price_set",
            "subtotal_price_set",
            fallback_currency=currency,
        ),
        "discount_total": _money(
            payload,
            "currentTotalDiscountsSet",
            "totalDiscountsSet",
            "current_total_discounts_set",
            "total_discounts_set",
            "total_discounts",
            fallback_currency=currency,
        ),
        "shipping_total": _money(
            payload,
            "currentShippingPriceSet",
            "totalShippingPriceSet",
            "current_shipping_price_set",
            "total_shipping_price_set",
            fallback_currency=currency,
        ),
        "tax_total": _money(
            payload,
            "currentTotalTaxSet",
            "totalTaxSet",
            "current_total_tax_set",
            "total_tax_set",
            "total_tax",
            fallback_currency=currency,
        ),
        "total": _money(
            payload,
            "currentTotalPriceSet",
            "totalPriceSet",
            "current_total_price_set",
            "total_price_set",
            "total_price",
            fallback_currency=currency,
        ),
        "lines": [_normalise_line(item, currency) for item in _nodes(line_source)],
        "shipping_lines": [
            _normalise_shipping(item, currency) for item in _nodes(shipping_source)
        ],
        "transactions": [
            _normalise_transaction(item, currency)
            for item in _nodes(payload.get("transactions"))
        ],
        "refunds": [
            _normalise_refund(item, currency) for item in _nodes(payload.get("refunds"))
        ],
        "returns": [_normalise_return(item) for item in _nodes(payload.get("returns"))],
        "raw": payload,
    }
    if not order["name"]:
        order["name"] = order["number"] or identifier.rsplit("/", 1)[-1]
    return order


def normalize_refund_payload(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Normalise a standalone refunds/create webhook."""
    order_id = shopify_gid(
        "Order",
        payload.get("order_id") or (payload.get("order") or {}).get("id"),
    )
    currency = str(payload.get("currency") or "").upper()
    if not order_id:
        raise ShopifyOrderPayloadError("Refund payload has no order ID.")
    return order_id, _normalise_refund(payload, currency)


def normalize_bulk_orders(  # noqa: C901
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reassemble Shopify bulk JSONL rows into complete current order snapshots."""
    roots: dict[str, dict[str, Any]] = {}
    children: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        if not isinstance(row, dict):
            continue
        parent = row.get("__parentId")
        if parent:
            children[str(parent)].append(dict(row))
        elif str(row.get("id") or "").startswith("gid://shopify/Order/"):
            roots[str(row["id"])] = dict(row)

    def attach(node: dict[str, Any]) -> None:  # noqa: C901
        node_children = children.get(str(node.get("id")), [])
        line_items = []
        shipping_lines = []
        refunds = []
        transactions = []
        refund_shipping_lines = []
        order_adjustments = []
        refund_line_items = []
        returns = []
        return_line_items = []
        exchange_line_items = []
        for child in node_children:
            identifier = str(child.get("id") or "")
            resource = (
                identifier.rsplit("/", 2)[-2]
                if identifier.startswith("gid://") and "/" in identifier
                else ""
            )
            if resource == "LineItem":
                attach(child)
                line_items.append(child)
            elif resource == "ShippingLine":
                shipping_lines.append(child)
            elif resource == "Refund":
                attach(child)
                refunds.append(child)
            elif resource == "OrderTransaction":
                transactions.append(child)
            elif resource == "RefundLineItem":
                refund_line_items.append(child)
            elif resource == "RefundShippingLine":
                refund_shipping_lines.append(child)
            elif resource == "OrderAdjustment":
                order_adjustments.append(child)
            elif resource == "Return":
                attach(child)
                returns.append(child)
            elif resource == "ReturnLineItem":
                return_line_items.append(child)
            elif resource == "ExchangeLineItem":
                exchange_line_items.append(child)
        if line_items:
            node["lineItems"] = {"nodes": line_items}
        if shipping_lines:
            node["shippingLines"] = {"nodes": shipping_lines}
        if refunds:
            node["refunds"] = {"nodes": refunds}
        if transactions:
            node["transactions"] = transactions
        if refund_line_items:
            node["refundLineItems"] = {"nodes": refund_line_items}
        if refund_shipping_lines:
            node["refundShippingLines"] = {"nodes": refund_shipping_lines}
        if order_adjustments:
            node["orderAdjustments"] = {"nodes": order_adjustments}
        if returns:
            node["returns"] = {"nodes": returns}
        if return_line_items:
            node["returnLineItems"] = {"nodes": return_line_items}
        if exchange_line_items:
            node["exchangeLineItems"] = {"nodes": exchange_line_items}

    result = []
    for root in roots.values():
        attach(root)
        result.append(normalize_order_payload(root))
    return result


def line_diffs(
    existing: Iterable[dict[str, Any]], incoming: Iterable[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Return deterministic add/update/remove operations keyed by Shopify line ID."""
    old = {str(item["id"]): item for item in existing}
    new = {str(item["id"]): item for item in incoming}
    added = [new[key] for key in sorted(new.keys() - old.keys())]
    removed = [old[key] for key in sorted(old.keys() - new.keys())]
    updated = [
        {"before": old[key], "after": new[key]}
        for key in sorted(old.keys() & new.keys())
        if old[key] != new[key]
    ]
    return {"add": added, "update": updated, "remove": removed}


def allocate_amount(total: Any, weights: Iterable[Any], quantum: Any) -> list[Decimal]:
    """Allocate exactly using largest remainders, including negative totals."""
    amount = decimal_amount(total)
    unit = decimal_amount(quantum)
    values = [max(decimal_amount(weight), Decimal("0")) for weight in weights]
    if unit <= 0:
        raise ValueError("Allocation quantum must be positive.")
    if not values:
        return []
    if not any(values):
        values = [Decimal("1")] * len(values)
    sign = Decimal("-1") if amount < 0 else Decimal("1")
    positive = abs(amount)
    total_weight = sum(values)
    exact = [positive * weight / total_weight for weight in values]
    base = [
        (value / unit).to_integral_value(rounding=ROUND_DOWN) * unit for value in exact
    ]
    remaining_units = int(
        ((positive - sum(base)) / unit).to_integral_value(rounding=ROUND_DOWN)
    )
    order = sorted(
        range(len(values)),
        key=lambda index: (exact[index] - base[index], -index),
        reverse=True,
    )
    for index in order[:remaining_units]:
        base[index] += unit
    remainder = positive - sum(base)
    if remainder:
        base[order[0]] += remainder
    return [value * sign for value in base]


def allocate_refund(
    total: Any,
    refundable_lines: Iterable[dict[str, Any]],
    quantum: Any,
) -> list[dict[str, Any]]:
    """Allocate a partial refund by each line's remaining refundable value."""
    lines = list(refundable_lines)
    allocations = allocate_amount(
        total,
        [line.get("refundable_amount", "0") for line in lines],
        quantum,
    )
    result = []
    for line, amount in zip(lines, allocations, strict=False):
        available = decimal_amount(line.get("refundable_amount"))
        if abs(amount) > available:
            raise ShopifyOrderPayloadError(
                "Refund allocation exceeds a line's refundable amount."
            )
        result.append({**line, "allocated_amount": amount})
    return result


def payload_digest(payload: dict[str, Any]) -> str:
    """Stable idempotency fingerprint for a normalised order snapshot."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()
