from decimal import Decimal

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector_account.lib.payout import (
    EntryPlanMismatch,
    PayoutNetMismatch,
    TransactionNetMismatch,
    normalize_payout,
    normalize_transaction,
    plan_payout_entry,
)

ACCOUNTS = {"payout": "bank", "fee": "fees", "fx_gain": "fx-gain", "fx_loss": "fx-loss"}


def _transaction(
    transaction_id,
    amount,
    fee,
    net,
    *,
    route="clearing",
    account="clearing",
    company_amount=None,
    company_fee=None,
    transaction_type="CHARGE",
):
    values = {
        "id": transaction_id,
        "currency": "USD",
        "amount": amount,
        "fee": fee,
        "net": net,
        "route": route,
        "account": account,
        "type": transaction_type,
        "display_type": transaction_type.title(),
    }
    if company_amount is not None:
        values["company_amount"] = company_amount
    if company_fee is not None:
        values["company_fee"] = company_fee
    return values


class TestShopifyLibPayout(TransactionCase):
    def test_payout_and_transaction_payloads_normalize_exact_decimals(self):
        payout = normalize_payout(
            {
                "id": "payout-1",
                "issuedAt": "2026-07-20T00:00:00Z",
                "status": "paid",
                "net": {"amount": "96.995", "currencyCode": "usd"},
                "summary": {
                    "chargesGross": {"amount": "100.000", "currencyCode": "USD"},
                    "chargesFee": {"amount": "3.005", "currencyCode": "USD"},
                },
            }
        )
        transaction = normalize_transaction(
            {
                "id": "transaction-1",
                "type": "CHARGE",
                "amount": {"amount": "100.000", "currencyCode": "USD"},
                "fee": {"amount": "3.005", "currencyCode": "USD"},
                "net": {"amount": "96.995", "currencyCode": "USD"},
            }
        )
        assert payout["gross"] == "100.000"
        assert payout["fees"] == "3.005"
        assert payout["net"] == "96.995"
        assert transaction["amount"] == "100.000"
        assert transaction["fee"] == "3.005"

    def test_balanced_charge_refund_and_fee_plan(self):
        plan = plan_payout_entry(
            {"currency": "USD", "net": "77.00", "reference": "P-1"},
            [
                _transaction("charge", "100.00", "3.00", "97.00"),
                _transaction("refund", "-20.00", "0.00", "-20.00"),
            ],
            ACCOUNTS,
            company_currency="USD",
        )
        assert (
            sum(
                Decimal(line["debit"]) - Decimal(line["credit"])
                for line in plan["lines"]
            )
            == 0
        )
        assert plan["lines"][0]["debit"] == "77.00"
        assert any(
            line["role"] == "fee" and line["debit"] == "3.00" for line in plan["lines"]
        )

    def test_fee_rounding_uses_currency_quantum(self):
        plan = plan_payout_entry(
            {"currency": "USD", "net": "10.000", "company_net": "10.00"},
            [
                _transaction(
                    "charge",
                    "10.006",
                    "0.006",
                    "10.000",
                    company_amount="10.006",
                    company_fee="0.006",
                )
            ],
            ACCOUNTS,
            company_currency="USD",
        )
        fee = next(line for line in plan["lines"] if line["role"] == "fee")
        assert fee["debit"] == "0.01"

    def test_multi_currency_plan_books_only_conversion_difference(self):
        plan = plan_payout_entry(
            {"currency": "USD", "net": "97.00", "company_net": "89.00"},
            [
                _transaction(
                    "charge",
                    "100.00",
                    "3.00",
                    "97.00",
                    company_amount="91.50",
                    company_fee="2.75",
                )
            ],
            ACCOUNTS,
            company_currency="EUR",
        )
        fx = next(
            line for line in plan["lines"] if line["role"] == "currency_difference"
        )
        assert fx["credit"] == "0.25"
        assert fx["account"] == "fx-gain"

    def test_payout_net_mismatch_is_typed(self):
        with self.assertRaisesRegex(PayoutNetMismatch, "does not equal"):
            plan_payout_entry(
                {"currency": "USD", "net": "98.00"},
                [_transaction("charge", "100.00", "3.00", "97.00")],
                ACCOUNTS,
                company_currency="USD",
            )

    def test_transaction_net_mismatch_is_typed(self):
        with self.assertRaisesRegex(TransactionNetMismatch, "less fee"):
            plan_payout_entry(
                {"currency": "USD", "net": "98.00"},
                [_transaction("charge", "100.00", "3.00", "98.00")],
                ACCOUNTS,
                company_currency="USD",
            )

    def test_same_currency_imbalance_is_typed_not_force_balanced(self):
        with self.assertRaisesRegex(EntryPlanMismatch, "out of balance"):
            plan_payout_entry(
                {"currency": "USD", "net": "97.00", "company_net": "97.01"},
                [_transaction("charge", "100.00", "3.00", "97.00")],
                ACCOUNTS,
                company_currency="USD",
            )

    def test_chargeback_reverses_clearing_and_books_fee(self):
        plan = plan_payout_entry(
            {"currency": "USD", "net": "-115.00"},
            [
                _transaction(
                    "chargeback",
                    "-100.00",
                    "15.00",
                    "-115.00",
                    transaction_type="CHARGEBACK_HOLD",
                )
            ],
            ACCOUNTS,
            company_currency="USD",
        )
        clearing = next(line for line in plan["lines"] if line["role"] == "clearing")
        fee = next(line for line in plan["lines"] if line["role"] == "fee")
        assert clearing["debit"] == "100.00"
        assert fee["debit"] == "15.00"

    def test_fee_correction_uses_the_mapped_fee_expense_account(self):
        plan = plan_payout_entry(
            {"currency": "USD", "net": "-5.00"},
            [
                _transaction(
                    "fee-correction",
                    "-5.00",
                    "0.00",
                    "-5.00",
                    route="fee",
                    account="fees",
                    transaction_type="CHARGEBACK_FEE",
                )
            ],
            ACCOUNTS,
            company_currency="USD",
        )
        correction = next(
            line for line in plan["lines"] if line["transaction_id"] == "fee-correction"
        )
        assert correction["account"] == "fees"
        assert correction["debit"] == "5.00"
