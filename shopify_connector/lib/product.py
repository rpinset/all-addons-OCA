"""Pure-Python helpers for Shopify product payloads."""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Iterable
from copy import deepcopy
from typing import Any

SYNC_FIELDS = ("name", "description", "price", "images", "status")
VALID_OWNERS = {"odoo", "shopify"}


class ShopifyProductPayloadError(ValueError):
    """Raised when a product payload or JSONL result is malformed."""


def sign_product_image_path(
    secret: str,
    instance_id: int,
    model_name: str,
    record_id: int,
    checksum: str,
) -> str:
    """Sign a narrow product-image download path for Shopify."""

    message = f"{instance_id}:{model_name}:{record_id}:{checksum}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def verify_product_image_signature(
    signature: str,
    secret: str,
    instance_id: int,
    model_name: str,
    record_id: int,
    checksum: str,
) -> bool:
    """Verify a product-image path signature without timing leaks."""

    expected = sign_product_image_path(
        secret, instance_id, model_name, record_id, checksum
    )
    return hmac.compare_digest(signature or "", expected)


def parse_jsonl(
    content: bytes | str | Iterable[bytes | str],
) -> list[dict[str, Any]]:
    """Parse JSON Lines while accepting byte streams, text, and blank lines."""

    if isinstance(content, bytes):
        lines: Iterable[bytes | str] = content.splitlines()
    elif isinstance(content, str):
        lines = content.splitlines()
    else:
        lines = content

    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(lines, start=1):
        if not isinstance(raw_line, (bytes, str)):
            raise ShopifyProductPayloadError(
                f"JSONL line {line_number} is not bytes or text."
            )
        try:
            line = (
                raw_line.decode("utf-8-sig")
                if isinstance(raw_line, bytes)
                else raw_line.lstrip("\ufeff")
            )
        except UnicodeDecodeError as exc:
            raise ShopifyProductPayloadError(
                f"JSONL line {line_number} is not valid UTF-8."
            ) from exc
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ShopifyProductPayloadError(
                f"JSONL line {line_number} is invalid JSON."
            ) from exc
        if not isinstance(record, dict):
            raise ShopifyProductPayloadError(
                f"JSONL line {line_number} is not a JSON object."
            )
        records.append(record)
    return records


def merge_owned_fields(
    current: dict[str, Any],
    incoming: dict[str, Any],
    ownership: dict[str, str],
    *,
    source: str,
    seed_missing: bool = False,
) -> dict[str, Any]:
    """Merge sync fields only when the incoming side owns the field.

    ``seed_missing`` is intended for first creation, where the non-owner side
    does not yet have a value to preserve.
    """

    if source not in VALID_OWNERS:
        raise ValueError(f"Unknown ownership source: {source}")
    result = deepcopy(current)
    for field_name in SYNC_FIELDS:
        owner = ownership.get(field_name)
        if owner not in VALID_OWNERS:
            raise ValueError(f"Missing or invalid owner for {field_name}.")
        if field_name not in incoming:
            continue
        if owner == source or (seed_missing and field_name not in current):
            result[field_name] = deepcopy(incoming[field_name])
    return result


