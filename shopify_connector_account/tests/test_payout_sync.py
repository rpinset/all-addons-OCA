from datetime import date
from unittest.mock import Mock, patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.client import ShopifyUserError
from odoo.addons.shopify_connector_account.lib.payout import (
    PayoutPlanningError,
    normalize_payout,
)
from odoo.addons.shopify_connector_account.models.payout_sync import (
    _date_query,
    _utc_datetime,
)


class TestShopifyPayoutSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Payout Sync Shop",
                "shop_url": "payout-sync.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.currency = cls.instance.company_id.currency_id

    def _payout(self, payout_id="sync-1", legacy_id="101"):
        return self.instance._upsert_payout(
            {
                "id": f"gid://shopify/ShopifyPaymentsPayout/{payout_id}",
                "legacy_id": legacy_id,
                "reference": f"PAYOUT-{payout_id}",
                "issued_at": "2026-07-20T04:00:00+04:00",
                "status": "PAID",
                "transaction_type": "DEPOSIT",
                "currency": self.currency.name,
                "gross": "100.00",
                "fees": "3.00",
                "net": "97.00",
                "summary": {},
                "raw": {"id": payout_id},
            }
        )

    def _transaction_payload(self, transaction_id, payout, **overrides):
        values = {
            "id": f"gid://shopify/ShopifyPaymentsBalanceTransaction/{transaction_id}",
            "type": "ADJUSTMENT",
            "displayType": "Adjustment",
            "sourceType": "ADJUSTMENT",
            "sourceId": "source-1",
            "sourceOrderTransactionId": "",
            "associatedPayout": {"id": payout.shopify_id},
            "associatedOrder": {},
            "transactionDate": "2026-07-19T00:00:00Z",
            "amount": {"amount": "10.00", "currencyCode": self.currency.name},
            "fee": {"amount": "0.00", "currencyCode": self.currency.name},
            "net": {"amount": "10.00", "currencyCode": self.currency.name},
            "adjustmentReason": "RESERVE",
            "test": False,
        }
        values.update(overrides)
        return values

    def test_date_and_datetime_boundaries_are_canonical(self):
        self.assertFalse(_utc_datetime(False))
        self.assertEqual(
            _utc_datetime("2026-07-20T04:00:00+04:00").isoformat(),
            "2026-07-20T00:00:00",
        )
        self.assertEqual(
            _date_query("issued_at", date(2026, 7, 1), date(2026, 7, 31)),
            "issued_at:>=2026-07-01 issued_at:<=2026-07-31",
        )
        self.assertIsNone(_date_query("issued_at"))

    def test_payments_page_paginates_and_handles_missing_account(self):
        client = Mock()
        client.execute.side_effect = [
            {
                "shopifyPaymentsAccount": {
                    "payouts": {
                        "nodes": [{"id": "payout-1"}],
                        "pageInfo": {"hasNextPage": True, "endCursor": "next"},
                    }
                }
            },
            {
                "shopifyPaymentsAccount": {
                    "payouts": {
                        "nodes": [{"id": "payout-2"}],
                        "pageInfo": {"hasNextPage": False},
                    }
                }
            },
        ]
        with patch.object(
            type(self.instance), "_shopify_client", autospec=True, return_value=client
        ):
            account, records = self.instance._payments_page(
                "query", {"query": "issued_at:>=2026-07-01"}, "payouts"
            )

        self.assertTrue(account)
        self.assertEqual([item["id"] for item in records], ["payout-1", "payout-2"])
        self.assertEqual(client.execute.call_args_list[1].args[1]["after"], "next")

        client.execute.return_value = {"shopifyPaymentsAccount": None}
        client.execute.side_effect = None
        with patch.object(
            type(self.instance), "_shopify_client", autospec=True, return_value=client
        ):
            self.assertEqual(
                self.instance._payments_page("query", {}, "payouts"), (None, [])
            )

    def test_import_payouts_handles_availability_and_upserts(self):
        self.instance.active = False
        self.assertEqual(self.instance._job_import_payouts(), [])
        self.instance.active = True

        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            side_effect=ShopifyUserError("payments denied"),
        ):
            self.assertEqual(self.instance._job_import_payouts(), [])
        self.assertEqual(self.instance.shopify_payments_state, "unavailable")

        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=({"activated": False}, []),
        ):
            self.assertEqual(self.instance._job_import_payouts(), [])
        self.assertEqual(self.instance.shopify_payments_state, "unavailable")

        payload = {
            "id": "gid://shopify/ShopifyPaymentsPayout/202",
            "legacyResourceId": "202",
            "externalTraceId": "PAYOUT-202",
            "issuedAt": "2026-07-20T00:00:00Z",
            "status": "PAID",
            "transactionType": "DEPOSIT",
            "net": {"amount": "97.00", "currencyCode": self.currency.name},
            "summary": {
                "chargesGross": {
                    "amount": "100.00",
                    "currencyCode": self.currency.name,
                },
                "chargesFees": {
                    "amount": "3.00",
                    "currencyCode": self.currency.name,
                },
            },
        }
        with (
            patch.object(
                type(self.instance),
                "_payments_page",
                autospec=True,
                return_value=({"activated": True}, [payload]),
            ),
            patch.object(
                type(self.instance), "_import_payout_transactions", autospec=True
            ) as import_transactions,
            patch.object(
                type(self.instance),
                "_import_disputes",
                autospec=True,
                side_effect=ShopifyUserError("disputes denied"),
            ),
        ):
            payout_ids = self.instance._job_import_payouts("2026-07-01", "2026-07-31")

        payout = self.env["shopify.payout"].browse(payout_ids)
        self.assertEqual(payout.reference, "PAYOUT-202")
        self.assertEqual(payout.net_exact, "97.00")
        self.assertEqual(self.instance.shopify_payments_state, "enabled")
        import_transactions.assert_called_once_with(self.instance, payout)

        updated_values = normalize_payout(payload | {"status": "SCHEDULED"})
        updated = self.instance._upsert_payout(updated_values)
        self.assertEqual(updated, payout)
        self.assertEqual(updated.payout_status, "SCHEDULED")

    def test_currency_and_payout_identity_errors_are_typed(self):
        with self.assertRaisesRegex(PayoutPlanningError, "no currency record"):
            self.instance._currency("ZZZ")
        with self.assertRaisesRegex(PayoutPlanningError, "without an ID"):
            self.instance._upsert_payout(
                {
                    "id": "",
                    "currency": self.currency.name,
                }
            )

    def test_transaction_import_filters_foreign_and_removes_stale_rows(self):
        payout = self._payout()
        stale = self.env["shopify.payout.transaction"].create(
            {
                "instance_id": self.instance.id,
                "payout_id": payout.id,
                "shopify_id": "gid://shopify/ShopifyPaymentsBalanceTransaction/stale",
                "currency_id": self.currency.id,
                "amount_exact": "1.00",
                "fee_exact": "0.00",
                "net_exact": "1.00",
            }
        )
        foreign = self._transaction_payload(
            "foreign",
            payout,
            associatedPayout={"id": "gid://shopify/ShopifyPaymentsPayout/other"},
        )
        matching = self._transaction_payload("matching", payout)
        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=({"activated": True}, [foreign, matching]),
        ):
            self.instance._import_payout_transactions(payout)

        self.assertFalse(stale.exists())
        transaction = payout.transaction_ids
        self.assertEqual(len(transaction), 1)
        self.assertEqual(transaction.route, "adjustment")
        self.assertTrue(transaction.is_unmatched)
        self.assertIn("No reconciliation account", transaction.unmatched_reason)

        changed = self._transaction_payload(
            "matching", payout, displayType="Reserve adjustment"
        )
        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=({"activated": True}, [changed]),
        ):
            self.instance._import_payout_transactions(payout)
        self.assertEqual(payout.transaction_ids, transaction)
        self.assertEqual(transaction.display_type, "Reserve adjustment")

        payout.legacy_resource_id = False
        with self.assertRaisesRegex(PayoutPlanningError, "has no legacy ID"):
            self.instance._import_payout_transactions(payout)

        payout.legacy_resource_id = "101"
        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=(None, []),
        ):
            self.assertFalse(self.instance._import_payout_transactions(payout))

    def test_dispute_import_and_queue_operations_are_behavioral(self):
        dispute_payload = {
            "id": "gid://shopify/ShopifyPaymentsDispute/303",
            "order": None,
            "amount": {"amount": "12.00", "currencyCode": self.currency.name},
            "status": "UNDER_REVIEW",
            "type": "CHARGEBACK",
            "reasonDetails": {
                "reason": "FRAUDULENT",
                "networkReasonCode": "4827",
            },
            "initiatedAt": "2026-07-20T00:00:00Z",
            "evidenceDueBy": "2026-07-30T00:00:00Z",
            "evidenceSentOn": None,
            "finalizedOn": None,
        }
        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=({"activated": True}, [dispute_payload]),
        ):
            self.instance._import_disputes("2026-07-01", "2026-07-31")
        dispute = self.instance.dispute_ids
        self.assertEqual(dispute.dispute_status, "UNDER_REVIEW")
        self.assertFalse(dispute.order_binding_id)

        delayed = Mock()
        with patch.object(
            type(self.instance), "with_delay", autospec=True, return_value=delayed
        ):
            self.assertTrue(dispute._shopify_enqueue_fresh_retry())
            dispute.write({"state": "error", "error_message": "retry me"})
            dispute.action_retry_sync()
        self.assertEqual(dispute.state, "pending")
        self.assertFalse(dispute.error_message)
        self.assertEqual(delayed._job_import_payouts.call_count, 2)

        self.instance.active = False
        self.assertFalse(dispute._shopify_enqueue_fresh_retry())

    def test_cron_manual_action_and_payout_retry_enqueue_exact_jobs(self):
        payout = self._payout("queue", "404")
        delayed = Mock()
        instance_model = type(self.instance)
        payout_model = type(payout)
        with (
            patch.object(
                instance_model, "search", autospec=True, return_value=self.instance
            ),
            patch.object(
                instance_model, "with_delay", autospec=True, return_value=delayed
            ) as with_delay,
            patch.object(
                payout_model, "with_delay", autospec=True, return_value=delayed
            ),
        ):
            self.env["shopify.instance"]._cron_import_shopify_payouts()
            self.assertTrue(payout.action_generate_entry())
            self.assertTrue(payout._shopify_enqueue_fresh_retry())

        self.assertEqual(delayed._job_import_payouts.call_count, 2)
        delayed._job_generate_entry.assert_called_once()
        self.assertIn(
            "shopify.payouts.daily", with_delay.call_args_list[0].kwargs["identity_key"]
        )

        self.instance.write(
            {
                "payout_import_date_from": "2026-07-31",
                "payout_import_date_to": "2026-07-01",
            }
        )
        with self.assertRaisesRegex(ValidationError, "must precede"):
            self.instance.action_import_payouts()

        self.instance.write(
            {
                "payout_import_date_from": "2026-07-01",
                "payout_import_date_to": "2026-07-31",
            }
        )
        delayed.reset_mock()
        with patch.object(
            instance_model, "with_delay", autospec=True, return_value=delayed
        ):
            self.assertTrue(self.instance.action_import_payouts())
        delayed._job_import_payouts.assert_called_once_with("2026-07-01", "2026-07-31")
