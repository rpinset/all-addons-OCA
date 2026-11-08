from unittest.mock import Mock, patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from ..lib.product import merge_owned_fields
from ..models.product_sync import ShopifyProductTemplateSync
from .common import (
    MAIN_IMAGE_ID,
    SHARED_IMAGE_ID,
    VARIANT_IMAGE_ID,
    download_test_image,
    image_product_payload,
)


class TestShopifyProductSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Product Shop",
                "shop_url": "product-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"

    def test_matching_prefers_barcode_before_sku(self):
        barcode_product = self.env["product.product"].create(
            {
                "name": "Barcode Product",
                "barcode": "MATCH-BARCODE",
                "company_id": self.instance.company_id.id,
            }
        )
        self.env["product.product"].create(
            {
                "name": "SKU Product",
                "default_code": "MATCH-SKU",
                "company_id": self.instance.company_id.id,
            }
        )
        payload = {
            "variants": [
                {
                    "barcode": "MATCH-BARCODE",
                    "sku": "MATCH-SKU",
                }
            ]
        }

        matched = self.env["shopify.product.template"]._match_odoo_template(
            self.instance, payload
        )

        self.assertEqual(matched, barcode_product.product_tmpl_id)

    def test_matching_uses_sku_when_barcode_is_absent(self):
        sku_product = self.env["product.product"].create(
            {
                "name": "SKU Product",
                "default_code": "ONLY-SKU",
                "company_id": self.instance.company_id.id,
            }
        )

        matched = self.env["shopify.product.template"]._match_odoo_template(
            self.instance,
            {"variants": [{"barcode": "", "sku": "ONLY-SKU"}]},
        )

        self.assertEqual(matched, sku_product.product_tmpl_id)

    def test_default_ownership_and_merge_preserve_owner_side(self):
        self.assertEqual(
            self.instance._product_field_owners(),
            {
                "name": "odoo",
                "description": "odoo",
                "price": "odoo",
                "images": "odoo",
                "status": "shopify",
            },
        )
        merged = merge_owned_fields(
            {"name": "Odoo", "status": "DRAFT"},
            {"name": "Shopify", "status": "ACTIVE"},
            self.instance._product_field_owners(),
            source="shopify",
        )
        self.assertEqual(merged, {"name": "Odoo", "status": "ACTIVE"})

    def test_product_webhook_dispatch_queues_gid_keyed_import(self):
        event = self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": "product-webhook-1",
                "topic": "products/update",
                "payload": {
                    "admin_graphql_api_id": "gid://shopify/Product/42",
                    "title": "Webhook Product",
                    "variants": [],
                    "options": [],
                    "images": [],
                },
            }
        )
        delayed = Mock()
        product_model_class = type(self.env["shopify.product.template"])

        with patch.object(
            product_model_class,
            "with_delay",
            autospec=True,
            return_value=delayed,
        ) as with_delay:
            event._dispatch()

        self.assertEqual(event.state, "done")
        self.assertIn(
            "gid://shopify/Product/42",
            with_delay.call_args.kwargs["identity_key"],
        )
        delayed._job_import_product_from_api.assert_called_once()

    def test_export_uses_mock_client_and_creates_bindings(self):
        product = self.env["product.product"].create(
            {
                "name": "Export Product",
                "default_code": "EXPORT-1",
                "barcode": "90001",
                "list_price": 25,
                "company_id": self.instance.company_id.id,
            }
        )
        client = Mock()
        exported_product = {
            "id": "gid://shopify/Product/90",
            "title": "Export Product",
            "handle": "export-product",
            "status": "ACTIVE",
            "updatedAt": "2026-07-29T00:00:00Z",
            "variants": {
                "nodes": [
                    {
                        "id": "gid://shopify/ProductVariant/91",
                        "sku": "EXPORT-1",
                        "barcode": "90001",
                        "price": "25.00",
                        "selectedOptions": [
                            {
                                "name": "Title",
                                "value": "Default Title",
                            }
                        ],
                    }
                ],
                "pageInfo": {"hasNextPage": False, "endCursor": "v1"},
            },
            "media": {
                "nodes": [],
                "pageInfo": {"hasNextPage": False, "endCursor": None},
            },
            "collections": {
                "nodes": [],
                "pageInfo": {"hasNextPage": False, "endCursor": None},
            },
        }
        client.execute.side_effect = [
            {"metafieldDefinition": None},
            {
                "metafieldDefinitionCreate": {
                    "createdDefinition": {"id": "gid://shopify/MetafieldDefinition/1"}
                }
            },
            {
                "productSet": {
                    "product": {
                        "id": "gid://shopify/Product/90",
                    }
                }
            },
            {"product": exported_product},
        ]
        instance_model_class = type(self.instance)

        with patch.object(
            instance_model_class,
            "_shopify_client",
            autospec=True,
            return_value=client,
        ):
            binding_id = self.env["shopify.product.template"]._job_export_product(
                self.instance.id, product.product_tmpl_id.id
            )

        binding = self.env["shopify.product.template"].browse(binding_id)
        self.assertEqual(binding.shopify_id, "gid://shopify/Product/90")
        self.assertEqual(
            binding.variant_binding_ids.shopify_id,
            "gid://shopify/ProductVariant/91",
        )
        self.assertEqual(client.execute.call_count, 4)
        definition_variables = client.execute.call_args_list[1].args[1]
        self.assertEqual(definition_variables["definition"]["type"], "id")
        product_set_variables = client.execute.call_args_list[2].args[1]
        self.assertEqual(
            product_set_variables["input"]["productOptions"],
            [
                {
                    "name": "Title",
                    "position": 1,
                    "values": [{"name": "Default Title"}],
                }
            ],
        )
        self.assertEqual(
            product_set_variables["input"]["variants"][0]["optionValues"],
            [{"optionName": "Title", "name": "Default Title"}],
        )
        database_uuid = (
            self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        )
        self.assertEqual(
            product_set_variables["identifier"],
            {
                "customId": {
                    "key": "odoo_product_id",
                    "value": (
                        f"{database_uuid or self.env.cr.dbname}:"
                        f"{self.instance.id}:"
                        f"{product.product_tmpl_id.id}"
                    ),
                }
            },
        )

    def test_repeated_sparse_import_preserves_variant_binding_identity(self):
        payload = {
            "id": "gid://shopify/Product/500",
            "name": "Sparse Shirt",
            "description": "",
            "handle": "sparse-shirt",
            "status": "DRAFT",
            "updated_at": "2026-07-29T00:00:00Z",
            "options": [
                {
                    "id": "gid://shopify/ProductOption/1",
                    "name": "Color",
                    "position": 1,
                    "values": ["Blue", "Red"],
                },
                {
                    "id": "gid://shopify/ProductOption/2",
                    "name": "Size",
                    "position": 2,
                    "values": ["S", "M"],
                },
            ],
            "variants": [
                {
                    "id": "gid://shopify/ProductVariant/501",
                    "title": "Blue / S",
                    "sku": "BLUE-S",
                    "barcode": "",
                    "price": "10.00",
                    "selected_options": [
                        {"name": "Color", "value": "Blue"},
                        {"name": "Size", "value": "S"},
                    ],
                    "media_ids": [],
                    "updated_at": "2026-07-29T00:00:00Z",
                },
                {
                    "id": "gid://shopify/ProductVariant/502",
                    "title": "Red / M",
                    "sku": "RED-M",
                    "barcode": "",
                    "price": "12.00",
                    "selected_options": [
                        {"name": "Color", "value": "Red"},
                        {"name": "Size", "value": "M"},
                    ],
                    "media_ids": [],
                    "updated_at": "2026-07-29T00:00:00Z",
                },
            ],
            "images": [],
            "collections": [],
        }
        binding_model = self.env["shopify.product.template"]

        binding_id = binding_model._job_import_product(
            self.instance.id, payload, payload_normalized=True
        )
        binding = binding_model.browse(binding_id)
        first_ids = binding.variant_binding_ids.ids
        first_variant_ids = binding.variant_binding_ids.odoo_id.ids

        binding_model._job_import_product(
            self.instance.id, payload, payload_normalized=True
        )

        self.assertEqual(binding.variant_binding_ids.ids, first_ids)
        self.assertEqual(binding.variant_binding_ids.odoo_id.ids, first_variant_ids)
        self.assertEqual(len(binding.variant_binding_ids), 2)
        self.assertEqual(len(binding.odoo_id.product_variant_ids), 2)

    def test_import_rebinds_variant_recreated_under_new_gid(self):
        def variant(gid, color, sku):
            return {
                "id": gid,
                "title": color,
                "sku": sku,
                "barcode": "",
                "price": "10.00",
                "selected_options": [{"name": "Color", "value": color}],
                "media_ids": [],
                "updated_at": "2026-07-29T00:00:00Z",
            }

        payload = {
            "id": "gid://shopify/Product/700",
            "name": "Recreated Shirt",
            "description": "",
            "handle": "recreated-shirt",
            "status": "ACTIVE",
            "updated_at": "2026-07-29T00:00:00Z",
            "options": [
                {
                    "id": "gid://shopify/ProductOption/7",
                    "name": "Color",
                    "position": 1,
                    "values": ["Blue", "Red"],
                }
            ],
            "variants": [
                variant("gid://shopify/ProductVariant/701", "Blue", "BLUE"),
                variant("gid://shopify/ProductVariant/702", "Red", "RED"),
            ],
            "images": [],
            "collections": [],
        }
        binding_model = self.env["shopify.product.template"]
        binding = binding_model.browse(
            binding_model._job_import_product(
                self.instance.id, payload, payload_normalized=True
            )
        )
        blue_binding = binding.variant_binding_ids.filtered(
            lambda item: item.shopify_id == "gid://shopify/ProductVariant/701"
        )
        blue_variant = blue_binding.odoo_id

        # Shopify recreates the Blue variant under a new GID.
        payload["updated_at"] = "2026-07-30T00:00:00Z"
        payload["variants"][0] = variant(
            "gid://shopify/ProductVariant/801", "Blue", "BLUE-2"
        )
        result = binding_model._job_import_product(
            self.instance.id, payload, payload_normalized=True
        )

        self.assertEqual(result, binding.id, binding.error_message)
        self.assertEqual(binding.state, "synced")
        self.assertEqual(len(binding.variant_binding_ids), 2)
        self.assertEqual(blue_binding.shopify_id, "gid://shopify/ProductVariant/801")
        self.assertEqual(blue_binding.odoo_id, blue_variant)
        self.assertEqual(blue_binding.sku_snapshot, "BLUE-2")
        self.assertEqual(blue_variant.default_code, "BLUE-2")
        self.assertEqual(len(binding.odoo_id.product_variant_ids), 2)

    def test_company_change_is_blocked_after_product_sync(self):
        product = self.env["product.product"].create(
            {
                "name": "Bound Product",
                "company_id": self.instance.company_id.id,
            }
        )
        self.env["shopify.product.template"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Product/700",
                "odoo_id": product.product_tmpl_id.id,
            }
        )
        other_company = self.env["res.company"].create({"name": "Other Company"})

        with self.assertRaises(ValidationError):
            self.instance.company_id = other_company

    def test_cross_instance_bindings_keep_field_ownership_isolated(self):
        second = self.env["shopify.instance"].create(
            {
                "name": "Second Product Shop",
                "shop_url": "second-product-shop.myshopify.com",
                "access_token": "second-token",
                "webhook_secret": "second-secret",
            }
        )
        second.state = "connected"
        product = self.env["product.product"].create(
            {
                "name": "Shared SKU Product",
                "default_code": "SHARED-SKU",
                "company_id": self.instance.company_id.id,
            }
        )
        first_binding = self.env["shopify.product.template"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Product/801",
                "odoo_id": product.product_tmpl_id.id,
                "status": "ACTIVE",
            }
        )
        second_binding = self.env["shopify.product.template"].create(
            {
                "instance_id": second.id,
                "shopify_id": "gid://shopify/Product/802",
                "odoo_id": product.product_tmpl_id.id,
                "status": "ACTIVE",
            }
        )
        self.instance.field_mapping_ids.filtered(
            lambda mapping: mapping.field == "name"
        ).owner = "odoo"
        second.field_mapping_ids.filtered(
            lambda mapping: mapping.field == "name"
        ).owner = "shopify"
        existing = {
            "options": [],
            "media": {"nodes": []},
        }

        first_input, _files = self.env["shopify.product.template"]._product_set_input(
            self.instance,
            product.product_tmpl_id,
            first_binding,
            existing_product=existing,
        )
        second_input, _files = self.env["shopify.product.template"]._product_set_input(
            second,
            product.product_tmpl_id,
            second_binding,
            existing_product=existing,
        )

        self.assertEqual(first_input["title"], product.name)
        self.assertNotIn("title", second_input)
        self.assertEqual(first_binding.odoo_id, second_binding.odoo_id)
        self.assertEqual(
            first_input["variants"][0]["sku"],
            second_input["variants"][0]["sku"],
        )

    def _import_image_product(self):
        binding_model = self.env["shopify.product.template"]
        with patch.object(
            type(binding_model), "_download_image", side_effect=download_test_image
        ):
            return binding_model.browse(
                binding_model._job_import_product(
                    self.instance.id, image_product_payload(), payload_normalized=True
                )
            )

    def test_import_sets_main_and_exclusive_variant_images(self):
        binding = self._import_image_product()
        blue = binding.variant_binding_ids.filtered(
            lambda item: item.shopify_id == "gid://shopify/ProductVariant/701"
        )
        red = binding.variant_binding_ids - blue

        self.assertEqual(binding.state, "synced")
        self.assertTrue(binding.odoo_id.image_1920)
        self.assertEqual(binding.main_image_shopify_id, MAIN_IMAGE_ID)
        self.assertEqual(blue.image_shopify_id, VARIANT_IMAGE_ID)
        self.assertTrue(blue.odoo_id.image_variant_1920)
        self.assertFalse(red.image_shopify_id)
        self.assertFalse(red.odoo_id.image_variant_1920)

    def test_core_export_keeps_shopify_images_it_does_not_manage(self):
        binding = self._import_image_product()
        media = [
            {"id": image_id, "mediaContentType": "IMAGE"}
            for image_id in (MAIN_IMAGE_ID, VARIANT_IMAGE_ID, SHARED_IMAGE_ID)
        ] + [{"id": "gid://shopify/Video/1", "mediaContentType": "VIDEO"}]

        unmanaged_ids = ShopifyProductTemplateSync._unmanaged_shopify_image_ids(
            binding, binding, media
        )

        self.assertEqual(unmanaged_ids, [SHARED_IMAGE_ID])