def normalize_product_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize GraphQL, webhook, or assembled bulk product shapes."""

    if not isinstance(payload, dict):
        raise ShopifyProductPayloadError("Product payload must be an object.")
    shopify_id = _gid(
        payload.get("admin_graphql_api_id") or payload.get("id"),
        "Product",
    )
    if not shopify_id:
        raise ShopifyProductPayloadError("Product payload has no Shopify ID.")

    options = [
        _normalize_option(option)
        for option in _nodes(payload.get("options"))
        if isinstance(option, dict)
    ]
    variants = [
        _normalize_variant(variant, options)
        for variant in _nodes(payload.get("variants"))
        if isinstance(variant, dict)
    ]
    images_source = payload.get("media")
    if images_source is None:
        images_source = payload.get("images")
    images = [
        _normalize_image(image)
        for image in _nodes(images_source)
        if isinstance(image, dict)
    ]
    featured_media = payload.get("featuredMedia") or payload.get("featured_media")
    if isinstance(featured_media, dict):
        featured = _normalize_image(featured_media)
        if featured["id"] and not any(
            image["id"] == featured["id"] for image in images
        ):
            images.insert(0, featured)

    collections = [
        _normalize_collection(collection)
        for collection in _nodes(payload.get("collections"))
        if isinstance(collection, dict)
    ]
    status = str(payload.get("status") or "DRAFT").upper()
    description = payload.get("descriptionHtml")
    if description is None:
        description = payload.get("body_html")
    if description is None:
        description = payload.get("description") or ""

    return {
        "id": shopify_id,
        "name": payload.get("title") or payload.get("name") or "",
        "description": description,
        "handle": payload.get("handle") or "",
        "status": status,
        "updated_at": payload.get("updatedAt") or payload.get("updated_at"),
        "options": options,
        "variants": variants,
        "images": images,
        "collections": collections,
    }


def normalize_bulk_products(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reassemble Shopify bulk child rows and normalize each product."""

    products: dict[str, dict[str, Any]] = {}
    child_rows: list[dict[str, Any]] = []
    variants: dict[str, dict[str, Any]] = {}

    for row in records:
        row_id = str(row.get("id") or "")
        parent_id = row.get("__parentId")
        if not parent_id and _gid_type(row_id) == "Product":
            for connection_name in ("variants", "media", "collections"):
                if not isinstance(row.get(connection_name), list):
                    row[connection_name] = []
            products[row_id] = row
        else:
            child_rows.append(row)

    for row in child_rows:
        row_id = str(row.get("id") or "")
        parent_id = str(row.get("__parentId") or "")
        row_type = _gid_type(row_id)
        if row_type == "ProductVariant" and parent_id in products:
            products[parent_id]["variants"].append(row)
            variants[row_id] = row
    for row in child_rows:
        row_id = str(row.get("id") or "")
        parent_id = str(row.get("__parentId") or "")
        row_type = _gid_type(row_id)
        if row_type in {"MediaImage", "ProductImage"}:
            if parent_id in products:
                products[parent_id]["media"].append(row)
            elif parent_id in variants:
                variants[parent_id].setdefault("media", []).append(row)
        elif row_type == "Collection" and parent_id in products:
            products[parent_id]["collections"].append(row)

    return [normalize_product_payload(product) for product in products.values()]


