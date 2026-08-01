from __future__ import annotations

# pylint: disable=consider-merging-classes-inherited
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from odoo import api, fields, models
from odoo.fields import Command

from odoo.addons.shopify_connector.lib.client import ShopifyError, ShopifyUserError
from odoo.addons.shopify_connector.lib.order import shopify_gid

from ..graphql.payout import (
    SHOPIFY_PAYMENTS_DISPUTES_QUERY,
    SHOPIFY_PAYMENTS_PAYOUTS_QUERY,
    SHOPIFY_PAYMENTS_TRANSACTIONS_QUERY,
)
from ..lib.payout import (
    MissingAccountMapping,
    PayoutPlanningError,
    decimal_amount,
    normalize_dispute,
    normalize_payout,
    normalize_transaction,
    plan_payout_entry,
)

OPEN_DISPUTE_STATES = {
    "NEEDS_RESPONSE",
    "UNDER_REVIEW",
    "OPEN",
    "SUBMITTED",
}


def _utc_datetime(value):
    if not value:
        return False
    parsed = (
        value
        if isinstance(value, datetime)
        else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    )
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _date_query(field, date_from=None, date_to=None):
    terms = []
    if date_from:
        terms.append(f"{field}:>={str(date_from)[:10]}")
    if date_to:
        terms.append(f"{field}:<={str(date_to)[:10]}")
    return " ".join(terms) or None


