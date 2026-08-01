from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.product import (
    ShopifyProductPayloadError,
    merge_owned_fields,
    normalize_bulk_products,
    normalize_product_payload,
    parse_jsonl,
    sign_product_image_path,
    verify_product_image_signature,
)


class TestShopifyLibProduct(TransactionCase):
    def test_webhook_product_normalizes_variants_options_and_images(self):
        payload = {
            "id": 123,
            "title": "Trail Shoe",
            "body_html": "<p>Fast</p>",
            "handle": "trail-shoe",
            "status": "active",
            "options": [{"id": 1, "name": "Size", "position": 1, "values": ["S", "M"]}],
            "variants": [
                {
                    "id": 456,
                    "sku": "SHOE-S",
                    "barcode": "10001",
                    "price": "79.90",
                    "option1": "S",
                }
            ],
            "images": [
                {
                    "admin_graphql_api_id": "gid://shopify/MediaImage/88",
                    "src": "https://cdn.example/shoe.jpg",
                    "alt": "Trail shoe",
                }
            ],
        }
        product = normalize_product_payload(payload)
        assert product["id"] == "gid://shopify/Product/123"
        assert product["status"] == "ACTIVE"
        assert product["options"][0]["values"] == ["S", "M"]
        assert product["variants"][0] == {
            "id": "gid://shopify/ProductVariant/456",
            "title": "",
            "sku": "SHOE-S",
            "barcode": "10001",
            "price": "79.90",
            "selected_options": [{"name": "Size", "value": "S"}],
            "media_ids": [],
            "inventory_item_id": "",
            "inventory_tracked": False,
            "updated_at": None,
        }
        assert product["images"][0]["id"] == "gid://shopify/MediaImage/88"

    def test_graphql_edges_are_normalized(self):
        payload = {
            "id": "gid://shopify/Product/1",
            "title": "Mug",
            "options": {
                "nodes": [
                    {
                        "id": "gid://shopify/ProductOption/2",
                        "name": "Color",
                        "position": 1,
                        "optionValues": [{"name": "Blue"}],
                    }
                ]
            },
            "variants": {
                "edges": [
                    {
                        "node": {
                            "id": "gid://shopify/ProductVariant/3",
                            "price": "12.00",
                            "inventoryItem": {
                                "id": "gid://shopify/InventoryItem/30",
                                "tracked": True,
                            },
                            "selectedOptions": [{"name": "Color", "value": "Blue"}],
                            "media": {"nodes": [{"id": "gid://shopify/MediaImage/4"}]},
                        }
                    }
                ]
            },
            "media": {
                "nodes": [
                    {
                        "id": "gid://shopify/MediaImage/4",
                        "image": {"url": "https://cdn.example/mug.jpg"},
                    }
                ]
            },
        }
        product = normalize_product_payload(payload)
        assert product["variants"][0]["selected_options"] == [
            {"name": "Color", "value": "Blue"}
        ]
        assert product["variants"][0]["media_ids"] == ["gid://shopify/MediaImage/4"]
        assert (
            product["variants"][0]["inventory_item_id"]
            == "gid://shopify/InventoryItem/30"
        )
        assert product["variants"][0]["inventory_tracked"] is True
        assert product["images"][0]["url"] == "https://cdn.example/mug.jpg"

    def test_normalization_is_idempotent_for_media_and_smart_collections(self):
        normalized = normalize_product_payload(
            {
                "id": "gid://shopify/Product/1",
                "title": "Mug",
                "variants": [
                    {
                        "id": "gid://shopify/ProductVariant/2",
                        "price": "5.00",
                        "selected_options": [{"name": "Color", "value": "Blue"}],
                        "media_ids": ["gid://shopify/MediaImage/3"],
                    }
                ],
                "images": [
                    {
                        "id": "gid://shopify/MediaImage/3",
                        "url": "https://cdn.example/mug.jpg",
                        "alt": "Mug",
                    }
                ],
                "collections": [
                    {
                        "id": "gid://shopify/Collection/4",
                        "name": "Automatic",
                        "type": "smart",
                    }
                ],
            }
        )
        assert normalize_product_payload(normalized) == normalized

    def test_product_image_signatures_are_scoped_and_timing_safe(self):
        signature = sign_product_image_path(
            "secret", 4, "product.template", 9, "abc123"
        )
        assert verify_product_image_signature(
            signature, "secret", 4, "product.template", 9, "abc123"
        )
        assert not verify_product_image_signature(
            signature, "secret", 4, "product.template", 10, "abc123"
        )

    def test_bulk_rows_reassemble_even_when_media_precedes_variant(self):
        records = [
            {
                "id": "gid://shopify/Product/1",
                "title": "Hat",
                "status": "ACTIVE",
                "options": [
                    {"name": "Size", "position": 1, "optionValues": [{"name": "M"}]}
                ],
            },
            {
                "id": "gid://shopify/MediaImage/3",
                "__parentId": "gid://shopify/ProductVariant/2",
                "image": {"url": "https://cdn.example/hat.jpg"},
            },
            {
                "id": "gid://shopify/ProductVariant/2",
                "__parentId": "gid://shopify/Product/1",
                "sku": "HAT-M",
                "price": "10.00",
                "selectedOptions": [{"name": "Size", "value": "M"}],
            },
            {
                "id": "gid://shopify/Collection/4",
                "__parentId": "gid://shopify/Product/1",
                "title": "Summer",
                "ruleSet": None,
            },
        ]
        products = normalize_bulk_products(records)
        assert len(products) == 1
        assert products[0]["variants"][0]["media_ids"] == ["gid://shopify/MediaImage/3"]
        assert products[0]["collections"][0]["type"] == "custom"

    def test_bulk_rows_accept_a_single_pass_generator(self):
        records = (
            record
            for record in [
                {
                    "id": "gid://shopify/Product/1",
                    "title": "Generated",
                    "status": "ACTIVE",
                },
                {
                    "id": "gid://shopify/ProductVariant/2",
                    "__parentId": "gid://shopify/Product/1",
                    "price": "1.00",
                },
            ]
        )
        products = normalize_bulk_products(records)
        assert products[0]["name"] == "Generated"
        assert products[0]["variants"][0]["id"].endswith("/2")

    def test_ownership_merge_only_accepts_the_authoritative_side(self):
        owners = {
            "name": "odoo",
            "description": "shopify",
            "price": "odoo",
            "images": "shopify",
            "status": "shopify",
        }
        current = {
            "name": "Odoo Name",
            "description": "Old",
            "price": "10.00",
            "images": ["old"],
            "status": "DRAFT",
        }
        incoming = {
            "name": "Shopify Name",
            "description": "New",
            "price": "12.00",
            "images": ["new"],
            "status": "ACTIVE",
        }
        merged = merge_owned_fields(current, incoming, owners, source="shopify")
        assert merged == {
            "name": "Odoo Name",
            "description": "New",
            "price": "10.00",
            "images": ["new"],
            "status": "ACTIVE",
        }

    def test_ownership_merge_can_seed_a_missing_non_owner_value(self):
        owners = {
            "name": "odoo",
            "description": "shopify",
            "price": "odoo",
            "images": "shopify",
            "status": "shopify",
        }
        assert merge_owned_fields(
            {},
            {"name": "Initial", "status": "ACTIVE"},
            owners,
            source="shopify",
            seed_missing=True,
        ) == {"name": "Initial", "status": "ACTIVE"}

    def test_jsonl_accepts_bom_bytes_and_blank_lines(self):
        content = b'\xef\xbb\xbf{"id": 1}\n\n{"id": 2}\r\n'
        assert parse_jsonl(content) == [{"id": 1}, {"id": 2}]

    def test_jsonl_rejects_malformed_lines_1(self):
        content, message = ('{"id": 1}\nnot-json', "line 2")
        with self.assertRaisesRegex(ShopifyProductPayloadError, message):
            parse_jsonl(content)

    def test_jsonl_rejects_malformed_lines_2(self):
        content, message = ('{"id": 1}\n[]', "line 2")
        with self.assertRaisesRegex(ShopifyProductPayloadError, message):
            parse_jsonl(content)

    def test_jsonl_rejects_malformed_lines_3(self):
        content, message = ([object()], "line 1")
        with self.assertRaisesRegex(ShopifyProductPayloadError, message):
            parse_jsonl(content)
