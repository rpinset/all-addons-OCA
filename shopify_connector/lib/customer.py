"""Pure-Python helpers for Shopify customer synchronization."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


class ShopifyCustomerPayloadError(ValueError):
    """Raised when a Shopify customer payload is malformed."""


PHONE_SEARCH_SUFFIX_DIGITS = 4


def normalize_email(value: Any) -> str:
    """Normalize an email for deterministic, case-insensitive matching."""

    return str(value or "").strip().casefold()


def normalize_phone(
    value: Any, default_country_calling_code: str | int | None = None
) -> str:
    """Normalize common international/local formats without dependencies."""

    raw = str(value or "").strip()
    if not raw:
        return ""
    raw = re.split(r"(?:ext\.?|extension|x)\s*\d+\s*$", raw, flags=re.I)[0]
    explicit_international = raw.startswith("+") or raw.startswith("00")
    digits = re.sub(r"\D", "", raw)
    if raw.startswith("00"):
        digits = digits[2:]
    country = re.sub(r"\D", "", str(default_country_calling_code or ""))
    if not explicit_international and country:
        digits = digits.lstrip("0")
        if not digits.startswith(country):
            digits = f"{country}{digits}"
        explicit_international = True
    if not digits:
        return ""
    if explicit_international and 7 <= len(digits) <= 15:
        return f"+{digits}"
    return digits


def phone_search_suffix(
    normalized_phone: str, digits: int = PHONE_SEARCH_SUFFIX_DIGITS
) -> str:
    """Return a selective suffix suitable for a server-side candidate query."""

    number = re.sub(r"\D", "", str(normalized_phone or ""))
    if digits < 1 or len(number) < digits:
        return ""
    return number[-digits:]


def normalize_customer_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize GraphQL, webhook, and bulk customer shapes."""

    if not isinstance(payload, Mapping):
        raise ShopifyCustomerPayloadError("Customer payload must be an object.")
    customer_id = _gid(
        payload.get("admin_graphql_api_id") or payload.get("id"), "Customer"
    )
    if not customer_id:
        raise ShopifyCustomerPayloadError("Customer payload has no Shopify ID.")
    first_name = str(payload.get("firstName") or payload.get("first_name") or "")
    last_name = str(payload.get("lastName") or payload.get("last_name") or "")
    display_name = str(
        payload.get("displayName")
        or payload.get("name")
        or " ".join(part for part in (first_name, last_name) if part)
        or payload.get("email")
        or payload.get("phone")
        or ""
    )
    default_email = payload.get("defaultEmailAddress") or {}
    default_phone = payload.get("defaultPhoneNumber") or {}
    consent = (
        payload.get("emailMarketingConsent")
        or payload.get("email_marketing_consent")
        or {}
    )
    tags = payload.get("tags") or []
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    addresses = [
        normalize_customer_address(address)
        for address in _nodes(payload.get("addressesV2") or payload.get("addresses"))
        if isinstance(address, Mapping)
    ]
    default_address = payload.get("defaultAddress") or payload.get("default_address")
    default_address_id = (
        _gid(default_address.get("id"), "MailingAddress")
        if isinstance(default_address, Mapping)
        else ""
    )
    if (
        isinstance(default_address, Mapping)
        and default_address_id
        and not any(address["id"] == default_address_id for address in addresses)
    ):
        addresses.insert(0, normalize_customer_address(default_address))
    for address in addresses:
        address["is_default"] = address["id"] == default_address_id
    return {
        "id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "name": display_name,
        "email": normalize_email(
            payload.get("email") or default_email.get("emailAddress")
        ),
        "phone": str(payload.get("phone") or default_phone.get("phoneNumber") or ""),
        "marketing_state": str(
            consent.get("marketingState") or consent.get("state") or "NOT_SUBSCRIBED"
        ).upper(),
        "tags": sorted({str(tag).strip() for tag in tags if str(tag).strip()}),
        "tax_exempt": bool(
            payload.get("taxExempt")
            if payload.get("taxExempt") is not None
            else payload.get("tax_exempt")
        ),
        "updated_at": payload.get("updatedAt") or payload.get("updated_at"),
        "addresses": addresses,
    }


