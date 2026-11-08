# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from odoo.addons.queue_job.exception import RetryableJobError

from .common import FakeResponse, MercadoLibreProductCommon, Transport


class TestMercadoLibreProductExport(MercadoLibreProductCommon):
    def test_price_exporter_posts_prices_api(self):
        product = self._product("SKU-LEGACY", price=1800)
        binding = self._import_item(self.item_legacy)
        self.assertEqual(binding.odoo_id, product)
        transport = Transport([FakeResponse(200, {"id": "MLA100"})])
        binding.with_context(mercadolibre_transport=transport)._job_export_price()
        self.assertEqual(len(transport.calls), 1)
        call = transport.calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertTrue(call["url"].endswith("/items/MLA100/prices"))
        self.assertEqual(call["json"]["prices"][0]["amount"], product.lst_price)
        self.assertNotIn("price", call["json"])
        self.assertFalse(any(item["method"] == "PUT" for item in transport.calls))

    def test_price_change_enqueues_one_job(self):
        product = self._product("SKU-LEGACY", price=100)
        binding = self._import_item(self.item_legacy)
        product = self.env["product.product"].browse(product.id)
        product.lst_price = 222
        jobs = self._jobs(f"meli:price:{self.backend.id}:{binding.id}")
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs.method_name, "_job_export_price")

    def test_legacy_stock_sends_available_quantity(self):
        self.backend.versions = "legacy_item"
        self.backend.export_stock = True
        product = self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        self._set_qty(product, 4)
        mapping = self._mapping()
        transport = Transport([FakeResponse(200, {})])
        binding.with_context(mercadolibre_transport=transport)._job_export_stock(
            mapping.id
        )
        call = transport.calls[0]
        self.assertEqual(call["method"], "PUT")
        self.assertTrue(call["url"].endswith("/items/MLA100"))
        self.assertNotIn("/prices", call["url"])
        self.assertEqual(call["json"], {"available_quantity": 4})

    def test_legacy_stock_exports_zero(self):
        self.backend.versions = "legacy_item"
        self.backend.export_stock = True
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        mapping = self._mapping()
        transport = Transport([FakeResponse(200, {})])
        binding.with_context(mercadolibre_transport=transport)._job_export_stock(
            mapping.id
        )
        self.assertEqual(transport.calls[0]["json"], {"available_quantity": 0})

    def test_user_product_stock_uses_seller_warehouse(self):
        self.backend.export_stock = True
        product = self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        self.assertEqual(binding.user_product_id, "MLAU200")
        self._set_qty(product, 6)
        mapping = self._mapping()
        transport = Transport([FakeResponse(200, {})])
        binding.with_context(mercadolibre_transport=transport)._job_export_stock(
            mapping.id
        )
        call = transport.calls[0]
        self.assertEqual(call["method"], "PUT")
        self.assertTrue(
            call["url"].endswith("/user-products/MLAU200/stock/type/seller_warehouse")
        )
        self.assertEqual(
            call["json"],
            {
                "locations": [
                    {
                        "quantity": 6,
                        "store_id": "STORE1",
                        "network_node_id": "NODE1",
                    }
                ]
            },
        )

    def test_selling_address_uses_its_stock_type(self):
        self.backend.export_stock = True
        self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        mapping = self._mapping(stock_type="selling_address")
        transport = Transport([FakeResponse(200, {})])
        binding.with_context(mercadolibre_transport=transport)._job_export_stock(
            mapping.id
        )
        self.assertTrue(
            transport.calls[0]["url"].endswith(
                "/user-products/MLAU200/stock/type/selling_address"
            )
        )

    def test_user_product_without_id_falls_back_to_legacy(self):
        self.backend.versions = "user_product"
        self.backend.export_stock = True
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        self.assertFalse(binding.user_product_id)
        mapping = self._mapping()
        transport = Transport([FakeResponse(200, {})])
        binding.with_context(mercadolibre_transport=transport)._job_export_stock(
            mapping.id
        )
        self.assertTrue(transport.calls[0]["url"].endswith("/items/MLA100"))
        self.assertIn("available_quantity", transport.calls[0]["json"])

    def test_fulfillment_binding_exports_nothing(self):
        self.backend.export_stock = True
        self._product("SKU-FULL")
        binding = self._import_item(self.item_fulfillment)
        self.assertTrue(binding.fulfillment)
        mapping = self._mapping()
        transport = Transport([FakeResponse(200, {})])
        exported = binding.with_context(
            mercadolibre_transport=transport
        )._job_export_stock(mapping.id)
        self.assertFalse(exported)
        self.assertFalse(transport.calls)

    def test_fulfillment_mapping_exports_nothing(self):
        self.backend.export_stock = True
        self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        mapping = self._mapping(stock_type="fulfillment")
        transport = Transport([FakeResponse(200, {})])
        exported = binding.with_context(
            mercadolibre_transport=transport
        )._job_export_stock(mapping.id)
        self.assertFalse(exported)
        self.assertFalse(transport.calls)

    def test_repeated_stock_export_keeps_one_pending_job(self):
        self.backend.export_stock = True
        self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        mapping = self._mapping()
        binding._enqueue_stock_export(mapping)
        binding._enqueue_stock_export(mapping)
        jobs = self._jobs(f"meli:stock:{self.backend.id}:{binding.id}:{mapping.id}")
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs.state, "pending")
        self.assertEqual(jobs.method_name, "_job_export_stock")

    def test_done_move_enqueues_stock_for_mapped_warehouse(self):
        self.backend.export_stock = True
        product = self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        warehouse = self._warehouse()
        mapping = self._mapping(warehouse=warehouse)
        self._set_qty(product, 5, warehouse)
        product = self.env["product.product"].browse(product.id)
        move = self.env["stock.move"].create(
            {
                "product_id": product.id,
                "product_uom_qty": 1,
                "location_id": warehouse.lot_stock_id.id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )
        move._action_confirm()
        move._action_assign()
        move.quantity = 1
        move.picked = True
        move._action_done()
        self.assertEqual(move.state, "done")
        jobs = self._jobs(f"meli:stock:{self.backend.id}:{binding.id}:{mapping.id}")
        self.assertEqual(len(jobs), 1)

    def test_stock_version_selects_the_exporter(self):
        self.backend.versions = "legacy_item"
        with self.backend.work_on("mercadolibre.product.product") as work:
            exporter = work.component(usage="stock.exporter")
        self.assertEqual(exporter._name, "mercadolibre.product.exporter.stock.legacy")
        self.backend.versions = "user_product"
        with self.backend.work_on("mercadolibre.product.product") as work:
            exporter = work.component(usage="stock.exporter")
        self.assertEqual(
            exporter._name,
            "mercadolibre.product.exporter.stock.user_product",
        )

    def test_publisher_is_not_installed(self):
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        with self.backend.work_on("mercadolibre.product.product") as work:
            publisher = work.component(usage="product.publisher")
            with self.assertRaises(UserError) as caught:
                publisher.run(binding)
        self.assertIn("Listing publication is not installed.", str(caught.exception))

    def test_price_http_429_is_retryable(self):
        self.backend.access_token = "secret-token"
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        transport = Transport(
            [
                FakeResponse(
                    429,
                    self.error_429,
                    headers={"Retry-After": "15"},
                )
            ]
        )
        # Catch the error directly. assertRaises rolls back its savepoint and
        # would undo the pending state written just before the error is re-raised.
        try:
            binding.with_context(mercadolibre_transport=transport)._job_export_price()
        except RetryableJobError as error:
            self.assertEqual(error.seconds, 15)
            self.assertNotIn("secret-token", str(error))
        else:
            self.fail("HTTP 429 must raise RetryableJobError")
        self.assertEqual(binding.state, "pending")