class ShopifyInstancePayoutSync(models.Model):
    _inherit = "shopify.instance"

    @api.model
    def _cron_import_shopify_payouts(self):
        today = fields.Date.context_today(self)
        date_from = fields.Date.to_string(today - timedelta(days=7))
        date_to = fields.Date.to_string(today)
        for instance in self.search(
            [
                ("active", "=", True),
                ("state", "=", "connected"),
                ("shopify_payments_state", "!=", "unavailable"),
            ]
        ):
            instance.with_delay(
                description=self.env._(
                    "Daily Shopify Payments import for %s", instance.name
                ),
                identity_key=(f"shopify.payouts.daily.{instance.id}.{date_to}"),
            )._job_import_payouts(date_from, date_to)
            instance._write_log(
                entity="drift_payouts",
                direction="import",
                level="info",
                message=self.env._(
                    "Daily Shopify Payments payout drift import queued."
                ),
                record=instance,
            )

    def _payments_page(self, query, variables, connection):
        self.ensure_one()
        after = None
        records = []
        while True:
            data = self._shopify_client().execute(
                query,
                {**variables, "first": 250, "after": after},
            )
            account = data.get("shopifyPaymentsAccount")
            if not account:
                return None, []
            page = account.get(connection) or {}
            records.extend(page.get("nodes") or [])
            page_info = page.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                return account, records
            after = page_info.get("endCursor")

    def _job_import_payouts(self, date_from=False, date_to=False):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return []
        payout_query = _date_query("issued_at", date_from, date_to)
        try:
            account, payloads = self._payments_page(
                SHOPIFY_PAYMENTS_PAYOUTS_QUERY,
                {"query": payout_query},
                "payouts",
            )
        except ShopifyUserError as exc:
            self.shopify_payments_state = "unavailable"
            self._write_log(
                entity="payout",
                direction="import",
                level="info",
                message=self.env._("Shopify Payments is unavailable: %s", exc),
                record=self,
            )
            return []
        if not account or not account.get("activated"):
            self.shopify_payments_state = "unavailable"
            self._write_log(
                entity="payout",
                direction="import",
                level="info",
                message=self.env._("Shopify Payments is not active for this shop."),
                record=self,
            )
            return []
        self.shopify_payments_state = "enabled"
        imported = self.env["shopify.payout"]
        for payload in payloads:
            payout = self._upsert_payout(normalize_payout(payload))
            self._import_payout_transactions(payout)
            imported |= payout
        try:
            self._import_disputes(date_from, date_to)
        except ShopifyUserError as exc:
            self._write_log(
                entity="dispute",
                direction="import",
                level="warning",
                message=self.env._("Shopify disputes could not be imported: %s", exc),
                record=self,
            )
        self._write_log(
            entity="payout",
            direction="import",
            level="info",
            message=self.env._(
                "Imported %s Shopify Payments payout(s).", len(imported)
            ),
            record=self,
        )
        return imported.ids

    def _currency(self, code):
        currency = (
            self.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", code)], limit=1)
        )
        if not currency:
            raise PayoutPlanningError(
                f"Odoo has no currency record for Shopify currency {code}."
            )
        return currency

    def _upsert_payout(self, normalized):
        if not normalized["id"]:
            raise PayoutPlanningError("Shopify returned a payout without an ID.")
        currency = self._currency(normalized["currency"])
        values = {
            "instance_id": self.id,
            "shopify_id": normalized["id"],
            "reference": normalized["reference"],
            "legacy_resource_id": normalized["legacy_id"],
            "issued_at": _utc_datetime(normalized["issued_at"]),
            "payout_status": normalized["status"],
            "transaction_type": normalized["transaction_type"],
            "currency_id": currency.id,
            "gross_amount": normalized["gross"],
            "fee_amount": normalized["fees"],
            "net_amount": normalized["net"],
            "gross_exact": normalized["gross"],
            "fee_exact": normalized["fees"],
            "net_exact": normalized["net"],
            "summary": normalized["summary"],
            "raw_payload": normalized["raw"],
            "last_sync_date": fields.Datetime.now(),
            "state": "synced",
            "error_message": False,
        }
        payout = self.env["shopify.payout"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "=", normalized["id"]),
            ],
            limit=1,
        )
        if payout:
            payout.write(values)
        else:
            payout = self.env["shopify.payout"].create(values)
        return payout

    def _import_payout_transactions(self, payout):
        if not payout.legacy_resource_id:
            raise PayoutPlanningError(
                f"Payout {payout.reference} has no legacy ID for transaction filtering."
            )
        account, payloads = self._payments_page(
            SHOPIFY_PAYMENTS_TRANSACTIONS_QUERY,
            {"query": (f"payments_transfer_id:{payout.legacy_resource_id}")},
            "balanceTransactions",
        )
        if not account:
            return
        seen = set()
        for payload in payloads:
            normalized = normalize_transaction(payload)
            if normalized["payout_id"] and normalized["payout_id"] != payout.shopify_id:
                continue
            transaction = self._upsert_payout_transaction(payout, normalized)
            seen.add(transaction.shopify_id)
        payout.transaction_ids.filtered(
            lambda item: item.shopify_id not in seen
        ).unlink()

    def _gift_card_liability_account(self):
        self.ensure_one()
        account = self.gift_card_liability_account_id
        if account.account_type in (
            "liability_current",
            "liability_non_current",
        ):
            return account
        return self.env["account.account"]

    def _gateway_clearing_account(self, order_binding, source_order_transaction_id):
        payments = self.env["shopify.gateway.payment"].search(
            [
                ("instance_id", "=", self.id),
                ("order_binding_id", "=", order_binding.id),
            ]
        )
        if source_order_transaction_id:
            gid = shopify_gid("OrderTransaction", source_order_transaction_id)
            exact = payments.filtered(lambda item: item.transaction_shopify_id == gid)
            payments = exact or payments
        payment = payments[:1].payment_id
        if payment:
            return payment.move_id.line_ids.filtered(
                lambda line: (
                    line.account_id.account_type
                    not in ("asset_receivable", "liability_payable")
                )
            )[:1].account_id
        raw_transactions = (order_binding.raw_payload or {}).get("transactions") or []
        if isinstance(raw_transactions, dict):
            raw_transactions = raw_transactions.get("nodes") or []
        target_gid = shopify_gid("OrderTransaction", source_order_transaction_id)
        transaction = next(
            (
                item
                for item in raw_transactions
                if not target_gid
                or shopify_gid("OrderTransaction", item.get("id")) == target_gid
            ),
            {},
        )
        gateway = (
            str(transaction.get("gateway") or transaction.get("formattedGateway") or "")
            .strip()
            .lower()
        )
        mapping = self.env["shopify.gateway.journal"].search(
            [
                ("instance_id", "=", self.id),
                ("gateway", "=", gateway),
            ],
            limit=1,
        )
        return mapping.journal_id.default_account_id

    def _transaction_route(self, normalized, order_binding):
        transaction_type = normalized["type"]
        source_type = normalized["source_type"]
        if "GIFT_CARD" in transaction_type or "GIFT_CARD" in source_type:
            return "gift_card", self._gift_card_liability_account()
        if "FEE" in transaction_type:
            return "fee", self.payout_fee_account_id
        if order_binding:
            return (
                "clearing",
                self._gateway_clearing_account(
                    order_binding,
                    normalized["source_order_transaction_id"],
                ),
            )
        if (
            source_type
            in {
                "ADJUSTMENT",
                "ADJUSTMENT_REVERSAL",
                "DISPUTE",
                "SYSTEM_ADJUSTMENT",
                "TRANSFER",
            }
            or "ADJUSTMENT" in transaction_type
            or "CHARGEBACK" in transaction_type
        ):
            return "adjustment", self.payout_adjustment_account_id
        return "clearing", self.env["account.account"]

    def _upsert_payout_transaction(self, payout, normalized):
        currency = self._currency(normalized["currency"])
        order_id = shopify_gid("Order", normalized["order_id"])
        order_binding = self.env["shopify.order"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "=", order_id),
            ],
            limit=1,
        )
        route, account = self._transaction_route(normalized, order_binding)
        unmatched_reason = ""
        if order_id and not order_binding:
            unmatched_reason = self.env._("No order binding matches %s.", order_id)
        elif not account:
            unmatched_reason = self.env._(
                "No reconciliation account is available for %s.",
                (normalized["display_type"] or normalized["type"]),
            )
        values = {
            "instance_id": self.id,
            "payout_id": payout.id,
            "shopify_id": normalized["id"],
            "transaction_type": normalized["type"],
            "display_type": normalized["display_type"],
            "source_type": normalized["source_type"],
            "source_id": normalized["source_id"],
            "source_order_transaction_id": normalized["source_order_transaction_id"],
            "transaction_date": _utc_datetime(normalized["transaction_date"]),
            "currency_id": currency.id,
            "amount": normalized["amount"],
            "fee": normalized["fee"],
            "net": normalized["net"],
            "amount_exact": normalized["amount"],
            "fee_exact": normalized["fee"],
            "net_exact": normalized["net"],
            "order_binding_id": order_binding.id,
            "reconciliation_account_id": account.id,
            "route": route,
            "is_unmatched": bool(unmatched_reason),
            "unmatched_reason": unmatched_reason,
            "adjustment_reason": normalized["adjustment_reason"],
            "test": normalized["test"],
            "raw_payload": normalized["raw"],
        }
        transaction = self.env["shopify.payout.transaction"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "=", normalized["id"]),
            ],
            limit=1,
        )
        if transaction:
            transaction.write(values)
        else:
            transaction = self.env["shopify.payout.transaction"].create(values)
        return transaction

    def _import_disputes(self, date_from=False, date_to=False):
        account, payloads = self._payments_page(
            SHOPIFY_PAYMENTS_DISPUTES_QUERY,
            {"query": _date_query("initiated_at", date_from, date_to)},
            "disputes",
        )
        if not account:
            return
        for payload in payloads:
            self._upsert_dispute(normalize_dispute(payload))

    def _upsert_dispute(self, normalized):
        currency = self._currency(normalized["currency"])
        order_id = shopify_gid("Order", normalized["order_id"])
        order_binding = self.env["shopify.order"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "=", order_id),
            ],
            limit=1,
        )
        values = {
            "instance_id": self.id,
            "shopify_id": normalized["id"],
            "order_binding_id": order_binding.id,
            "currency_id": currency.id,
            "amount": normalized["amount"],
            "amount_exact": normalized["amount"],
            "dispute_status": normalized["status"],
            "dispute_type": normalized["type"],
            "reason": normalized["reason"],
            "network_reason_code": normalized["network_reason_code"],
            "initiated_at": _utc_datetime(normalized["initiated_at"]),
            "evidence_due_by": _utc_datetime(normalized["evidence_due_by"]),
            "evidence_sent_on": _utc_datetime(normalized["evidence_sent_on"]),
            "finalized_on": _utc_datetime(normalized["finalized_on"]),
            "raw_payload": normalized["raw"],
            "last_sync_date": fields.Datetime.now(),
            "state": "synced",
            "error_message": False,
        }
        dispute = self.env["shopify.dispute"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "=", normalized["id"]),
            ],
            limit=1,
        )
        if dispute:
            dispute.write(values)
        else:
            dispute = self.env["shopify.dispute"].create(values)
        if order_binding:
            summary = self.env._("Open Shopify Payments dispute %s", dispute.shopify_id)
            sale_order = order_binding.odoo_id
            activities = (
                sale_order.activity_ids.filtered(
                    lambda activity: activity.summary == summary
                )
                if sale_order
                else self.env["mail.activity"]
            )
            if (
                sale_order
                and normalized["status"] in OPEN_DISPUTE_STATES
                and not activities
            ):
                sale_order.activity_schedule(
                    "mail.mail_activity_data_todo",
                    summary=summary,
                    note=self.env._(
                        "Review the %(type)s dispute for %(amount)s "
                        "%(currency)s. Evidence due: %(due)s.",
                        type=normalized["type"],
                        amount=normalized["amount"],
                        currency=normalized["currency"],
                        due=normalized["evidence_due_by"] or "-",
                    ),
                )
            elif normalized["status"] not in OPEN_DISPUTE_STATES and activities:
                activities.action_done()
        return dispute