def _nodes(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if not isinstance(value, dict):
        return []
    if isinstance(value.get("nodes"), list):
        return value["nodes"]
    edges = value.get("edges")
    if isinstance(edges, list):
        return [
            edge.get("node")
            for edge in edges
            if isinstance(edge, dict) and edge.get("node") is not None
        ]
    return []


def _normalize_option(option: dict[str, Any]) -> dict[str, Any]:
    values = option.get("optionValues")
    if values is None:
        values = option.get("values")
    normalized_values = []
    for value in _nodes(values) if isinstance(values, dict) else values or []:
        if isinstance(value, dict):
            name = value.get("name") or value.get("value")
        else:
            name = value
        if name is not None:
            normalized_values.append(str(name))
    return {
        "id": _gid(option.get("id"), "ProductOption"),
        "name": str(option.get("name") or ""),
        "position": int(option.get("position") or 0),
        "values": normalized_values,
    }


def _normalize_variant(
    variant: dict[str, Any], product_options: list[dict[str, Any]]
) -> dict[str, Any]:
    selected_options = []
    raw_selected = variant.get("selectedOptions")
    if raw_selected is None:
        raw_selected = variant.get("selected_options")
    for option in raw_selected or []:
        if isinstance(option, dict):
            selected_options.append(
                {
                    "name": str(option.get("name") or option.get("optionName") or ""),
                    "value": str(option.get("value") or option.get("name") or ""),
                }
            )
    if not selected_options:
        for position in range(1, 4):
            value = variant.get(f"option{position}")
            if value:
                option_name = (
                    product_options[position - 1]["name"]
                    if len(product_options) >= position
                    else f"Option {position}"
                )
                selected_options.append({"name": option_name, "value": str(value)})

    media_ids = [
        _gid(media_id, "MediaImage")
        for media_id in variant.get("media_ids", [])
        if media_id
    ]
    media_ids.extend(
        _gid(media.get("id"), "MediaImage")
        for media in _nodes(variant.get("media"))
        if isinstance(media, dict) and media.get("id")
    )
    media_ids = list(dict.fromkeys(media_ids))
    featured_media = variant.get("featuredMedia") or variant.get("featured_media")
    if isinstance(featured_media, dict) and featured_media.get("id"):
        media_id = _gid(featured_media["id"], "MediaImage")
        if media_id not in media_ids:
            media_ids.insert(0, media_id)
    elif variant.get("image_id"):
        media_id = _gid(variant["image_id"], "MediaImage")
        if media_id not in media_ids:
            media_ids.insert(0, media_id)

    inventory_item = variant.get("inventoryItem")
    if not isinstance(inventory_item, dict):
        inventory_item = variant.get("inventory_item")
    if not isinstance(inventory_item, dict):
        inventory_item = {}
    inventory_item_id = (
        inventory_item.get("admin_graphql_api_id")
        or inventory_item.get("id")
        or variant.get("inventory_item_admin_graphql_api_id")
        or variant.get("inventory_item_id")
    )
    tracked = inventory_item.get("tracked")
    if tracked is None:
        tracked = variant.get("inventory_tracked")
    if tracked is None:
        tracked = variant.get("inventory_management") == "shopify"

    return {
        "id": _gid(
            variant.get("admin_graphql_api_id") or variant.get("id"),
            "ProductVariant",
        ),
        "title": str(variant.get("title") or ""),
        "sku": str(variant.get("sku") or ""),
        "barcode": str(variant.get("barcode") or ""),
        "price": str(variant.get("price") or "0"),
        "selected_options": selected_options,
        "media_ids": [media_id for media_id in media_ids if media_id],
        "inventory_item_id": _gid(inventory_item_id, "InventoryItem"),
        "inventory_tracked": bool(tracked),
        "updated_at": variant.get("updatedAt") or variant.get("updated_at"),
    }


def _normalize_image(image: dict[str, Any]) -> dict[str, Any]:
    nested_image = image.get("image")
    if not isinstance(nested_image, dict):
        nested_image = {}
    preview = image.get("preview")
    preview_image = (
        preview.get("image")
        if isinstance(preview, dict) and isinstance(preview.get("image"), dict)
        else {}
    )
    source = (
        nested_image.get("url")
        or preview_image.get("url")
        or image.get("url")
        or image.get("src")
        or image.get("originalSource")
        or ""
    )
    return {
        "id": _gid(
            image.get("admin_graphql_api_id") or image.get("id"),
            "MediaImage",
        ),
        "url": str(source),
        "alt": str(
            image.get("alt")
            or image.get("altText")
            or nested_image.get("altText")
            or ""
        ),
        "media_content_type": str(
            image.get("mediaContentType") or image.get("media_content_type") or "IMAGE"
        ).upper(),
    }


def _normalize_collection(collection: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": _gid(collection.get("id"), "Collection"),
        "name": str(collection.get("title") or collection.get("name") or ""),
        "handle": str(collection.get("handle") or ""),
        "type": collection.get("type")
        or ("smart" if collection.get("ruleSet") else "custom"),
        "updated_at": collection.get("updatedAt") or collection.get("updated_at"),
    }


def _gid(value: Any, resource: str) -> str:
    if value is None or value == "":
        return ""
    text = str(value)
    if text.startswith("gid://shopify/"):
        return text
    return f"gid://shopify/{resource}/{text}"


def _gid_type(gid: str) -> str:
    parts = gid.split("/")
    return parts[-2] if len(parts) >= 2 else ""
