# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import AccessError
from odoo.tests.common import new_test_user

from odoo.addons.connector_mercadolibre_product.components.product_adapter import (
    MercadoLibreProductAdapter,
)
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

from .common import FakeResponse, MercadoLibreProductCommon, Transport


class CategoryAdapter:
    def __init__(self, details, attributes=None):
        self.details = details
        self.attributes = attributes if attributes is not None else []
        self.calls = []

    def read(self, path):  # pylint: disable=method-required-super
        self.calls.append(path)
        if path.endswith("/attributes"):
            return self.attributes
        external_id = path.rstrip("/").split("/")[-1]
        return self.details[external_id]


class TestMercadoLibreProductEdges(MercadoLibreProductCommon):
    def _manager(self):
        return new_test_user(
            self.env,
            login="ml_catalog_manager",
            groups=(
                "base.group_user,connector_mercadolibre.group_mercadolibre_manager"
            ),
        )

    def _plain_user(self):
        return new_test_user(
            self.env,
            login="ml_catalog_user",
            groups="base.group_user",
        )

    def _listener(self):
        with self.backend.work_on("product.product") as work:
            listeners = work.many_components(usage="event.listener")
        return next(
            listener
            for listener in listeners
            if listener._name == "mercadolibre.product.listener"
        )

    def _handler(self, name):
        with self.backend.work_on("mercadolibre.notification") as work:
            handlers = work.many_components(usage="notification.handler")
        return next(handler for handler in handlers if handler._name == name)

    def _notification(self, resource, topic="stock-location"):
        return self.env["mercadolibre.notification"].create(
            {
                "backend_id": self.backend.id,
                "topic": topic,
                "resource": resource,
            }
        )

    def test_binder_unwraps_the_product_and_an_empty_match(self):
        product = self._product("SKU-LEGACY")
        self._import_item(self.item_legacy)
        with self.backend.work_on("mercadolibre.product.product") as work:
            binder = work.component(usage="binder")
            self.assertEqual(
                binder.to_internal("MLA100", unwrap=True),
                product,
            )
            self.assertFalse(binder.to_internal("MLA-MISSING", unwrap=True))
            self.assertFalse(binder.to_internal("MLA-MISSING"))

    def test_price_export_skips_when_disabled_or_unbound(self):
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        self.backend.export_prices = False
        transport = Transport([FakeResponse(200, {})])
        exported = binding.with_context(
            mercadolibre_transport=transport
        )._job_export_price()
        self.assertFalse(exported)
        self.assertFalse(transport.calls)
        self.backend.export_prices = True
        binding.odoo_id = False
        exported = binding.with_context(
            mercadolibre_transport=transport
        )._job_export_price()
        self.assertFalse(exported)
        self.assertFalse(transport.calls)

    def test_price_export_records_permanent_and_unexpected_errors(self):
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        transport = Transport(
            [FakeResponse(400, {"message": "nope", "error": "bad_request"})]
        )
        try:
            binding.with_context(mercadolibre_transport=transport)._job_export_price()
        except FailedJobError as error:
            self.assertIn("nope", str(error))
        else:
            self.fail("a client error must fail the job")
        self.assertEqual(binding.state, "error")
        binding.write({"state": "synced", "error_message": False})
        with self.backend.work_on("mercadolibre.product.product") as work:
            exporter = work.component(usage="record.exporter")
            with patch.object(
                MercadoLibreProductAdapter,
                "update_prices",
                side_effect=RuntimeError("boom"),
            ):
                try:
                    exporter.run(binding)
                except FailedJobError as error:
                    self.assertIn("boom", str(error))
                else:
                    self.fail("unexpected errors must fail the job")
        self.assertEqual(binding.state, "error")
        self.assertIn("boom", binding.error_message)

    def test_stock_export_skips_disabled_unbound_and_missing_mappings(self):
        self.backend.versions = "legacy_item"
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        mapping = self._mapping()
        self.backend.export_stock = False
        self.assertFalse(binding._job_export_stock(mapping.id))
        self.backend.export_stock = True
        binding.odoo_id = False
        self.assertFalse(binding._job_export_stock(mapping.id))
        binding.odoo_id = self._product("SKU-LEGACY")
        binding.fulfillment = True
        self.assertFalse(binding._job_export_stock(mapping.id))
        self.assertFalse(binding._job_export_stock(999999))

    def test_import_without_a_payload_reads_the_item(self):
        self._product("SKU-LEGACY")
        transport = Transport([FakeResponse(200, self.item_legacy)])
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            binding = work.component(usage="record.importer").run("MLA100")
        self.assertEqual(binding.external_id, "MLA100")
        self.assertTrue(transport.calls[0]["url"].endswith("/items/MLA100"))

    def test_import_without_category_or_sku_creates_nothing_extra(self):
        item = self._copy_item(self.item_legacy, attributes=[], seller_custom_field="")
        item.pop("category_id")
        binding = self._import_item(item)
        self.assertFalse(binding.category_id)
        self.assertFalse(binding.odoo_id)
        self.assertFalse(binding.seller_sku)

    def test_import_creates_a_product_from_the_sku_when_title_and_price_are_missing(
        self,
    ):
        self.backend.create_missing_products = True
        item = self._copy_item(self.item_legacy, id="MLA101")
        item.pop("title", None)
        item.pop("price", None)
        item["attributes"] = [{"id": "SELLER_SKU", "value_name": "SKU-BARE"}]
        binding = self._import_item(item)
        self.assertEqual(binding.odoo_id.name, "SKU-BARE")
        self.assertEqual(binding.odoo_id.list_price, 0.0)

    def test_import_keeps_a_retryable_error_and_records_a_failed_sync(self):
        self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        with patch.object(
            type(binding),
            "mark_synced",
            side_effect=RetryableJobError("later", seconds=4),
        ):
            with self.assertRaises(RetryableJobError):
                self._import_item(self.item_legacy)
        with patch.object(
            type(binding), "mark_synced", side_effect=FailedJobError("nope")
        ):
            try:
                self._import_item(self.item_legacy)
            except FailedJobError as error:
                self.assertIn("nope", str(error))
            else:
                self.fail("a failed sync must be re-raised")
        self.assertEqual(binding.state, "error")

    def test_import_wraps_a_create_failure_when_no_binding_exists_yet(self):
        item = self._copy_item(self.item_legacy, id="MLA404")
        model = self.env["mercadolibre.product.product"]
        with patch.object(type(model), "create", side_effect=RuntimeError("boom")):
            with self.assertRaises(FailedJobError) as caught:
                self._import_item(item)
        self.assertIn("boom", str(caught.exception))

    def test_search_pages_by_offset_and_stops_on_an_empty_page(self):
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {"paging": {"total": 3}, "results": ["MLA1", "MLA2"]},
                ),
                FakeResponse(200, {"results": []}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            item_ids = work.component(usage="backend.adapter").search_item_ids()
        self.assertEqual(item_ids, ["MLA1", "MLA2"])
        transport = Transport(
            [
                FakeResponse(200, {"paging": {"total": 2}, "results": ["MLA1"]}),
                FakeResponse(200, {"results": ["MLA2"]}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            item_ids = work.component(usage="backend.adapter").search_item_ids()
        self.assertEqual(item_ids, ["MLA1", "MLA2"])

    def test_scan_follows_the_scroll_until_it_repeats_or_ends(self):
        transport = Transport(
            [
                FakeResponse(200, {"paging": {"total": 1001}, "results": []}),
                FakeResponse(200, {"results": ["MLA1"], "scroll_id": "s1"}),
                FakeResponse(200, {"results": ["MLA2"], "scroll_id": "s1"}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            item_ids = work.component(usage="backend.adapter").search_item_ids()
        self.assertEqual(item_ids, ["MLA1", "MLA2"])
        transport = Transport(
            [
                FakeResponse(200, {"paging": {"total": 1001}, "results": []}),
                FakeResponse(200, {"results": ["MLA3"], "scroll_id": "s2"}),
                FakeResponse(200, {"results": [], "scroll_id": "s3"}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            item_ids = work.component(usage="backend.adapter").search_item_ids()
        self.assertEqual(item_ids, ["MLA3"])

    def test_read_stock_accepts_a_relative_resource(self):
        transport = Transport([FakeResponse(200, {"quantity": 2})])
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.product.product") as work:
            payload = work.component(usage="backend.adapter").read_stock(
                "user-products/MLAU200/stock"
            )
        self.assertEqual(payload["quantity"], 2)
        self.assertTrue(
            transport.calls[0]["url"].endswith("/user-products/MLAU200/stock")
        )

    def test_mapper_covers_missing_optional_listing_fields(self):
        with self.backend.work_on("mercadolibre.product.product") as work:
            mapper = work.component(usage="import.mapper")
            values = mapper.listing(
                {
                    "id": "MLA9",
                    "pictures": [{}, {"url": "https://example.com/a.jpg"}],
                    "shipping": {},
                    "inventory_id": "INV",
                    "attributes": [{"id": "SELLER_SKU"}],
                    "seller_custom_field": "SKU-CUSTOM",
                }
            )
        self.assertEqual(values["listing_status"], "active")
        self.assertEqual(values["seller_sku"], "SKU-CUSTOM")
        self.assertEqual(values["picture_urls"], ["https://example.com/a.jpg"])
        self.assertTrue(values["fulfillment"])
        self.assertFalse(values["currency_id"])
        self.assertFalse(values["permalink"])
        self.assertEqual(values["marketplace_qty"], 0.0)
        with self.backend.work_on("mercadolibre.product.product") as work:
            mapper = work.component(usage="import.mapper")
            self.assertFalse(mapper._currency_id("ZZZ"))
            self.assertFalse(mapper._seller_sku(False, False))
            variation = {
                "available_quantity": 0,
                "user_product_id": False,
                "id": False,
            }
            values = mapper.listing(
                {
                    "id": "MLA8",
                    "status": "active",
                    "currency_id": "ARS",
                    "_variation": variation,
                    "available_quantity": 6,
                    "user_product_id": "MLAU8",
                }
            )
        self.assertEqual(values["marketplace_qty"], 0.0)
        self.assertEqual(values["user_product_id"], "MLAU8")
        self.assertFalse(values["variation_id"])

    def test_export_mapper_covers_currency_variation_and_optional_location_ids(self):
        self._product("SKU-LEGACY", price=12)
        binding = self._import_item(self.item_legacy)
        binding.currency_id = False
        binding.variation_id = "15"
        mapping = self._mapping()
        with self.backend.work_on("mercadolibre.product.product") as work:
            mapper = work.component(usage="export.mapper")
            price = mapper.price_payload(binding)
            self.assertEqual(
                price["prices"][0]["currency_id"],
                binding.backend_id.company_id.currency_id.name,
            )
            varied = mapper.legacy_stock_payload(binding, 2)
            self.assertEqual(varied["variations"][0]["id"], 15)
            self.assertEqual(varied["variations"][0]["available_quantity"], 2)
            fractional = mapper.legacy_stock_payload(binding, 1.5)
            self.assertEqual(
                fractional["variations"][0]["available_quantity"],
                1.5,
            )
            mapping.store_id = False
            mapping.network_node_id = False
            bare = mapper.user_product_stock_payload(mapping, 3)
            self.assertEqual(bare, {"locations": [{"quantity": 3}]})
            mapping.store_id = "STORE9"
            store_only = mapper.user_product_stock_payload(mapping, 3)
            self.assertEqual(store_only["locations"][0]["store_id"], "STORE9")
            self.assertNotIn("network_node_id", store_only["locations"][0])

    def test_listener_ignores_unrelated_writes_and_disabled_exports(self):
        product = self._product("SKU-LEGACY")
        product.with_context(connector_no_export=True).write({"lst_price": 11})
        self.env["product.product"].create(
            {"name": "Plain", "type": "consu", "is_storable": True}
        )
        binding = self._import_item(self.item_legacy)
        product = self.env["product.product"].browse(product.id)
        product.name = "Renamed kettle"
        self.assertFalse(self._jobs(f"meli:price:{self.backend.id}:{binding.id}"))
        self.backend.export_prices = False
        product.lst_price = 30
        self.assertFalse(self._jobs(f"meli:price:{self.backend.id}:{binding.id}"))
        listener = self._listener()
        listener.on_record_write(product, fields=None)
        self.env.cr.execute(
            "UPDATE mercadolibre_product_product SET external_id = '' WHERE id = %s",
            (binding.id,),
        )
        binding.invalidate_recordset()
        self.backend.export_prices = True
        listener._export_prices(product)

    def test_listener_stock_paths_cover_locations_and_skipped_mappings(self):
        self.backend.export_stock = True
        product = self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        warehouse = self._warehouse()
        mapping = self._mapping(warehouse=warehouse)
        listener = self._listener()
        supplier = self.env.ref("stock.stock_location_suppliers")
        customer = self.env.ref("stock.stock_location_customers")
        outside = self.env["stock.move"].create(
            {
                "product_id": product.id,
                "product_uom_qty": 1,
                "location_id": supplier.id,
                "location_dest_id": customer.id,
            }
        )
        listener.on_record_write(outside, fields={"state"})
        listener.on_record_create(outside)
        listener._export_stock_for_move(outside)
        self.assertTrue(listener._mapping_touched(mapping, mapping.location_id))
        child = self.env["stock.location"].create(
            {
                "name": "Bin",
                "location_id": warehouse.lot_stock_id.id,
                "usage": "internal",
            }
        )
        self.assertTrue(listener._mapping_touched(mapping, child))
        self.assertTrue(
            listener._mapping_touched(mapping, warehouse.lot_stock_id.location_id)
        )
        other = self.env["stock.location"].create(
            {
                "name": "Elsewhere",
                "location_id": warehouse.view_location_id.id,
                "usage": "internal",
            }
        )
        self.assertFalse(listener._mapping_touched(mapping, other))
        self.env.cr.execute(
            "UPDATE stock_location SET parent_path = NULL WHERE id = %s",
            (child.id,),
        )
        child.invalidate_recordset()
        self.assertFalse(listener._mapping_touched(mapping, child))
        stock = warehouse.lot_stock_id
        stock_path = stock.parent_path
        self.env.cr.execute(
            "UPDATE stock_location SET parent_path = NULL WHERE id = %s",
            (stock.id,),
        )
        stock.invalidate_recordset()
        mapping.invalidate_recordset()
        self.assertFalse(listener._mapping_touched(mapping, other))
        self.env.cr.execute(
            "UPDATE stock_location SET parent_path = %s WHERE id = %s",
            (stock_path, stock.id),
        )
        stock.invalidate_recordset()
        mapping.invalidate_recordset()
        fulfillment = self._mapping(stock_type="fulfillment", warehouse=warehouse)
        move = self.env["stock.move"].create(
            {
                "product_id": product.id,
                "product_uom_qty": 1,
                "location_id": warehouse.lot_stock_id.id,
                "location_dest_id": customer.id,
            }
        )
        listener._export_stock_for_move(move)
        self.env.cr.execute(
            "UPDATE mercadolibre_warehouse_mapping "
            "SET location_id = NULL WHERE id = %s",
            (mapping.id,),
        )
        mapping.invalidate_recordset()
        listener._export_stock_for_move(move)
        binding.fulfillment = True
        self.backend.export_stock = True
        listener._export_stock_for_move(move)
        self.backend.export_stock = False
        listener._export_stock_for_move(move)
        self.assertEqual(fulfillment.stock_type, "fulfillment")
        other_warehouse = self.env["stock.warehouse"].create(
            {
                "name": "Second",
                "code": "SEC",
                "company_id": self.backend.company_id.id,
            }
        )
        self._mapping(warehouse=other_warehouse)
        self.backend.export_stock = True
        binding.fulfillment = False
        self._set_qty(product, 5, warehouse)
        move._action_confirm()
        move._action_assign()
        move.quantity = 1
        move.picked = True
        move._action_done()
        listener.on_record_create(move)
        listener._export_stock_for_move(move)

    def test_notification_helpers_cover_resources_quantities_and_bindings(self):
        items = self._handler("mercadolibre.notification.handler.items")
        self.assertEqual(items._resource_id("/items/MLA100", "items"), "MLA100")
        self.assertEqual(items._resource_id("/seller/MLA9", "items"), "MLA9")
        self.assertEqual(items._resource_id("/items", "items"), "items")
        self.assertEqual(items._resource_id("", "items"), "")
        self.assertEqual(items._resource_id(False, "items"), "")
        stock = self._handler("mercadolibre.notification.handler.stock")
        self.assertEqual(stock._quantity("nope"), 0.0)
        self.assertEqual(stock._quantity({"available_quantity": 0}), 0.0)
        self.assertEqual(stock._quantity({"available_quantity": 4}), 4)
        self.assertEqual(stock._quantity({"locations": []}), 0.0)
        self.assertEqual(stock._quantity({"quantity": 3}), 3)
        self.assertEqual(
            stock._quantity({"locations": [{"quantity": 1}, {"quantity": False}]}),
            1.0,
        )
        self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        notification = self._notification("/user-products/MLAU200/stock")
        self.assertEqual(stock._binding(notification, {}), binding)
        self.assertEqual(
            stock._binding(notification, {"user_product_id": "MLAU200"}),
            binding,
        )
        notification.resource = "/items/MLA200"
        self.assertEqual(stock._binding(notification, {}), binding)
        notification.resource = "/warehouses/1"
        self.assertFalse(stock._binding(notification, []))
        notification.resource = "/user-products"
        self.assertFalse(stock._binding(notification, {}))

    def test_catalog_buttons_require_a_manager_and_enqueue_jobs(self):
        user = self._plain_user()
        with self.assertRaises(AccessError):
            self.backend.with_user(user).button_import_listings()
        with self.assertRaises(AccessError):
            self.backend.with_user(user).button_refresh_categories()
        manager = self._manager()
        self.backend.with_user(manager).button_import_listings()
        self.backend.with_user(manager).button_refresh_categories()
        self.assertTrue(self._jobs(f"meli:listings:{self.backend.id}"))
        self.assertTrue(self._jobs(f"meli:categories:{self.backend.id}"))
        self.backend.import_products = False
        self.assertIsNone(self.backend._job_import_listings())
        self.backend.import_products = True
        other = self.env["mercadolibre.backend"].create(
            {
                "name": "Other seller",
                "site_id": "MLM",
                "client_id": "other",
                "client_secret": "other-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
                "import_products": False,
            }
        )
        self.env["mercadolibre.backend"].cron_import_listings()
        self.assertTrue(self._jobs(f"meli:listings:{self.backend.id}"))
        self.assertFalse(self._jobs(f"meli:listings:{other.id}"))

    def test_listing_actions_match_export_and_count_bindings(self):
        self.env["mercadolibre.product.product"].init()
        bare = self._product("SKU-BARE")
        product = self._product("SKU-LEGACY")
        binding = self._import_item(self.item_legacy)
        user = self._plain_user()
        with self.assertRaises(AccessError):
            binding.with_user(user).button_match()
        with self.assertRaises(AccessError):
            binding.with_user(user).button_export_price()
        with self.assertRaises(AccessError):
            binding.with_user(user).button_export_stock()
        unbound = self._import_item(
            self._copy_item(
                self.item_legacy,
                id="MLA500",
                attributes=[],
                seller_custom_field="",
            )
        )
        unbound.seller_sku = False
        manager = self._manager()
        unbound.with_user(manager).button_match()
        self.assertFalse(unbound.odoo_id)
        unbound.seller_sku = "SKU-BARE"
        unbound.with_user(manager).button_match()
        self.assertEqual(unbound.odoo_id, bare)
        binding.with_user(manager).button_export_price()
        self.assertTrue(self._jobs(f"meli:price:{self.backend.id}:{binding.id}"))
        warehouse = self._warehouse()
        self._mapping(warehouse=warehouse)
        self._mapping(stock_type="fulfillment", warehouse=warehouse)
        binding.with_user(manager).button_export_stock()
        seller = self.backend.warehouse_mapping_ids.filtered(
            lambda mapping: mapping.stock_type == "seller_warehouse"
        )
        self.assertTrue(
            self._jobs(f"meli:stock:{self.backend.id}:{binding.id}:{seller.id}")
        )
        action = self.backend.action_view_products()
        self.assertEqual(action["domain"], [("backend_id", "=", self.backend.id)])
        product_action = product.action_view_mercadolibre_bindings()
        self.assertEqual(product_action["domain"], [("odoo_id", "in", product.ids)])
        template_action = product.product_tmpl_id.action_view_mercadolibre_bindings()
        self.assertIn(product.id, template_action["domain"][0][2])
        lonely = self._product("SKU-LONELY")
        counted = (product | lonely).mapped("mercadolibre_bind_count")
        self.assertEqual(counted, [1, 0])
        templates = (product.product_tmpl_id | lonely.product_tmpl_id).mapped(
            "mercadolibre_bind_count"
        )
        self.assertEqual(templates, [1, 0])
        empty_backend = self.env["mercadolibre.backend"].create(
            {
                "name": "Empty",
                "site_id": "MLM",
                "client_id": "empty",
                "client_secret": "empty-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
            }
        )
        counts = (self.backend | empty_backend).mapped("product_binding_count")
        self.assertEqual(counts, [2, 0])
        self.env["mercadolibre.backend"].browse()._compute_product_binding_count()
        self.env["product.product"].browse()._compute_mercadolibre_bind_count()
        self.env["product.template"].browse()._compute_mercadolibre_bind_count()
        urls = binding.picture_url_text
        self.assertIn("legacy.jpg", urls)
        binding.picture_urls = {"not": "a list"}
        self.assertFalse(binding.picture_url_text)
        transport = Transport(
            [
                FakeResponse(200, self.item_legacy),
                FakeResponse(200, self.item_legacy),
            ]
        )
        self.backend.with_context(mercadolibre_transport=transport)._job_import_item(
            "MLA100"
        )
        binding.with_context(mercadolibre_transport=transport)._job_import()

    def test_category_sync_updates_parents_and_skips_repeats(self):
        details = {
            "MLA12": {
                "id": "MLA12",
                "name": "Parent",
                "listing_allowed": True,
                "children_categories": [
                    {
                        "id": "MLA13",
                        "name": "Child",
                        "listing_allowed": False,
                        "children_categories": [],
                    },
                    {"id": "MLA12"},
                ],
            }
        }
        adapter = CategoryAdapter(details, attributes=[{"id": "BRAND"}])
        categories = self.env["mercadolibre.category"]
        categories._sync_nodes(self.backend, None, adapter)
        categories._sync_nodes(
            self.backend,
            [{"id": "MLA12"}, {"id": "MLA12"}, {}],
            adapter,
        )
        parent = categories.search([("external_id", "=", "MLA12")])
        child = categories.search([("external_id", "=", "MLA13")])
        self.assertEqual(child.parent_id, parent)
        self.assertEqual(parent.attribute_schema, [{"id": "BRAND"}])
        self.assertFalse(child.attribute_schema)
        adapter.details["MLA12"]["name"] = "Renamed"
        categories._sync_nodes(
            self.backend,
            [
                {
                    "id": "MLA12",
                    "name": "Renamed",
                    "listing_allowed": True,
                    "children_categories": [],
                }
            ],
            adapter,
        )
        self.assertEqual(parent.name, "Renamed")
        transport = Transport(
            [
                FakeResponse(200, [{"id": "MLA20"}]),
                FakeResponse(
                    200,
                    {
                        "id": "MLA20",
                        "name": "Fetched",
                        "listing_allowed": False,
                        "children_categories": [],
                    },
                ),
            ]
        )
        self.backend.with_context(
            mercadolibre_transport=transport
        )._job_refresh_categories()
        self.assertTrue(categories.search([("external_id", "=", "MLA20")]))
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {
                        "results": [
                            {
                                "id": "MLA21",
                                "name": "Wrapped",
                                "listing_allowed": False,
                                "children_categories": [],
                            }
                        ]
                    },
                )
            ]
        )
        self.backend.with_context(
            mercadolibre_transport=transport
        )._job_refresh_categories()
        self.assertTrue(categories.search([("external_id", "=", "MLA21")]))
        transport = Transport([FakeResponse(200, {})])
        self.backend.with_context(
            mercadolibre_transport=transport
        )._job_refresh_categories()
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {
                        "categories": [
                            {
                                "id": "MLA22",
                                "name": "Listed",
                                "listing_allowed": True,
                                "children_categories": [],
                            }
                        ]
                    },
                ),
                FakeResponse(200, [{"id": "MODEL"}]),
            ]
        )
        self.backend.with_context(
            mercadolibre_transport=transport
        )._job_refresh_categories()
        listed = categories.search([("external_id", "=", "MLA22")])
        self.assertEqual(listed.attribute_schema, [{"id": "MODEL"}])