class ShopifyPayoutEntry(models.Model):
    _inherit = "shopify.payout"

    def _convert_exact(self, currency, amount, conversion_date):
        company = self.company_id
        if currency == company.currency_id:
            return decimal_amount(amount)
        converted = currency._convert(
            float(decimal_amount(amount)),
            company.currency_id,
            company,
            conversion_date,
            round=False,
        )
        return Decimal(str(converted))

    def _planning_accounts(self):
        instance = self.instance_id
        company = self.company_id
        return {
            "payout": instance.payout_journal_id.default_account_id.id,
            "fee": instance.payout_fee_account_id.id,
            "fx_gain": (
                instance.payout_currency_gain_account_id
                or company.income_currency_exchange_account_id
            ).id,
            "fx_loss": (
                instance.payout_currency_loss_account_id
                or company.expense_currency_exchange_account_id
            ).id,
        }

    def _job_generate_entry(self):
        self = self.sudo()
        self.ensure_one()
        instance = self.instance_id
        if not instance.active:
            return False
        if self.entry_id and self.entry_id.state == "posted":
            return self.entry_id.id
        if not instance.payout_journal_id:
            self._set_planning_error(
                MissingAccountMapping("Configure a payout journal.")
            )
            return False
        if not instance.payout_journal_id.default_account_id:
            self._set_planning_error(
                MissingAccountMapping("The payout journal has no default account.")
            )
            return False
        payout_date = fields.Date.to_date(self.issued_at) or fields.Date.today()
        transactions = []
        for transaction in self.transaction_ids:
            transaction_date = (
                fields.Date.to_date(transaction.transaction_date) or payout_date
            )
            transactions.append(
                {
                    "id": transaction.shopify_id,
                    "currency": transaction.currency_id.name,
                    "amount": transaction.amount_exact,
                    "fee": transaction.fee_exact,
                    "net": transaction.net_exact,
                    "route": transaction.route,
                    "account": transaction.reconciliation_account_id.id,
                    "name": transaction.display_type,
                    "type": transaction.transaction_type,
                    "company_amount": format(
                        self._convert_exact(
                            transaction.currency_id,
                            transaction.amount_exact,
                            transaction_date,
                        ),
                        "f",
                    ),
                    "company_fee": format(
                        self._convert_exact(
                            transaction.currency_id,
                            transaction.fee_exact,
                            transaction_date,
                        ),
                        "f",
                    ),
                }
            )
        payout_values = {
            "currency": self.currency_id.name,
            "net": self.net_exact,
            "reference": self.reference,
            "company_net": format(
                self._convert_exact(self.currency_id, self.net_exact, payout_date),
                "f",
            ),
        }
        try:
            plan = plan_payout_entry(
                payout_values,
                transactions,
                self._planning_accounts(),
                company_currency=self.company_id.currency_id.name,
                quantum=str(self.company_id.currency_id.rounding),
            )
        except (PayoutPlanningError, ShopifyError) as exc:
            self._set_planning_error(exc)
            return False
        old_entry = self.entry_id
        if old_entry and old_entry.state == "draft":
            self.entry_id = False
            old_entry.unlink()
        line_commands = []
        for line in plan["lines"]:
            values = {
                "name": line["name"],
                "account_id": line["account"],
                # Exact Decimals are validated in the plan; Odoo monetary
                # fields require float values at the ORM boundary.
                "debit": float(Decimal(line["debit"])),
                "credit": float(Decimal(line["credit"])),
            }
            if line["currency"] != self.company_id.currency_id.name:
                values.update(
                    {
                        "currency_id": self.currency_id.id,
                        "amount_currency": float(Decimal(line["amount_currency"])),
                    }
                )
            line_commands.append(Command.create(values))
        entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": instance.payout_journal_id.id,
                "company_id": self.company_id.id,
                "date": payout_date,
                "ref": self.env._(
                    "%(reference)s / %(date)s",
                    reference=self.reference,
                    date=payout_date,
                ),
                "line_ids": line_commands,
            }
        )
        self.write(
            {
                "entry_id": entry.id,
                "state": "synced",
                "error_message": False,
            }
        )
        if instance.payout_auto_post:
            entry.action_post()
        instance._write_log(
            entity="payout",
            direction="import",
            level="info",
            message=self.env._(
                "Generated payout journal entry %s.", entry.display_name
            ),
            record=self,
        )
        return entry.id

    def _set_planning_error(self, error):
        self.write({"state": "error", "error_message": str(error)})
        self.instance_id._write_log(
            entity="payout",
            direction="import",
            level="error",
            message=self.env._("Payout entry generation failed: %s", error),
            record=self,
        )
