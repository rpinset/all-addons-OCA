import re

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.operability import (
    identity_key_pattern,
    missing_scopes,
    scope_handles,
    state_count_label,
)


class TestShopifyLibOperability(TransactionCase):
    def test_scope_diff_is_normalized_sorted_and_deduplicated(self):
        granted = {"read_orders", "write_products"}
        assert missing_scopes(
            granted, ["write_products", "read_products", "read_orders"]
        ) == ("read_products",)

    def test_scope_handles_ignores_invalid_entries(self):
        payload = {
            "currentAppInstallation": {
                "accessScopes": [
                    {"handle": "read_orders"},
                    {},
                    None,
                    {"handle": " write_products "},
                ]
            }
        }
        assert scope_handles(payload) == {"read_orders", "write_products"}

    def test_state_count_label_has_stable_order(self):
        assert (
            state_count_label({"error": 2, "synced": 9, "pending": 1})
            == "9 synced · 1 pending · 2 errors"
        )

    def test_the_store_of_a_job_is_the_first_id_of_its_key(self):
        def store_2(key):
            return bool(re.search(identity_key_pattern(2), key))

        assert store_2("shopify.inventory.locations.2")
        assert store_2("shopify.customer.export.2.1")
        assert store_2("shopify.inventory.delta.2.15.1")
        assert store_2("shopify.b2b.import.2")
        assert store_2("shopify.orders.bulk.2.False.False")
        assert store_2("shopify.retry.shopify.product.template.2.9.0a1b2c3d")
        assert not store_2("shopify.customer.export.1.2")
        assert not store_2("shopify.inventory.delta.1.2.7")
        assert not store_2("shopify.inventory.locations.21")
        assert not store_2("other.module.2")
