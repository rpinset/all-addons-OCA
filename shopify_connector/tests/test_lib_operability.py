from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.operability import (
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
