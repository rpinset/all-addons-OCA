"""Pure helpers for connector onboarding and operational summaries."""

from __future__ import annotations

from collections.abc import Iterable


def scope_handles(payload: dict) -> set[str]:
    """Extract normalized access-scope handles from Shopify's response."""
    installation = payload.get("currentAppInstallation") or {}
    scopes = installation.get("accessScopes") or []
    return {
        str(scope.get("handle") or "").strip()
        for scope in scopes
        if isinstance(scope, dict) and scope.get("handle")
    }


def missing_scopes(granted: Iterable[str], required: Iterable[str]) -> tuple[str, ...]:
    """Return the required handles absent from the granted set."""
    granted_set = {str(handle).strip() for handle in granted if str(handle).strip()}
    return tuple(
        sorted(
            {str(handle).strip() for handle in required if str(handle).strip()}
            - granted_set
        )
    )


def state_count_label(counts: dict[str, int]) -> str:
    """Format binding state counts consistently for stock Odoo views."""
    return (
        f"{counts.get('synced', 0)} synced · "
        f"{counts.get('pending', 0)} pending · "
        f"{counts.get('error', 0)} errors"
    )
