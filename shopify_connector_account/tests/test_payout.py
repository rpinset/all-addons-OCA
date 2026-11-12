from unittest.mock import Mock, patch

from odoo import SUPERUSER_ID
from odoo.fields import Command

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.shopify_connector.models.order_sync import ShopifyOrderImportError


class TestShopifyPayoutAccounting(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = (
            cls.env["base"]
            .with_user(SUPERUSER_ID)
            .with_company(cls.company_data["company"])
            .env
        )
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Payments Shop",
                "shop_url": "payments-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.company = cls.instance.company_id
        cls.currency = cls.company.currency_id
        cls.journal = cls.company_data["default_journal_bank"]
        cls.expense_account = cls.company_data["default_account_expense"]
        if not cls.expense_account:
            cls.expense_account = cls._account(
                "Shopify Test Expense", "SHOPEXP", "expense"
            )
        if not cls.journal:
            cls.clearing_account = cls._account(
                "Shopify Test Clearing", "SHOPCLR", "asset_current"
            )
            cls.journal = cls.env["account.journal"].create(
                {
                    "name": "Shopify Test Bank",
                    "code": "SHBK",
                    "type": "bank",
                    "company_id": cls.company.id,
                    "default_account_id": cls.clearing_account.id,
                }
            )
        else:
            cls.clearing_account = cls.journal.default_account_id
        cls.liability_account = cls._account(
            "Shopify Gift Card Liability", "SHOPGFT", "liability_current"
        )
        cls.instance.write(
            {
                "payout_journal_id": cls.journal.id,
                "payout_fee_account_id": cls.expense_account.id,
                "payout_adjustment_account_id": cls.expense_account.id,
            }
        )

    @classmethod
    def _account(cls, name, code, account_type):
        return cls.env["account.account"].create(
            {
                "name": name,
                "code": code,
                "account_type": account_type,
                "company_ids": [Command.set(cls.company.ids)],
            }
        )

    def _payout(self, payout_id, net="97.00"):
        return self.env["shopify.payout"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": (f"gid://shopify/ShopifyPaymentsPayout/{payout_id}"),
                "reference": f"PAYOUT-{payout_id}",
                "legacy_resource_id": str(payout_id),
                "issued_at": "2026-07-20 00:00:00",
                "payout_status": "PAID",
                "currency_id": self.currency.id,
                "gross_amount": "100.00",
                "fee_amount": "3.00",
                "net_amount": net,
                "gross_exact": "100.00",
                "fee_exact": "3.00",
                "net_exact": net,
                "state": "synced",
            }
        )

    def _transaction(self, payout, transaction_id="1", net="97.00"):
        return self.env["shopify.payout.transaction"].create(
            {
                "instance_id": self.instance.id,
                "payout_id": payout.id,
                "shopify_id": (
                    f"gid://shopify/ShopifyPaymentsBalanceTransaction/{transaction_id}"
                ),
                "transaction_type": "CHARGE",
                "display_type": "Charge",
                "source_type": "CHARGE",
                "transaction_date": "2026-07-19 00:00:00",
                "currency_id": self.currency.id,
                "amount": "100.00",
                "fee": "3.00",
                "net": net,
                "amount_exact": "100.00",
                "fee_exact": "3.00",
                "net_exact": net,
                "reconciliation_account_id": (self.journal.default_account_id.id),
                "route": "clearing",
            }
        )

    def test_entry_generation_is_balanced_and_draft(self):
        payout = self._payout(701)
        self._transaction(payout)

        entry_id = payout._job_generate_entry()
        entry = self.env["account.move"].browse(entry_id)

        self.assertEqual(entry.state, "draft")
        self.assertEqual(entry.ref, "PAYOUT-701 / 2026-07-20")
        self.assertEqual(sum(entry.line_ids.mapped("balance")), 0)

    def test_draft_regeneration_replaces_instead_of_duplicates(self):
        payout = self._payout(702)
        self._transaction(payout, transaction_id="2")
        first_id = payout._job_generate_entry()

        second_id = payout._job_generate_entry()

        self.assertNotEqual(first_id, second_id)
        self.assertFalse(self.env["account.move"].browse(first_id).exists())
        self.assertEqual(
            self.env["account.move"].search_count([("id", "=", second_id)]),
            1,
        )

    def test_mismatch_marks_payout_error_without_entry(self):
        payout = self._payout(703, net="98.00")
        self._transaction(payout, transaction_id="3", net="97.00")

        result = payout._job_generate_entry()

        self.assertFalse(result)
        self.assertEqual(payout.state, "error")
        self.assertFalse(payout.entry_id)
        self.assertIn("does not equal", payout.error_message)

    def test_open_dispute_creates_order_activity(self):
        sale = self.env["sale.order"].create(
            {
                "partner_id": self.company.partner_id.id,
                "company_id": self.company.id,
            }
        )
        order_binding = self.env["shopify.order"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Order/704",
                "odoo_id": sale.id,
                "order_name": "#704",
                "state": "synced",
            }
        )

        dispute = self.instance._upsert_dispute(
            {
                "id": "gid://shopify/ShopifyPaymentsDispute/705",
                "order_id": order_binding.shopify_id,
                "amount": "25.00",
                "currency": self.currency.name,
                "status": "NEEDS_RESPONSE",
                "type": "CHARGEBACK",
                "reason": "FRAUDULENT",
                "network_reason_code": "4827",
                "initiated_at": "2026-07-20T00:00:00Z",
                "evidence_due_by": "2026-07-30T00:00:00Z",
                "evidence_sent_on": None,
                "finalized_on": None,
                "raw": {},
            }
        )

        self.assertEqual(dispute.order_binding_id, order_binding)
        self.assertTrue(
            sale.activity_ids.filtered(
                lambda activity: dispute.shopify_id in activity.summary
            )
        )

        closed = self.instance._upsert_dispute(
            {
                "id": dispute.shopify_id,
                "order_id": order_binding.shopify_id,
                "amount": "25.00",
                "currency": self.currency.name,
                "status": "WON",
                "type": "CHARGEBACK",
                "reason": "FRAUDULENT",
                "network_reason_code": "4827",
                "initiated_at": "2026-07-20T00:00:00Z",
                "evidence_due_by": "2026-07-30T00:00:00Z",
                "evidence_sent_on": "2026-07-25T00:00:00Z",
                "finalized_on": "2026-07-26T00:00:00Z",
                "raw": {"status": "WON"},
            }
        )

        self.assertEqual(closed, dispute)
        self.assertEqual(closed.dispute_status, "WON")
        self.assertFalse(
            sale.activity_ids.filtered(
                lambda activity: dispute.shopify_id in activity.summary
            )
        )

    def test_daily_import_updates_an_open_dispute_older_than_its_window(self):
        dispute = self.instance._upsert_dispute(
            {
                "id": "gid://shopify/ShopifyPaymentsDispute/707",
                "order_id": "gid://shopify/Order/708",
                "amount": "25.00",
                "currency": self.currency.name,
                "status": "NEEDS_RESPONSE",
                "type": "CHARGEBACK",
                "reason": "FRAUDULENT",
                "network_reason_code": "4827",
                "initiated_at": "2026-07-20T00:00:00Z",
                "evidence_due_by": "2026-07-30T00:00:00Z",
                "evidence_sent_on": None,
                "finalized_on": None,
                "raw": {},
            }
        )
        won = {
            "id": dispute.shopify_id,
            "initiatedAt": "2026-07-20T00:00:00Z",
            "finalizedOn": "2026-08-25",
            "status": "WON",
            "type": "CHARGEBACK",
            "amount": {"amount": "25.00", "currencyCode": self.currency.name},
            "order": {"id": "gid://shopify/Order/708"},
        }

        def payments_page(instance, query, variables, connection):
            # Shopify filters disputes on the day they were opened.
            date_from = variables["query"].split()[0].split(">=")[1]
            return {"activated": True}, [won] if date_from <= "2026-07-20" else []

        with patch.object(type(self.instance), "_payments_page", autospec=True) as page:
            page.side_effect = payments_page
            self.instance._import_disputes("2026-08-20", "2026-08-27")

        self.assertEqual(dispute.dispute_status, "WON")

    def test_dispute_import_starts_a_day_before_the_oldest_open_dispute(self):
        # Opened just after midnight UTC: still the day before in a shop
        # west of UTC.
        self.instance._upsert_dispute(
            {
                "id": "gid://shopify/ShopifyPaymentsDispute/709",
                "order_id": "gid://shopify/Order/710",
                "amount": "25.00",
                "currency": self.currency.name,
                "status": "UNDER_REVIEW",
                "type": "CHARGEBACK",
                "reason": "FRAUDULENT",
                "network_reason_code": "4827",
                "initiated_at": "2026-07-20T00:30:00Z",
                "evidence_due_by": None,
                "evidence_sent_on": None,
                "finalized_on": None,
                "raw": {},
            }
        )

        with patch.object(type(self.instance), "_payments_page", autospec=True) as page:
            page.return_value = ({"activated": True}, [])
            self.instance._import_disputes("2026-08-20", "2026-08-27")

        self.assertEqual(
            page.call_args.args[2],
            {"query": "initiated_at:>=2026-07-19 initiated_at:<=2026-08-27"},
        )

    def test_entry_planning_boundaries_preserve_error_state(self):
        payout = self._payout(706)

        self.instance.payout_journal_id = False
        self.assertFalse(payout._job_generate_entry())
        self.assertEqual(payout.state, "error")
        self.assertIn("Configure a payout journal", payout.error_message)

        self.instance.payout_journal_id = self.journal
        self._transaction(payout, transaction_id="missing-account").write(
            {"reconciliation_account_id": False}
        )
        self.assertFalse(payout._job_generate_entry())
        self.assertIn("No account mapping", payout.error_message)
        self.assertFalse(payout.entry_id)

    def test_inactive_instance_and_posted_entry_are_idempotent_boundaries(self):
        payout = self._payout(707)
        self.instance.active = False
        self.assertFalse(payout._job_generate_entry())

        self.instance.active = True
        self._transaction(payout, transaction_id="posted")
        entry = self.env["account.move"].browse(payout._job_generate_entry())
        entry.action_post()
        self.assertEqual(payout._job_generate_entry(), entry.id)
        self.assertEqual(payout.entry_id, entry)

    def test_reimport_keeps_the_entry_error_of_a_payout(self):
        payout = self._payout(708, net="98.00")
        self._transaction(payout, transaction_id="8", net="97.00")
        self.assertFalse(payout._job_generate_entry())
        error = payout.error_message

        self.instance._upsert_payout(
            {
                "id": payout.shopify_id,
                "legacy_id": "708",
                "reference": "PAYOUT-708",
                "issued_at": "2026-07-20T00:00:00Z",
                "status": "PAID",
                "transaction_type": "DEPOSIT",
                "currency": self.currency.name,
                "gross": "100.00",
                "fees": "3.00",
                "net": "98.00",
                "summary": {},
                "raw": {},
            }
        )

        self.assertEqual(payout.state, "error")
        self.assertEqual(payout.error_message, error)

    def _balance_payload(self, payout, transaction_id, net="97.00"):
        def money(amount):
            return {"amount": amount, "currencyCode": self.currency.name}

        return {
            "id": (f"gid://shopify/ShopifyPaymentsBalanceTransaction/{transaction_id}"),
            "type": "CHARGE",
            "displayType": "Charge",
            "sourceType": "CHARGE",
            "associatedPayout": {"id": payout.shopify_id},
            "associatedOrder": {},
            "transactionDate": "2026-07-19T00:00:00Z",
            "amount": money("100.00"),
            "fee": money("3.00"),
            "net": money(net),
            "test": False,
        }

    def _import_transactions(self, payout, payloads):
        with patch.object(
            type(self.instance),
            "_payments_page",
            autospec=True,
            return_value=({"activated": True}, payloads),
        ):
            self.instance._import_payout_transactions(payout)

    def test_posted_entry_keeps_its_transactions_and_flags_changes(self):
        payout = self._payout(709)
        transaction = self._transaction(payout, transaction_id="9")
        entry = self.env["account.move"].browse(payout._job_generate_entry())
        entry.action_post()

        # Shopify reports the same transactions: nothing to flag.
        self._import_transactions(payout, [self._balance_payload(payout, "9")])
        self.assertEqual(payout.state, "synced")

        # Shopify replaced the transaction after the entry was posted.
        changed = [
            self._balance_payload(payout, "9", net="96.00"),
            self._balance_payload(payout, "10"),
        ]
        self._import_transactions(payout, changed)
        logs = self.env["shopify.log"].search(
            [("res_model", "=", payout._name), ("res_id", "=", payout.id)]
        )
        self.assertIn(payout.error_message, logs.mapped("message"))

        # The next import finds the same change: no new log entry.
        self._import_transactions(payout, changed)
        self.assertEqual(
            self.env["shopify.log"].search(
                [("res_model", "=", payout._name), ("res_id", "=", payout.id)]
            ),
            logs,
        )

        self.assertEqual(payout.transaction_ids, transaction)
        self.assertEqual(transaction.net_exact, "97.00")
        self.assertEqual(payout.state, "error")
        self.assertIn("1 added, 0 removed, 1 changed", payout.error_message)
        self.assertEqual(payout.entry_id, entry)
        self.assertEqual(entry.state, "posted")

    def _gift_card_payment(self, *, with_clearing=True):
        lines = []
        if with_clearing:
            lines = [
                Command.create(
                    {
                        "name": "Gift card clearing",
                        "account_id": self.clearing_account.id,
                        "debit": 25,
                    }
                ),
                Command.create(
                    {
                        "name": "Gift card counterline",
                        "account_id": self.expense_account.id,
                        "credit": 25,
                    }
                ),
            ]
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": self.journal.id,
                "company_id": self.company.id,
                "line_ids": lines,
            }
        )
        return Mock(
            move_id=move,
            journal_id=self.journal,
            date=False,
        )

    def _gateway_payment(self, payment, gateway="gift_card"):
        return Mock(
            gateway=gateway,
            gift_card_move_id=False,
            instance_id=self.instance,
            payment_id=payment,
            transaction_shopify_id="gid://shopify/OrderTransaction/gift-1",
        )

    def test_gift_card_reclassification_rejects_invalid_boundaries(self):
        payment = self._gift_card_payment()
        ordinary = self._gateway_payment(payment, gateway="card")
        self.env["shopify.order"]._after_shopify_gateway_payment(
            ordinary, {}, self.env["account.move"]
        )
        self.assertFalse(ordinary.gift_card_move_id)

        gift_card = self._gateway_payment(payment)
        with self.assertRaisesRegex(ShopifyOrderImportError, "liability account"):
            self.env["shopify.order"]._after_shopify_gateway_payment(
                gift_card, {}, self.env["account.move"]
            )

        product = self.env["product.product"].create(
            {
                "name": "Shopify Gift Card",
                "company_id": self.company.id,
                "property_account_income_id": self.liability_account.id,
            }
        )
        self.instance.gift_card_product_id = product
        no_clearing = self._gateway_payment(
            self._gift_card_payment(with_clearing=False)
        )
        with self.assertRaisesRegex(ShopifyOrderImportError, "no clearing line"):
            self.env["shopify.order"]._after_shopify_gateway_payment(
                no_clearing, {}, self.env["account.move"]
            )

    def test_gift_card_reclassification_creates_balanced_draft_once(self):
        product = self.env["product.product"].create(
            {
                "name": "Shopify Gift Card",
                "company_id": self.company.id,
                "property_account_income_id": self.liability_account.id,
            }
        )
        self.instance.gift_card_product_id = product
        gateway_payment = self._gateway_payment(self._gift_card_payment())

        with patch.object(
            type(self.instance), "_write_log", autospec=True
        ) as write_log:
            result = self.env["shopify.order"]._after_shopify_gateway_payment(
                gateway_payment, {}, self.env["account.move"]
            )

        move = gateway_payment.gift_card_move_id
        self.assertFalse(result)
        self.assertEqual(move.state, "draft")
        self.assertEqual(sum(move.line_ids.mapped("balance")), 0)
        self.assertEqual(
            set(move.line_ids.account_id.ids),
            set((self.liability_account | self.clearing_account).ids),
        )
        write_log.assert_called_once()

        existing = move
        self.env["shopify.order"]._after_shopify_gateway_payment(
            gateway_payment, {}, self.env["account.move"]
        )
        self.assertEqual(gateway_payment.gift_card_move_id, existing)