def normalize_customer_address(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize a Shopify customer mailing address."""

    return {
        "id": _gid(
            payload.get("admin_graphql_api_id") or payload.get("id"),
            "MailingAddress",
        ),
        "first_name": str(payload.get("firstName") or payload.get("first_name") or ""),
        "last_name": str(payload.get("lastName") or payload.get("last_name") or ""),
        "company": str(payload.get("company") or ""),
        "address1": str(payload.get("address1") or ""),
        "address2": str(payload.get("address2") or ""),
        "city": str(payload.get("city") or ""),
        "province": str(
            payload.get("province")
            or payload.get("provinceCode")
            or payload.get("province_code")
            or ""
        ),
        "country": str(
            payload.get("countryCodeV2")
            or payload.get("countryCode")
            or payload.get("country_code")
            or payload.get("country")
            or ""
        ).upper(),
        "zip": str(payload.get("zip") or ""),
        "phone": str(payload.get("phone") or ""),
        "is_default": bool(payload.get("default") or payload.get("is_default")),
    }


def diff_customer_addresses(
    existing: Iterable[Mapping[str, Any]],
    incoming: Iterable[Mapping[str, Any]],
) -> dict[str, list[Any]]:
    """Diff address snapshots by Shopify ID, then by stable content."""

    old = [dict(address) for address in existing]
    new = [dict(address) for address in incoming]
    old_by_id = {address.get("id"): address for address in old if address.get("id")}
    matched_old: set[int] = set()
    creates = []
    updates = []
    for address in new:
        current = old_by_id.get(address.get("id"))
        if current is None:
            fingerprint = _address_fingerprint(address)
            current = next(
                (
                    candidate
                    for candidate in old
                    if id(candidate) not in matched_old
                    and _address_fingerprint(candidate) == fingerprint
                ),
                None,
            )
        if current is None:
            creates.append(address)
            continue
        matched_old.add(id(current))
        if _address_fingerprint(current) != _address_fingerprint(address):
            updates.append((current, address))
    deletes = [address for address in old if id(address) not in matched_old]
    return {"create": creates, "update": updates, "delete": deletes}


def normalize_bulk_customers(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reassemble Customer and MailingAddress bulk JSONL records."""

    customers: dict[str, dict[str, Any]] = {}
    children = []
    for record in records:
        record_id = str(record.get("id") or "")
        if not record.get("__parentId") and "/Customer/" in record_id:
            customer = dict(record)
            customer["addresses"] = []
            customers[record_id] = customer
        else:
            children.append(record)
    for record in children:
        parent_id = str(record.get("__parentId") or "")
        if parent_id in customers and "/MailingAddress/" in str(record.get("id") or ""):
            customers[parent_id]["addresses"].append(record)
    return [normalize_customer_payload(customer) for customer in customers.values()]


def _address_fingerprint(address: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(
        str(address.get(field) or "").strip().casefold()
        for field in (
            "first_name",
            "last_name",
            "company",
            "address1",
            "address2",
            "city",
            "province",
            "country",
            "zip",
            "phone",
            "is_default",
        )
    )


def _nodes(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not isinstance(value, Mapping):
        return []
    if isinstance(value.get("nodes"), list):
        return value["nodes"]
    if isinstance(value.get("edges"), list):
        return [
            edge.get("node")
            for edge in value["edges"]
            if isinstance(edge, Mapping) and edge.get("node") is not None
        ]
    return []


def _gid(value: Any, resource: str) -> str:
    if value is None or value == "":
        return ""
    text = str(value)
    if text.startswith("gid://shopify/"):
        return text
    return f"gid://shopify/{resource}/{text}"
