from odoo import SUPERUSER_ID

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

# The module, not the class: a test class imported into this namespace would
# run again as a test of this module.
from . import test_order_sync as order_tests


class TestOrderCarrier(AccountTestInvoicingCommon):
    """The Shopify shipping method gives the order and its delivery a carrier."""

    _bag = order_tests.TestShopifyOrderSync._bag
    _order_payload = order_tests.TestShopifyOrderSync._payload

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = (
            cls.env["base"]
            .with_user(SUPERUSER_ID)
            .with_company(cls.company_data["company"])
            .env
        )
        company = cls.company_data["company"]
        cls.currency = company.currency_id
        # A storable product, so that a confirmed order has a delivery.
        product = cls.env["product.product"].create(
            {
                "name": "Carrier Order Product",
                "type": "consu",
                "is_storable": True,
                "company_id": company.id,
            }
        )
        cls.postnl, cls.dhl = cls.env["delivery.carrier"].create(
            [
                {
                    "name": name,
                    "delivery_type": "fixed",
                    "product_id": cls.env["product.product"]
                    .create({"name": f"{name} Shipping", "type": "service"})
                    .id,
                }
                for name in ("PostNL Test", "DHL Test")
            ]
        )
        cls.store_a, cls.store_b = cls.env["shopify.instance"].create(
            [
                {
                    "name": f"Carrier Store {letter}",
                    "shop_url": f"carrier-store-{letter.lower()}.myshopify.com",
                    "access_token": "test-token",
                    "webhook_secret": "test-secret",
                    "order_confirmation_policy": "auto",
                    "auto_confirm_paid": True,
                }
                for letter in ("A", "B")
            ]
        )
        (cls.store_a | cls.store_b).write({"state": "connected"})
        cls.env["shopify.carrier.mapping"].create(
            [
                {
                    "instance_id": cls.store_a.id,
                    "carrier_id": cls.postnl.id,
                    "tracking_company": "PostNL",
                    "shipping_method_names": "Standard, Pakket aan huis",
                },
                {
                    "instance_id": cls.store_a.id,
                    "carrier_id": cls.dhl.id,
                    "tracking_company": "DHL",
                    "shipping_method_names": "express",
                },
                # Store B maps the carrier only for the tracking company.
                {
                    "instance_id": cls.store_b.id,
                    "carrier_id": cls.postnl.id,
                    "tracking_company": "PostNL",
                },
            ]
        )
        cls.bindings = {}
        for store in (cls.store_a, cls.store_b):
            template_binding = cls.env["shopify.product.template"].create(
                {
                    "instance_id": store.id,
                    "shopify_id": "gid://shopify/Product/10",
                    "odoo_id": product.product_tmpl_id.id,
                    "status": "ACTIVE",
                }
            )
            variant_binding = cls.env["shopify.product.variant"].create(
                {
                    "instance_id": store.id,
                    "shopify_id": "gid://shopify/ProductVariant/20",
                    "template_binding_id": template_binding.id,
                    "odoo_id": product.id,
                }
            )
            cls.bindings[store] = (template_binding, variant_binding)
        cls.order_model = cls.env["shopify.order"]

    def _import(self, store, title, code="", order_id=3001, **values):
        # The payload helper reads the bindings from self.
        self.template_binding, self.variant_binding = self.bindings[store]
        # One paid product line of 10.00 and a shipping line of 5.00.
        payload = self._order_payload(
            order_id=order_id,
            total="15.00",
            currentShippingPriceSet=self._bag("5.00"),
            displayFinancialStatus="PAID",
            **values,
        )
        payload["shippingLines"] = {
            "nodes": [
                {
                    "id": f"gid://shopify/ShippingLine/{order_id}",
                    "title": title,
                    "code": code,
                    "originalPriceSet": self._bag("5.00"),
                    "currentDiscountedPriceSet": self._bag("5.00"),
                    "taxLines": [],
                }
            ]
        }
        binding = self.order_model.browse(
            self.order_model._job_import_order(store.id, payload)
        )
        self.assertEqual(binding.state, "synced", binding.error_message)
        return binding.odoo_id

    def _delivery(self, order):
        return order.picking_ids.filtered(
            lambda picking: picking.picking_type_code == "outgoing"
        )

    def test_mapped_shipping_method_sets_the_carrier(self):
        order = self._import(self.store_a, "Standard")
        self.assertEqual(order.state, "sale")
        self.assertEqual(order.carrier_id, self.postnl)
        self.assertEqual(self._delivery(order).carrier_id, self.postnl)

    def test_match_ignores_case_and_uses_the_code_too(self):
        order = self._import(self.store_a, "Snelle levering", code="EXPRESS")
        self.assertEqual(order.carrier_id, self.dhl)
        self.assertEqual(self._delivery(order).carrier_id, self.dhl)

    def test_unmapped_shipping_method_leaves_the_carrier_empty(self):
        order = self._import(self.store_a, "Afhalen")
        self.assertFalse(order.carrier_id)
        self.assertFalse(self._delivery(order).carrier_id)

    def test_mapping_of_another_store_does_not_apply(self):
        # Store B has PostNL only as a tracking company, without methods.
        order = self._import(self.store_b, "Standard")
        self.assertFalse(order.carrier_id)

    def test_carrier_chosen_by_a_user_is_kept_on_a_new_import(self):
        order = self._import(self.store_a, "Standard")
        delivery = self._delivery(order)
        order.carrier_id = self.dhl
        delivery.carrier_id = self.dhl
        self._import(self.store_a, "Standard", updatedAt="2026-01-12T10:00:00Z")
        self.assertEqual(order.carrier_id, self.dhl)
        self.assertEqual(delivery.carrier_id, self.dhl)

    def test_existing_delivery_without_carrier_gets_it_on_a_new_import(self):
        # An order imported before the mapping existed.
        mapping = self.store_a.carrier_mapping_ids.filtered(
            lambda item: item.carrier_id == self.postnl
        )
        methods = mapping.shipping_method_names
        mapping.shipping_method_names = False
        order = self._import(self.store_a, "Standard")
        self.assertFalse(self._delivery(order).carrier_id)
        mapping.shipping_method_names = methods
        self._import(self.store_a, "Standard", updatedAt="2026-01-12T10:00:00Z")
        self.assertEqual(order.carrier_id, self.postnl)
        self.assertEqual(self._delivery(order).carrier_id, self.postnl)
