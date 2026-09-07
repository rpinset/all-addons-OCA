"""Shopify webhook authentication helpers using only the standard library."""

from __future__ import annotations

import base64
import hashlib
import hmac


def verify_webhook_hmac(
    payload: bytes, secret: str | bytes, provided_hmac: str | None
) -> bool:
    """Return whether a Shopify HMAC header authenticates ``payload``."""

    if not provided_hmac or not secret:
        return False
    secret_bytes = secret.encode("utf-8") if isinstance(secret, str) else secret
    digest = hmac.new(secret_bytes, payload, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("ascii")
    try:
        return hmac.compare_digest(expected, provided_hmac.strip())
    except (TypeError, ValueError):
        return False
