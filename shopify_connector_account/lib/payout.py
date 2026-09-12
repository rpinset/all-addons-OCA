"""Odoo-free Shopify Payments normalization and entry planning."""

from __future__ import annotations

from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any


class PayoutPlanningError(ValueError):
    """Base error for payout normalization and entry planning."""


class PayoutNetMismatch(PayoutPlanningError):
    """Transaction net total does not equal Shopify's payout net."""


class TransactionNetMismatch(PayoutPlanningError):
    """A transaction's amount less fee does not equal its net."""


class EntryPlanMismatch(PayoutPlanningError):
    """The proposed accounting plan is not exactly balanced."""


class MissingAccountMapping(PayoutPlanningError):
    """A required account route was not supplied."""


def decimal_amount(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if value in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PayoutPlanningError(f"Invalid monetary amount: {value!r}.") from exc


def _money(value: Any, fallback_currency: str = "") -> dict[str, str]:
    value = value or {}
    if not isinstance(value, dict):
        value = {"amount": value, "currencyCode": fallback_currency}
    return {
        "amount": format(decimal_amount(value.get("amount")), "f"),
        "currency": str(
            value.get("currencyCode")
            or value.get("currency")
            or fallback_currency
            or ""
        ).upper(),
    }


def normalize_payout(payload: dict[str, Any]) -> dict[str, Any]:
    net = _money(payload.get("net"))
    summary = payload.get("summary") or {}
    gross = Decimal("0")
    fees = Decimal("0")
    for name, value in summary.items():
        amount = decimal_amount(_money(value, net["currency"])["amount"])
        lowered = str(name).lower()
        if lowered.endswith("gross") or lowered == "usdcrebatecreditamount":
            gross += amount
        elif lowered.endswith("fee") or lowered.endswith("fees"):
            fees += amount
    return {
        "id": str(payload.get("id") or ""),
        "legacy_id": str(payload.get("legacyResourceId") or ""),
        "reference": str(
            payload.get("externalTraceId")
            or payload.get("legacyResourceId")
            or payload.get("id")
            or ""
        ),
        "issued_at": payload.get("issuedAt"),
        "status": str(payload.get("status") or "").upper(),
        "transaction_type": str(payload.get("transactionType") or "").upper(),
        "currency": net["currency"],
        "gross": format(gross, "f"),
        "fees": format(fees, "f"),
        "net": net["amount"],
        "summary": summary,
        "raw": payload,
    }


def normalize_transaction(payload: dict[str, Any]) -> dict[str, Any]:
    amount = _money(payload.get("amount"))
    fee = _money(payload.get("fee"), amount["currency"])
    net = _money(payload.get("net"), amount["currency"])
    associated_order = payload.get("associatedOrder") or {}
    associated_payout = payload.get("associatedPayout") or {}
    return {
        "id": str(payload.get("id") or ""),
        "type": str(payload.get("type") or "").upper(),
        "display_type": str(payload.get("displayType") or ""),
        "source_type": str(payload.get("sourceType") or "").upper(),
        "source_id": str(payload.get("sourceId") or ""),
        "source_order_transaction_id": str(
            payload.get("sourceOrderTransactionId") or ""
        ),
        "payout_id": str(associated_payout.get("id") or ""),
        "order_id": str(associated_order.get("id") or ""),
        "order_name": str(associated_order.get("name") or ""),
        "transaction_date": payload.get("transactionDate"),
        "currency": amount["currency"],
        "amount": amount["amount"],
        "fee": fee["amount"],
        "net": net["amount"],
        "adjustment_reason": str(payload.get("adjustmentReason") or ""),
        "test": bool(payload.get("test")),
        "raw": payload,
    }


def normalize_dispute(payload: dict[str, Any]) -> dict[str, Any]:
    amount = _money(payload.get("amount"))
    reason = payload.get("reasonDetails") or {}
    return {
        "id": str(payload.get("id") or ""),
        "order_id": str((payload.get("order") or {}).get("id") or ""),
        "amount": amount["amount"],
        "currency": amount["currency"],
        "status": str(payload.get("status") or "").upper(),
        "type": str(payload.get("type") or "").upper(),
        "reason": str(reason.get("reason") or ""),
        "network_reason_code": str(reason.get("networkReasonCode") or ""),
        "initiated_at": payload.get("initiatedAt"),
        "evidence_due_by": payload.get("evidenceDueBy"),
        "evidence_sent_on": payload.get("evidenceSentOn"),
        "finalized_on": payload.get("finalizedOn"),
        "raw": payload,
    }


def _rounded(value: Any, quantum: Decimal) -> Decimal:
    return decimal_amount(value).quantize(quantum, rounding=ROUND_HALF_UP)


def _line(
    *,
    role: str,
    account: Any,
    name: str,
    balance: Decimal,
    amount_currency: Decimal,
    currency: str,
    transaction_id: str = "",
) -> dict[str, Any]:
    if account in (None, "", False):
        raise MissingAccountMapping(f"No account mapping is configured for {name}.")
    return {
        "role": role,
        "account": account,
        "name": name,
        "debit": format(max(balance, Decimal("0")), "f"),
        "credit": format(max(-balance, Decimal("0")), "f"),
        "balance": format(balance, "f"),
        "amount_currency": format(amount_currency, "f"),
        "currency": currency,
        "transaction_id": transaction_id,
    }


def plan_payout_entry(
    payout: dict[str, Any],
    transactions: Iterable[dict[str, Any]],
    accounts: dict[str, Any],
    *,
    company_currency: str,
    quantum: Any = "0.01",
) -> dict[str, Any]:
    """Return a balanced exact-decimal plan or raise a typed error."""
    transactions = [dict(item) for item in transactions]
    payout_currency = str(payout.get("currency") or "").upper()
    company_currency = str(company_currency or "").upper()
    rounding = decimal_amount(quantum)
    payout_net = decimal_amount(payout.get("net"))
    transaction_net = Decimal("0")
    for transaction in transactions:
        if str(transaction.get("currency") or "").upper() != payout_currency:
            raise PayoutPlanningError(
                f"Transaction {transaction.get('id') or '-'} currency does "
                f"not match payout currency {payout_currency}."
            )
        amount = decimal_amount(transaction.get("amount"))
        fee = decimal_amount(transaction.get("fee"))
        net = decimal_amount(transaction.get("net"))
        if amount - fee != net:
            raise TransactionNetMismatch(
                f"Transaction {transaction.get('id') or '-'}: amount "
                f"{amount} less fee {fee} does not equal net {net}."
            )
        transaction_net += net
    if transaction_net != payout_net:
        raise PayoutNetMismatch(
            f"Payout net {payout_net} does not equal transaction net "
            f"{transaction_net} {payout_currency}."
        )

    bank_balance = _rounded(payout.get("company_net", payout_net), rounding)
    lines = [
        _line(
            role="payout",
            account=accounts.get("payout"),
            name=str(payout.get("reference") or "Shopify payout"),
            balance=bank_balance,
            amount_currency=payout_net,
            currency=payout_currency,
        )
    ]
    for transaction in transactions:
        transaction_id = str(transaction.get("id") or "")
        amount = decimal_amount(transaction.get("amount"))
        fee = decimal_amount(transaction.get("fee"))
        company_amount = _rounded(transaction.get("company_amount", amount), rounding)
        company_fee = _rounded(transaction.get("company_fee", fee), rounding)
        if amount:
            lines.append(
                _line(
                    role=str(transaction.get("route") or "clearing"),
                    account=transaction.get("account"),
                    name=str(
                        transaction.get("name")
                        or transaction.get("display_type")
                        or transaction.get("type")
                        or transaction_id
                    ),
                    balance=-company_amount,
                    amount_currency=-amount,
                    currency=payout_currency,
                    transaction_id=transaction_id,
                )
            )
        if fee:
            lines.append(
                _line(
                    role="fee",
                    account=accounts.get("fee"),
                    name=(
                        "Shopify fee: "
                        f"{transaction.get('display_type') or transaction_id}"
                    ),
                    balance=company_fee,
                    amount_currency=fee,
                    currency=payout_currency,
                    transaction_id=transaction_id,
                )
            )

    balance = sum(decimal_amount(line["balance"]) for line in lines)
    if balance:
        if payout_currency == company_currency:
            raise EntryPlanMismatch(
                f"Same-currency payout entry is out of balance by {balance} "
                f"{company_currency}."
            )
        fx_balance = -balance
        fx_account = (
            accounts.get("fx_loss") if fx_balance > 0 else accounts.get("fx_gain")
        )
        lines.append(
            _line(
                role="currency_difference",
                account=fx_account,
                name="Shopify payout currency difference",
                balance=fx_balance,
                amount_currency=Decimal("0"),
                currency=company_currency,
            )
        )
    final_balance = sum(decimal_amount(line["balance"]) for line in lines)
    if final_balance:
        raise EntryPlanMismatch(
            f"Entry plan is out of balance by {final_balance} {company_currency}."
        )
    return {
        "currency": payout_currency,
        "company_currency": company_currency,
        "net": format(payout_net, "f"),
        "lines": lines,
    }
