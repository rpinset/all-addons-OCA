from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from freezegun import freeze_time

from odoo import SUPERUSER_ID
from odoo.sql_db import db_connect

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.queue_job.exception import RetryableJobError
from odoo.addons.queue_job.tests.common import trap_jobs
from odoo.addons.shopify_connector.graphql.order import orders_updated_search
from odoo.addons.shopify_connector.lib.client import ShopifyError


class TestShopifyOrderSync(AccountTestInvoicingCommon):
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
                "name": "Order Shop",
                "shop_url": "order-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
                "unknown_product_policy": "block",
            }
        )
        cls.instance.state = "connected"
        cls.currency = cls.instance.company_id.currency_id
        cls.bank_journal = cls.company_data["default_journal_bank"]
        cls.sale_journal = cls.company_data["default_journal_sale"]
        cls.product = cls.env["product.product"].create(
            {
                "name": "Bound Order Product",
                "type": "service",
                "company_id": cls.instance.company_id.id,
            }
        )
        cls.template_binding = cls.env["shopify.product.template"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Product/10",
                "odoo_id": cls.product.product_tmpl_id.id,
                "status": "ACTIVE",
            }
        )
        cls.variant_binding = cls.env["shopify.product.variant"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/ProductVariant/20",
                "template_binding_id": cls.template_binding.id,
                "odoo_id": cls.product.id,
            }
        )
        cls.order_model = cls.env["shopify.order"]

    def _bag(self, amount):
        return {
            "shopMoney": {
                "amount": amount,
                "currencyCode": self.currency.name,
            },
            "presentmentMoney": {
                "amount": amount,
                "currencyCode": self.currency.name,
            },
        }

    def _payload(self, order_id=1, quantity=1, total="10.00", **values):
        payload = {
            "id": f"gid://shopify/Order/{order_id}",
            "name": f"#{order_id}",
            "createdAt": "2026-01-10T10:00:00Z",
            "updatedAt": "2026-01-10T10:00:00Z",
            "currencyCode": self.currency.name,
            "presentmentCurrencyCode": self.currency.name,
            "displayFinancialStatus": "PENDING",
            "displayFulfillmentStatus": "UNFULFILLED",
            "currentSubtotalPriceSet": self._bag(total),
            "currentTotalDiscountsSet": self._bag("0.00"),
            "currentShippingPriceSet": self._bag("0.00"),
            "currentTotalTaxSet": self._bag("0.00"),
            "currentTotalPriceSet": self._bag(total),
            "lineItems": {
                "nodes": [
                    {
                        "id": "gid://shopify/LineItem/30",
                        "name": "Bound Order Product",
                        "sku": "ORDER-1",
                        "quantity": quantity,
                        "currentQuantity": quantity,
                        "refundableQuantity": quantity,
                        "variant": {"id": self.variant_binding.shopify_id},
                        "product": {"id": self.template_binding.shopify_id},
                        "originalUnitPriceSet": self._bag("10.00"),
                        "discountedUnitPriceAfterAllDiscountsSet": self._bag("10.00"),
                        "taxLines": [],
                        "discountAllocations": [],
                    }
                ]
            },
            "shippingLines": {"nodes": []},
            "transactions": [],
            "refunds": {"nodes": []},
            "tags": ["web"],
            "discountCodes": [],
        }
        payload.update(values)
        return payload

    def _cancelled_payload(self, order_id, **values):
        """Return an order as Shopify sends it after a cancellation.

        Shopify keeps the ordered quantity but sets the current quantity of
        every line, and the current totals, to 0.
        """
        payload = self._payload(
            order_id=order_id,
            total="0.00",
            cancelledAt="2026-01-12T10:00:00Z",
            updatedAt="2026-01-12T10:00:00Z",
            **values,
        )
        for line in payload["lineItems"]["nodes"]:
            line["currentQuantity"] = 0
            line["refundableQuantity"] = 0
        return payload

    def test_order_build_and_edit_are_idempotent(self):
        binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload()
        )
        binding = self.order_model.browse(binding_id)

        self.assertEqual(binding.odoo_id.amount_total, 10)
        self.assertEqual(len(binding.line_binding_ids), 1)

        self.order_model._job_import_order(
            self.instance.id,
            self._payload(
                quantity=2,
                total="20.00",
                updatedAt="2026-01-11T10:00:00Z",
            ),
        )
        self.order_model._job_import_order(
            self.instance.id,
            self._payload(
                quantity=2,
                total="20.00",
                updatedAt="2026-01-11T10:00:00Z",
            ),
        )

        self.assertEqual(binding.odoo_id.order_line.product_uom_qty, 2)
        self.assertEqual(len(binding.line_binding_ids), 1)

    def test_order_imports_its_customer(self):
        payload = self._payload(order_id=14)
        payload["customer"] = {"id": "gid://shopify/Customer/140"}
        client = Mock()
        client.execute.return_value = {
            "customer": {
                "id": "gid://shopify/Customer/140",
                "firstName": "Order",
                "lastName": "Buyer",
                "defaultEmailAddress": {"emailAddress": "order.buyer@example.com"},
            }
        }

        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            binding_id = self.order_model._job_import_order(self.instance.id, payload)

        partner = self.order_model.browse(binding_id).odoo_id.partner_id
        self.assertNotEqual(partner, self.instance.guest_partner_id)
        self.assertEqual(partner.email, "order.buyer@example.com")
        self.assertEqual(
            partner.shopify_customer_binding_ids.shopify_id,
            "gid://shopify/Customer/140",
        )

    def _address(self, street, city="Veendam", zip_code="9641 AA", **values):
        return {
            "firstName": "Anna",
            "lastName": "de Vries",
            "company": None,
            "address1": street,
            "address2": None,
            "city": city,
            "provinceCode": None,
            "countryCodeV2": "NL",
            "zip": zip_code,
            "phone": "+31612345678",
            **values,
        }

    def test_order_imports_its_delivery_and_invoice_address(self):
        payload = self._payload(
            order_id=15,
            shippingAddress=self._address("Leveringsweg 2"),
            billingAddress=self._address("Factuurstraat 1", city="Groningen"),
        )

        binding_id = self.order_model._job_import_order(self.instance.id, payload)

        order = self.order_model.browse(binding_id).odoo_id
        shipping = order.partner_shipping_id
        invoice = order.partner_invoice_id
        self.assertEqual(shipping.parent_id, order.partner_id)
        self.assertEqual(shipping.type, "delivery")
        self.assertEqual(shipping.name, "Anna de Vries")
        self.assertEqual(shipping.street, "Leveringsweg 2")
        self.assertEqual(shipping.zip, "9641 AA")
        self.assertEqual(shipping.city, "Veendam")
        self.assertEqual(shipping.country_id.code, "NL")
        self.assertEqual(shipping.phone, "+31612345678")
        self.assertEqual(invoice.type, "invoice")
        self.assertEqual(invoice.street, "Factuurstraat 1")
        self.assertEqual(invoice.city, "Groningen")

    def test_reimported_order_reuses_its_address_contacts(self):
        values = {
            "shippingAddress": self._address("Leveringsweg 2"),
            "billingAddress": self._address("Leveringsweg 2"),
        }
        binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=16, **values)
        )
        order = self.order_model.browse(binding_id).odoo_id
        contacts = order.partner_id.child_ids

        self.order_model._job_import_order(
            self.instance.id,
            self._payload(
                order_id=16,
                quantity=2,
                total="20.00",
                updatedAt="2026-01-11T10:00:00Z",
                **values,
            ),
        )

        self.assertEqual(order.partner_id.child_ids, contacts)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(order.partner_shipping_id, contacts)
        self.assertEqual(order.partner_invoice_id, contacts)

    def test_shipping_address_edited_in_shopify_reaches_the_order(self):
        binding_id = self.order_model._job_import_order(
            self.instance.id,
            self._payload(order_id=17, shippingAddress=self._address("Oud 1")),
        )
        order = self.order_model.browse(binding_id).odoo_id

        self.order_model._job_import_order(
            self.instance.id,
            self._payload(
                order_id=17,
                updatedAt="2026-01-11T10:00:00Z",
                shippingAddress=self._address("Nieuw 9"),
            ),
        )

        self.assertEqual(order.partner_shipping_id.street, "Nieuw 9")

    def test_order_without_address_ships_to_the_customer(self):
        binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=18)
        )

        order = self.order_model.browse(binding_id).odoo_id
        self.assertEqual(order.partner_shipping_id, order.partner_id)
        self.assertEqual(order.partner_invoice_id, order.partner_id)

    def test_total_verification_failure_leaves_no_sale_order(self):
        before = self.env["sale.order"].search_count([])

        result = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=2, total="10.01")
        )

        binding = self.order_model.search(
            [
                ("instance_id", "=", self.instance.id),
                ("shopify_id", "=", "gid://shopify/Order/2"),
            ]
        )
        self.assertFalse(result)
        self.assertEqual(binding.state, "error")
        self.assertFalse(binding.odoo_id)
        self.assertEqual(self.env["sale.order"].search_count([]), before)

    def test_fixed_discount_over_several_units_matches_shopify_total(self):
        payload = self._payload(order_id=30, quantity=3, total="20.00")
        line = payload["lineItems"]["nodes"][0]
        line["discountedUnitPriceAfterAllDiscountsSet"] = self._bag("6.67")
        line["discountAllocations"] = [{"allocatedAmountSet": self._bag("10.00")}]

        binding = self.order_model.browse(
            self.order_model._job_import_order(self.instance.id, payload)
        )

        self.assertEqual(binding.state, "synced")
        self.assertEqual(binding.odoo_id.amount_total, 20)

    def test_order_edit_after_delivery_is_rejected(self):
        binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=3)
        )
        binding = self.order_model.browse(binding_id)

        with patch.object(type(self.order_model), "_is_delivered", return_value=True):
            result = self.order_model._job_import_order(
                self.instance.id,
                self._payload(
                    order_id=3,
                    quantity=2,
                    total="20.00",
                    updatedAt="2026-01-12T10:00:00Z",
                ),
            )

        self.assertFalse(result)
        self.assertEqual(binding.state, "error")
        self.assertEqual(binding.odoo_id.order_line.product_uom_qty, 1)

    def test_cancel_after_delivery_is_rejected(self):
        binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=4)
        )
        binding = self.order_model.browse(binding_id)

        with patch.object(type(self.order_model), "_is_delivered", return_value=True):
            result = self.order_model._job_import_order(
                self.instance.id,
                self._cancelled_payload(order_id=4),
            )

        self.assertFalse(result)
        self.assertNotEqual(binding.odoo_id.state, "cancel")
        self.assertIn("already delivered", binding.error_message)

    def test_cancel_that_odoo_does_not_apply_is_reported(self):
        self.instance.order_confirmation_policy = "auto"
        binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id,
                self._payload(order_id=13, displayFinancialStatus="PAID"),
            )
        )
        sale_order = binding.odoo_id

        # The cancel is blocked: Odoo returns an action and leaves the order.
        with patch.object(
            type(sale_order), "action_cancel", return_value={"type": "ir.actions"}
        ):
            result = self.order_model._job_import_order(
                self.instance.id,
                self._cancelled_payload(order_id=13, displayFinancialStatus="PAID"),
            )

        self.assertFalse(result)
        self.assertEqual(sale_order.state, "sale")
        self.assertIn("Odoo could not cancel", binding.error_message)

    def test_cancel_of_confirmed_order_cancels_the_sale_order(self):
        self.instance.order_confirmation_policy = "auto"
        binding_id = self.order_model._job_import_order(
            self.instance.id,
            self._payload(order_id=12, displayFinancialStatus="PAID"),
        )
        binding = self.order_model.browse(binding_id)
        self.assertEqual(binding.odoo_id.state, "sale")

        sale_order = binding.odoo_id

        result = self.order_model._job_import_order(
            self.instance.id,
            self._cancelled_payload(order_id=12, displayFinancialStatus="PAID"),
        )

        self.assertTrue(result, binding.error_message)
        self.assertEqual(sale_order.state, "cancel")
        self.assertEqual(sale_order.order_line.product_uom_qty, 1)

    def test_cancel_of_quotation_keeps_its_lines(self):
        binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id, self._payload(order_id=15)
            )
        )
        sale_order = binding.odoo_id
        self.assertEqual(sale_order.state, "draft")

        result = self.order_model._job_import_order(
            self.instance.id, self._cancelled_payload(order_id=15)
        )

        self.assertTrue(result, binding.error_message)
        self.assertEqual(sale_order.state, "cancel")
        self.assertEqual(sale_order.order_line.product_uom_qty, 1)
        self.assertEqual(sale_order.amount_total, 10)

    def test_unmapped_tax_records_actionable_error(self):
        payload = self._payload(order_id=5, total="11.00")
        payload["shippingAddress"] = {"countryCodeV2": "US"}
        payload["currentTotalTaxSet"] = self._bag("1.00")
        payload["lineItems"]["nodes"][0]["taxLines"] = [
            {"title": "Tax", "rate": "0.1", "priceSet": self._bag("1.00")}
        ]

        result = self.order_model._job_import_order(self.instance.id, payload)

        binding = self.order_model.search(
            [
                ("instance_id", "=", self.instance.id),
                ("shopify_id", "=", "gid://shopify/Order/5"),
            ]
        )
        self.assertFalse(result)
        self.assertEqual(binding.missing_tax_rate, "0.1")
        self.assertTrue(binding.missing_tax_country_id)

    def _austin_payload(self, order_id):
        # Austin, TX: state 6.25 %, city 1 %, transit 1 %.
        payload = self._payload(order_id=order_id, total="108.25")
        payload["shippingAddress"] = {"countryCodeV2": "US"}
        payload["currentSubtotalPriceSet"] = self._bag("100.00")
        payload["currentTotalTaxSet"] = self._bag("8.25")
        line = payload["lineItems"]["nodes"][0]
        line["id"] = f"gid://shopify/LineItem/{order_id}0"
        line["originalUnitPriceSet"] = self._bag("100.00")
        line["discountedUnitPriceAfterAllDiscountsSet"] = self._bag("100.00")
        line["taxLines"] = [
            {"title": title, "rate": rate, "priceSet": self._bag(amount)}
            for title, rate, amount in (
                ("Texas State Tax", "0.0625", "6.25"),
                ("Austin City Tax", "0.01", "1.00"),
                ("Austin MTA Transit", "0.01", "1.00"),
            )
        ]
        return payload

    def _map_tax(self, rate, amount):
        tax = self.env["account.tax"].create(
            {
                "name": f"Tax {amount}%",
                "amount": amount,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "company_id": self.instance.company_id.id,
            }
        )
        self.env["shopify.tax.mapping"].create(
            {
                "instance_id": self.instance.id,
                "rate": rate,
                "country_id": self.env.ref("base.us").id,
                "price_included": False,
                "tax_id": tax.id,
            }
        )
        return tax

    def test_same_rate_tax_lines_use_the_mapping_of_their_sum(self):
        state_tax = self._map_tax("0.0625", 6.25)
        self._map_tax("0.01", 1.0)
        local_tax = self._map_tax("0.02", 2.0)

        binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id, self._austin_payload(order_id=92)
            )
        )

        self.assertEqual(binding.state, "synced")
        self.assertEqual(binding.odoo_id.amount_total, 108.25)
        self.assertEqual(binding.odoo_id.order_line.tax_ids, state_tax | local_tax)

    def test_same_rate_tax_lines_ask_for_the_mapping_of_their_sum(self):
        self._map_tax("0.0625", 6.25)
        self._map_tax("0.01", 1.0)

        result = self.order_model._job_import_order(
            self.instance.id, self._austin_payload(order_id=93)
        )

        binding = self.order_model.search(
            [
                ("instance_id", "=", self.instance.id),
                ("shopify_id", "=", "gid://shopify/Order/93"),
            ]
        )
        self.assertFalse(result)
        self.assertEqual(binding.missing_tax_rate, "0.02")

    def test_high_risk_sets_hold_and_release_action(self):
        payload = self._payload(order_id=6)
        payload["risk"] = {"assessments": [{"riskLevel": "HIGH"}]}

        binding_id = self.order_model._job_import_order(self.instance.id, payload)
        order = self.order_model.browse(binding_id).odoo_id

        self.assertTrue(order.shopify_risk_hold)
        order.action_release_shopify_risk_hold()
        self.assertFalse(order.shopify_risk_hold)

    def test_sale_order_takes_the_shopify_order_name(self):
        payload = self._payload(order_id=16)
        payload["lineItems"]["nodes"][0]["id"] = "gid://shopify/LineItem/160"
        existing = self.order_model.browse(
            self.order_model._job_import_order(self.instance.id, payload)
        )
        odoo_name = existing.odoo_id.name
        self.instance.order_use_shopify_name = True

        payload["updatedAt"] = "2026-01-11T10:00:00Z"
        self.order_model._job_import_order(self.instance.id, payload)
        draft = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id, self._draft_payload(), is_draft=True
            )
        )
        self.assertEqual(draft.odoo_id.name, "#D90")
        order = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id,
                self._payload(order_id=90, sourceName="shopify_draft_order"),
            )
        )

        self.assertEqual(existing.odoo_id.name, odoo_name)
        self.assertEqual(order.odoo_id, draft.odoo_id)
        self.assertEqual(order.odoo_id.name, "#90")

    def _draft_payload(self, draft_id=90, order_id=90):
        return {
            "id": f"gid://shopify/DraftOrder/{draft_id}",
            "name": f"#D{draft_id}",
            "status": "COMPLETED",
            "createdAt": "2026-01-10T10:00:00Z",
            "updatedAt": "2026-01-10T10:00:00Z",
            "currencyCode": self.currency.name,
            "presentmentCurrencyCode": self.currency.name,
            "subtotalPriceSet": self._bag("10.00"),
            "totalDiscountsSet": self._bag("0.00"),
            "totalShippingPriceSet": self._bag("0.00"),
            "totalTaxSet": self._bag("0.00"),
            "totalPriceSet": self._bag("10.00"),
            "order": {"id": f"gid://shopify/Order/{order_id}"},
            "lineItems": {
                "nodes": [
                    {
                        "id": "gid://shopify/DraftOrderLineItem/900",
                        "name": "Bound Order Product",
                        "quantity": 1,
                        "variant": {"id": self.variant_binding.shopify_id},
                        "originalUnitPriceSet": self._bag("10.00"),
                        "discountedTotalSet": self._bag("10.00"),
                        "taxLines": [],
                    }
                ]
            },
        }

    def test_draft_order_discount_reaches_the_sale_order(self):
        payload = self._draft_payload(draft_id=91, order_id=91)
        payload.update(
            {
                "status": "OPEN",
                "order": None,
                "appliedDiscount": {"title": "Test", "amountSet": self._bag("1.00")},
                "subtotalPriceSet": self._bag("9.00"),
                "totalDiscountsSet": self._bag("1.00"),
                "totalPriceSet": self._bag("9.00"),
            }
        )

        binding = self.order_model.browse(
            self.order_model._job_import_order(self.instance.id, payload, is_draft=True)
        )

        self.assertEqual(binding.state, "synced", binding.error_message)
        self.assertEqual(binding.odoo_id.amount_total, 9.0)
        self.assertEqual(binding.odoo_id.order_line.discount, 10.0)

    def test_completed_draft_links_real_order_without_duplicate_sale(self):
        draft = self._draft_payload()
        before = self.env["sale.order"].search_count([])
        draft_binding_id = self.order_model._job_import_order(
            self.instance.id, draft, is_draft=True
        )

        order_binding_id = self.order_model._job_import_order(
            self.instance.id, self._payload(order_id=90)
        )

        draft_binding = self.order_model.browse(draft_binding_id)
        order_binding = self.order_model.browse(order_binding_id)
        self.assertEqual(self.env["sale.order"].search_count([]), before + 1)
        self.assertEqual(draft_binding.odoo_id, order_binding.odoo_id)
        self.assertEqual(draft_binding.replaced_by_id, order_binding)
        self.assertEqual(len(order_binding.odoo_id.order_line), 1)

    def test_order_from_draft_waits_for_its_draft_order(self):
        with self.assertRaises(RetryableJobError):
            self.order_model._job_import_order(
                self.instance.id,
                self._payload(order_id=91, sourceName="shopify_draft_order"),
            )
        self.assertFalse(
            self.order_model.search([("shopify_id", "=", "gid://shopify/Order/91")])
        )

    def test_order_from_draft_is_imported_alone_on_its_last_attempt(self):
        job = self.order_model.with_delay()._job_import_order(
            self.instance.id,
            self._payload(order_id=91, sourceName="shopify_draft_order"),
        )
        for _attempt in range(job.max_retries - 1):
            with self.assertRaises(RetryableJobError):
                job.perform()
            job.store()

        binding = self.order_model.browse(job.perform())

        self.assertEqual(binding.state, "synced")
        self.assertEqual(binding.odoo_id.amount_total, 10)
        self.assertTrue(
            self.env["shopify.log"].search(
                [
                    ("res_model", "=", binding._name),
                    ("res_id", "=", binding.id),
                    ("level", "=", "warning"),
                ]
            )
        )

    def test_order_from_draft_takes_over_confirmed_draft_quotation(self):
        draft_binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id, self._draft_payload(), is_draft=True
            )
        )
        quotation = draft_binding.odoo_id
        draft_line = quotation.order_line
        quotation.action_confirm()

        binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id,
                self._payload(order_id=90, sourceName="shopify_draft_order"),
            )
        )

        self.assertEqual(binding.state, "synced")
        self.assertEqual(binding.odoo_id, quotation)
        self.assertEqual(quotation.order_line, draft_line)
        self.assertEqual(binding.line_binding_ids.odoo_id, draft_line)
        self.assertEqual(draft_line.shopify_line_id, "gid://shopify/LineItem/30")
        self.assertEqual(draft_binding.replaced_by_id, binding)

    def test_order_from_draft_is_imported_alone_when_drafts_are_disabled(self):
        self.instance.draft_order_import_enabled = False

        draft_binding_id = self.order_model._job_import_order(
            self.instance.id, self._draft_payload(), is_draft=True
        )
        binding = self.order_model.browse(
            self.order_model._job_import_order(
                self.instance.id,
                self._payload(order_id=90, sourceName="shopify_draft_order"),
            )
        )

        self.assertFalse(draft_binding_id)
        self.assertEqual(binding.odoo_id.amount_total, 10)
        self.assertNotIn(
            "DRAFT_ORDERS_CREATE", self.instance._required_webhook_topics()
        )

    def test_order_import_is_retried_while_another_job_holds_the_order(self):
        with db_connect(self.env.cr.dbname).cursor() as cr:
            cr.execute(
                "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
                (self.instance.id, "gid://shopify/Order/1"),
            )
            with self.assertRaises(RetryableJobError):
                self.order_model._job_import_order(self.instance.id, self._payload())

    def test_gateway_mapping_is_case_normalized_for_payment_split(self):
        journal = self.bank_journal
        if not journal:
            self.skipTest("No bank or cash journal is installed for the test company.")

        mapping = self.env["shopify.gateway.journal"].create(
            {
                "instance_id": self.instance.id,
                "gateway": "  Shop Pay ",
                "journal_id": journal.id,
            }
        )

        self.assertEqual(mapping.gateway, "shop pay")

    def test_paid_order_registers_each_gateway_transaction_once(self):
        journal = self.bank_journal
        sale_journal = self.sale_journal
        if not journal or not sale_journal:
            self.skipTest("The test company has no accounting journals.")
        self.instance.write(
            {
                "order_confirmation_policy": "auto",
                "order_invoicing_policy": "paid",
            }
        )
        for gateway in ("gateway-a", "gateway-b"):
            self.env["shopify.gateway.journal"].create(
                {
                    "instance_id": self.instance.id,
                    "gateway": gateway,
                    "journal_id": journal.id,
                }
            )
        payload = self._payload(order_id=7, displayFinancialStatus="PAID")
        payload["transactions"] = [
            {
                "id": "gid://shopify/OrderTransaction/701",
                "gateway": "gateway-a",
                "kind": "SALE",
                "status": "SUCCESS",
                "amountSet": self._bag("4.00"),
            },
            {
                "id": "gid://shopify/OrderTransaction/702",
                "gateway": "gateway-b",
                "kind": "CAPTURE",
                "status": "SUCCESS",
                "amountSet": self._bag("6.00"),
            },
        ]

        binding_id = self.order_model._job_import_order(self.instance.id, payload)
        self.order_model._job_import_order(self.instance.id, payload)

        payments = self.env["shopify.gateway.payment"].search(
            [("order_binding_id", "=", binding_id)]
        )
        self.assertEqual(len(payments), 2)
        self.assertEqual(set(payments.mapped("amount")), {"4.00", "6.00"})

    def test_refund_of_invoiced_order_creates_posted_credit_note(self):
        sale_journal = self.sale_journal
        if not sale_journal:
            self.skipTest("The test company has no sales journal.")
        self.instance.write(
            {
                "order_confirmation_policy": "auto",
                "order_invoicing_policy": "paid",
            }
        )
        initial = self._payload(order_id=8, displayFinancialStatus="PAID")
        binding_id = self.order_model._job_import_order(self.instance.id, initial)
        binding = self.order_model.browse(binding_id)
        self.assertTrue(binding.odoo_id.invoice_ids)

        refunded = self._payload(
            order_id=8,
            displayFinancialStatus="PAID",
            updatedAt="2026-01-13T10:00:00Z",
        )
        refunded["refunds"] = {
            "nodes": [
                {
                    "id": "gid://shopify/Refund/801",
                    "createdAt": "2026-01-13T10:00:00Z",
                    "totalRefundedSet": self._bag("5.00"),
                    "refundLineItems": {
                        "nodes": [
                            {
                                "id": "gid://shopify/RefundLineItem/802",
                                "lineItem": {"id": "gid://shopify/LineItem/30"},
                                "quantity": 1,
                                "restockType": "NO_RESTOCK",
                                "subtotalSet": self._bag("5.00"),
                                "totalTaxSet": self._bag("0.00"),
                            }
                        ]
                    },
                    "refundShippingLines": {"nodes": []},
                    "orderAdjustments": {"nodes": []},
                    "transactions": {"nodes": []},
                }
            ]
        }

        result = self.order_model._job_import_order(self.instance.id, refunded)

        refund = binding.refund_binding_ids
        self.assertTrue(result, binding.error_message)
        self.assertEqual(len(refund), 1)
        self.assertEqual(refund.move_id.move_type, "out_refund")
        self.assertEqual(refund.move_id.state, "posted")

    def _updated_orders_page(self, numbers, cursor=None):
        return {
            "orders": {
                "nodes": [
                    {
                        "id": f"gid://shopify/Order/{number}",
                        "name": f"#{number}",
                        "updatedAt": "2026-11-01T10:00:00Z",
                    }
                    for number in numbers
                ],
                "pageInfo": {"hasNextPage": bool(cursor), "endCursor": cursor},
            }
        }

    def test_order_drift_imports_orders_updated_since_the_last_run(self):
        self.instance.write(
            {
                "order_drift_since": datetime(2026, 10, 1, 8, 0),
                "draft_order_import_enabled": False,
            }
        )
        client = Mock()
        client.execute.side_effect = [
            self._updated_orders_page([1001], cursor="page-2"),
            self._updated_orders_page([1002]),
        ]

        with (
            freeze_time("2026-11-02 09:00:00"),
            trap_jobs() as trap,
            patch.object(type(self.instance), "_shopify_client", return_value=client),
        ):
            queued = self.instance._job_sync_updated_orders()

        self.assertEqual(queued, 2)
        search = "updated_at:>='2026-10-01T07:00:00Z'"
        self.assertEqual(
            [call.args[1] for call in client.execute.call_args_list],
            [
                {"after": None, "query": search},
                {"after": "page-2", "query": search},
            ],
        )
        trap.assert_jobs_count(2, only=self.order_model._job_import_order_from_api)
        self.assertEqual(self.instance.order_drift_since, datetime(2026, 11, 2, 9, 0))

    def test_order_drift_skips_orders_already_imported_in_that_version(self):
        self.instance.write(
            {
                "order_drift_since": datetime(2026, 10, 1, 8, 0),
                "draft_order_import_enabled": False,
            }
        )
        self.order_model.create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Order/1001",
                "order_name": "#1001",
                "external_updated_at": datetime(2026, 11, 1, 10, 0),
                "state": "synced",
            }
        )
        client = Mock()
        client.execute.return_value = self._updated_orders_page([1001, 1002])

        with (
            trap_jobs() as trap,
            patch.object(type(self.instance), "_shopify_client", return_value=client),
        ):
            queued = self.instance._job_sync_updated_orders()

        self.assertEqual(queued, 1)
        trap.assert_enqueued_job(
            self.order_model._job_import_order_from_api,
            args=(self.instance.id, "gid://shopify/Order/1002"),
        )

    def test_order_drift_starts_two_days_back_on_its_first_run(self):
        self.instance.write(
            {"order_drift_since": False, "draft_order_import_enabled": False}
        )
        client = Mock()
        client.execute.return_value = self._updated_orders_page([])

        with (
            freeze_time("2026-11-02 09:00:00"),
            patch.object(type(self.instance), "_shopify_client", return_value=client),
        ):
            queued = self.instance._job_sync_updated_orders()

        self.assertEqual(queued, 0)
        self.assertEqual(
            client.execute.call_args.args[1]["query"],
            "updated_at:>='2026-10-31T08:00:00Z'",
        )
        self.assertEqual(self.instance.order_drift_since, datetime(2026, 11, 2, 9, 0))

    def test_order_drift_keeps_its_date_when_shopify_fails(self):
        since = datetime(2026, 10, 1, 8, 0)
        self.instance.write(
            {"order_drift_since": since, "draft_order_import_enabled": False}
        )
        client = Mock()
        client.execute.side_effect = ShopifyError("Shopify is unavailable.")

        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            self.assertRaises(ShopifyError),
        ):
            self.instance._job_sync_updated_orders()

        self.assertEqual(self.instance.order_drift_since, since)

    def test_order_drift_also_imports_updated_draft_orders(self):
        self.instance.write(
            {
                "order_drift_since": datetime(2026, 10, 1, 8, 0),
                "draft_order_import_enabled": True,
            }
        )
        client = Mock()
        client.execute.side_effect = [
            self._updated_orders_page([]),
            {"draftOrders": {"nodes": [], "pageInfo": {"hasNextPage": False}}},
        ]

        with (
            freeze_time("2026-11-02 09:00:00"),
            patch.object(type(self.instance), "_shopify_client", return_value=client),
        ):
            self.instance._job_sync_updated_orders()

        self.assertEqual(
            client.execute.call_args_list[1].args[1]["query"],
            "updated_at:>=2026-10-01",
        )

    def test_order_drift_cron_queues_the_updated_orders_sync(self):
        with trap_jobs() as trap:
            self.env["shopify.instance"]._cron_reconcile_orders()

        trap.assert_jobs_count(1, only=self.instance._job_sync_updated_orders)

    def test_order_drift_search_converts_to_utc(self):
        since = datetime(
            2026, 11, 2, 10, 30, 15, 500, tzinfo=timezone(timedelta(hours=1))
        )

        self.assertEqual(
            orders_updated_search(since), "updated_at:>='2026-11-02T09:30:15Z'"
        )
