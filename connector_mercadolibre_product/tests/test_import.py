# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import FakeResponse, MercadoLibreProductCommon, Transport


class TestMercadoLibreProductImport(MercadoLibreProductCommon):
    def test_sku_match_links_product_without_duplicating_it(self):
        product = self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        again = self._import_item(self.item_legacy)
        self.assertEqual(binding, again)
        self.assertEqual(binding.odoo_id, product)
        self.assertEqual(binding.seller_sku, "SKU-LEGACY")
        self.assertEqual(binding.listing_status, "active")
        self.assertEqual(binding.marketplace_qty, 4)
        self.assertFalse(binding.fulfillment)
        self.assertFalse(binding.variation_id)
        self.assertEqual(
            binding.picture_urls,
            ["https://http2.mlstatic.com/legacy.jpg"],
        )
        self.assertEqual(binding.category_id.external_id, "MLA1000")
        self.assertEqual(
            self.env["product.product"].search_count(
                [("default_code", "=", "SKU-LEGACY")]
            ),
            1,
        )
        self.assertEqual(
            self.env["mercadolibre.product.product"].search_count(
                [("external_id", "=", "MLA100")]
            ),
            1,
        )

    def test_seller_sku_wins_over_custom_field(self):
        preferred = self._product("SKU-A")
        self._product("SKU-B")
        item = self._copy_item(self.item_legacy, seller_custom_field="SKU-B")
        item["attributes"] = [{"id": "SELLER_SKU", "value_name": "SKU-A"}]
        binding = self._import_item(item)
        self.assertEqual(binding.odoo_id, preferred)
        self.assertEqual(binding.seller_sku, "SKU-A")

    def test_custom_field_matches_when_attribute_is_missing(self):
        product = self._product("SKU-CUSTOM")
        item = self._copy_item(
            self.item_legacy,
            seller_custom_field="SKU-CUSTOM",
            attributes=[],
        )
        binding = self._import_item(item)
        self.assertEqual(binding.odoo_id, product)

    def test_unmatched_listing_stays_unbound(self):
        self.backend.create_missing_products = False
        item = self._copy_item(self.item_legacy, seller_custom_field="SKU-MISSING")
        item["attributes"] = [{"id": "SELLER_SKU", "value_name": "SKU-MISSING"}]
        binding = self._import_item(item)
        self.assertTrue(binding)
        self.assertFalse(binding.odoo_id)
        self.assertFalse(
            self.env["product.product"].search([("default_code", "=", "SKU-MISSING")])
        )

    def test_create_missing_products_uses_seller_sku(self):
        self.backend.create_missing_products = True
        item = self._copy_item(
            self.item_legacy,
            title="Created kettle",
            seller_custom_field="SKU-NEW",
            price=42,
        )
        item["attributes"] = [{"id": "SELLER_SKU", "value_name": "SKU-NEW"}]
        binding = self._import_item(item)
        self._import_item(item)
        product = binding.odoo_id
        self.assertEqual(product.default_code, "SKU-NEW")
        self.assertEqual(product.name, "Created kettle")
        self.assertEqual(product.type, "consu")
        self.assertTrue(product.is_storable)
        self.assertEqual(product.list_price, 42)
        self.assertEqual(
            self.env["product.product"].search_count(
                [("default_code", "=", "SKU-NEW")]
            ),
            1,
        )

    def test_unknown_status_is_inactive(self):
        item = self._copy_item(self.item_legacy, status="payment_required")
        binding = self._import_item(item)
        self.assertEqual(binding.listing_status, "inactive")

    def test_variations_are_separate_bindings(self):
        item = self._copy_item(
            self.item_legacy,
            id="MLA400",
            variations=[
                {
                    "id": 11,
                    "available_quantity": 1,
                    "attributes": [{"id": "SELLER_SKU", "value_name": "SKU-V1"}],
                },
                {
                    "id": 12,
                    "available_quantity": 2,
                    "seller_custom_field": "SKU-V2",
                },
            ],
        )
        bindings = self._import_item(item)
        self.assertEqual(len(bindings), 2)
        self.assertEqual(set(bindings.mapped("variation_id")), {"11", "12"})
        with self.backend.work_on("mercadolibre.product.product") as work:
            binder = work.component(usage="binder")
            first = binder.to_internal("MLA400", variation_id="11")
            self.assertEqual(first.seller_sku, "SKU-V1")
            self.assertEqual(binder.to_external(first), "MLA400")
            self.assertFalse(binder.to_internal("MLA400"))

    def test_fulfillment_item_is_flagged(self):
        binding = self._import_item(self.item_fulfillment)
        self.assertTrue(binding.fulfillment)
        self.assertEqual(binding.user_product_id, "MLAU300")
        self.assertEqual(binding.marketplace_qty, 20)

    def test_batch_import_enqueues_one_job_per_item(self):
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {"paging": {"total": 2}, "results": ["MLA100", "MLA200"]},
                )
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        backend._job_import_listings()
        self.assertTrue(self.backend.last_product_sync_at)
        for item_id in ("MLA100", "MLA200"):
            jobs = self._jobs(f"meli:item:{self.backend.id}:{item_id}:")
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs.method_name, "_job_import_item")
        self.assertEqual(transport.calls[0]["method"], "GET")
        self.assertIn("/users/123456789/items/search", transport.calls[0]["url"])

    def test_search_uses_scan_above_one_thousand(self):
        transport = Transport(
            [
                FakeResponse(200, {"paging": {"total": 1001}, "results": []}),
                FakeResponse(200, {"results": ["MLA1", "MLA2"], "scroll_id": False}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            item_ids = work.component(usage="backend.adapter").search_item_ids()
        self.assertEqual(item_ids, ["MLA1", "MLA2"])
        self.assertEqual(transport.calls[1]["params"]["search_type"], "scan")