class TestShopifyPricelistRuleExport(TransactionCase):
    """A rule in the store pricelist re-exports the bound products it prices."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Pricelist Shop",
                "shop_url": "pricelist-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        company = cls.instance.company_id
        cls.parent_category = cls.env["product.category"].create({"name": "Baby"})
        cls.category = cls.env["product.category"].create(
            {"name": "Blankets", "parent_id": cls.parent_category.id}
        )
        cls.bound, cls.unbound = cls.env["product.template"].create(
            [
                {
                    "name": "Bound Blanket",
                    "categ_id": cls.category.id,
                    "list_price": 25,
                    "company_id": company.id,
                },
                {
                    "name": "Unbound Blanket",
                    "categ_id": cls.category.id,
                    "list_price": 25,
                    "company_id": company.id,
                },
            ]
        )
        cls.env["shopify.product.template"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Product/900",
                "odoo_id": cls.bound.id,
                "status": "ACTIVE",
                "state": "synced",
            }
        )

    def _rule(self, **values):
        return {
            "pricelist_id": self.instance.product_pricelist_id.id,
            "compute_price": "fixed",
            "fixed_price": 22,
            **values,
        }

    def _queued_exports(self, action):
        binding_class = type(self.env["shopify.product.template"])
        with patch.object(binding_class, "_enqueue_product_export") as enqueue:
            action()
        return {(call.args[0], call.args[1]) for call in enqueue.call_args_list}

    def test_product_rule_exports_the_product(self):
        exports = self._queued_exports(
            lambda: self.env["product.pricelist.item"].create(
                self._rule(applied_on="1_product", product_tmpl_id=self.bound.id)
            )
        )

        self.assertEqual(exports, {(self.instance, self.bound)})

    def test_category_rule_exports_the_bound_products_of_subcategories(self):
        exports = self._queued_exports(
            lambda: self.env["product.pricelist.item"].create(
                self._rule(
                    applied_on="2_product_category",
                    categ_id=self.parent_category.id,
                )
            )
        )

        self.assertEqual(exports, {(self.instance, self.bound)})

    def test_global_rule_change_and_removal_export_the_bound_products(self):
        rule = self.env["product.pricelist.item"].create(
            self._rule(applied_on="3_global")
        )

        changed = self._queued_exports(lambda: rule.write({"fixed_price": 21}))
        removed = self._queued_exports(rule.unlink)

        self.assertEqual(changed, {(self.instance, self.bound)})
        self.assertEqual(removed, {(self.instance, self.bound)})

    def test_rule_in_another_pricelist_exports_nothing(self):
        other = self.env["product.pricelist"].create({"name": "Other"})

        exports = self._queued_exports(
            lambda: self.env["product.pricelist.item"].create(
                {
                    **self._rule(applied_on="1_product", product_tmpl_id=self.bound.id),
                    "pricelist_id": other.id,
                }
            )
        )

        self.assertFalse(exports)


class TestShopifyExportInventoryTracking(TransactionCase):
    """A variant created by the export is tracked, with its Odoo stock."""

    LOCATION_ID = "gid://shopify/Location/950"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Tracking Shop",
                "shop_url": "tracking-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        company = cls.instance.company_id
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", company.id)], limit=1
        )
        cls.env["shopify.location"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": cls.LOCATION_ID,
                "legacy_resource_id": "950",
                "name": "Main",
                "active": True,
                "state": "synced",
                "warehouse_id": cls.warehouse.id,
                "odoo_location_id": cls.warehouse.lot_stock_id.id,
            }
        )
        cls.storable = cls.env["product.product"].create(
            {
                "name": "Tracked Cloth",
                "default_code": "TRACK-1",
                "type": "consu",
                "is_storable": True,
                "company_id": company.id,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.storable, cls.warehouse.lot_stock_id, 7
        )

    def _variant_input(self, product, binding=None):
        product_input, _files = self.env["shopify.product.template"]._product_set_input(
            self.instance, product.product_tmpl_id, binding
        )
        return product_input["variants"][0]

    def _binding(self, product, *, with_variant):
        binding = self.env["shopify.product.template"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Product/960",
                "odoo_id": product.product_tmpl_id.id,
                "status": "ACTIVE",
                "state": "synced",
            }
        )
        if with_variant:
            self.env["shopify.product.variant"].create(
                {
                    "instance_id": self.instance.id,
                    "shopify_id": "gid://shopify/ProductVariant/961",
                    "template_binding_id": binding.id,
                    "odoo_id": product.id,
                }
            )
        return binding

    def test_new_storable_variant_is_tracked_with_its_stock(self):
        values = self._variant_input(self.storable)

        self.assertEqual(values["inventoryItem"], {"tracked": True})
        self.assertEqual(
            values["inventoryQuantities"],
            [{"locationId": self.LOCATION_ID, "name": "available", "quantity": 7}],
        )

    def test_existing_variant_keeps_its_shopify_inventory_settings(self):
        binding = self._binding(self.storable, with_variant=True)

        values = self._variant_input(self.storable, binding)

        self.assertNotIn("inventoryItem", values)
        self.assertNotIn("inventoryQuantities", values)

    def test_new_variant_of_a_product_without_stock_sync_is_not_tracked(self):
        binding = self._binding(self.storable, with_variant=False)
        binding.inventory_sync_enabled = False

        values = self._variant_input(self.storable, binding)

        self.assertNotIn("inventoryItem", values)

    def test_service_is_not_tracked(self):
        service = self.env["product.product"].create(
            {
                "name": "Gift wrap",
                "type": "service",
                "company_id": self.instance.company_id.id,
            }
        )

        values = self._variant_input(service)

        self.assertNotIn("inventoryItem", values)
