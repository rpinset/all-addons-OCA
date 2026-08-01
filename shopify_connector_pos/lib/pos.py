"""Exact-money and relation helpers for Shopify POS orders."""

from __future__ import annotations

from typing import Any

try:
    from odoo.addons.shopify_connector.lib.order import (
        decimal_amount,
        selected_money,
        shopify_gid,
    )
except ModuleNotFoundError as exc:
    if exc.name != "odoo":
        raise
    from shopify_connector.lib.order import (
        decimal_amount,
        selected_money,
        shopify_gid,
    )


def selected_cash_rounding(order: dict[str, Any], *, use_presentment: bool):
    """Return the exact payment rounding for the configured currency side."""
    rounding = (order.get("cash_rounding") or {}).get("payment") or {
        "shop": {"amount": "0", "currency": ""},
        "presentment": {"amount": "0", "currency": ""},
    }
    return decimal_amount(selected_money(rounding, use_presentment)["amount"])


def adjusted_pos_total(order: dict[str, Any], *, use_presentment: bool):
    """Return order total plus its cash-payment rounding adjustment."""
    total = decimal_amount(selected_money(order["total"], use_presentment)["amount"])
    return total + selected_cash_rounding(order, use_presentment=use_presentment)


def exchange_origin_gid(payload: dict[str, Any]) -> str:
    """Extract a classic POS exchange's original order without guessing."""
    for name in (
        "exchangeOriginOrder",
        "exchange_origin_order",
        "exchangeOriginalOrder",
        "exchange_original_order",
        "originalOrder",
        "original_order",
    ):
        value = payload.get(name)
        if isinstance(value, dict):
            value = value.get("id")
        if value:
            return shopify_gid("Order", value)
    for name in (
        "exchangeOriginalOrderId",
        "exchange_original_order_id",
        "exchange_origin_order_id",
        "originalOrderId",
        "original_order_id",
    ):
        if payload.get(name):
            return shopify_gid("Order", payload[name])
    return ""
