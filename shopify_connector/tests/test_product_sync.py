from unittest.mock import Mock, patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from ..lib.product import merge_owned_fields


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
