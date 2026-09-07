from datetime import datetime, timedelta, timezone

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.inventory import (
    apply_negative_policy,
    build_inventory_set_payload,
    diff_inventory_levels,
    quantity_for_basis,
    should_ignore_echo,
)


class TestShopifyLibInventory(TransactionCase):
    def test_level_diff_reports_only_shared_drift_in_stable_order(self):
        desired = {("item-b", "location"): 4, ("item-a", "location"): 7}
        remote = {
            ("item-a", "location"): 5,
            ("item-b", "location"): 4,
            ("remote-only", "location"): 9,
        }
        assert diff_inventory_levels(desired, remote) == [
            {"key": ("item-a", "location"), "desired": 7, "remote": 5, "delta": 2}
        ]

    def test_echo_guard_requires_same_recent_quantity(self):
        now = datetime(2026, 7, 29, 12, tzinfo=timezone.utc)
        assert should_ignore_echo(8, 8, now - timedelta(seconds=30), now=now)
        assert not should_ignore_echo(7, 8, now - timedelta(seconds=30), now=now)
        assert not should_ignore_echo(8, 8, now - timedelta(minutes=6), now=now)
        assert not should_ignore_echo(8, None, None, now=now)

    def test_quantity_basis_selection_and_rounding(self):
        assert quantity_for_basis(3.6, 8.2, "free_qty") == 4
        assert quantity_for_basis(3.6, 8.2, "qty_available") == 8
        assert quantity_for_basis(-1.5, 0, "free_qty") == -2
        with self.assertRaises(ValueError):
            quantity_for_basis(1, 2, "forecast")

    def test_negative_policy_and_compare_payload(self):
        assert apply_negative_policy(-3, False) == (0, True)
        assert apply_negative_policy(-3, True) == (-3, False)
        assert build_inventory_set_payload(
            "gid://shopify/InventoryItem/1",
            "gid://shopify/Location/2",
            9,
            7,
            reference_document_uri="odoo://inventory/1/2",
        ) == {
            "name": "available",
            "reason": "correction",
            "referenceDocumentUri": "odoo://inventory/1/2",
            "quantities": [
                {
                    "inventoryItemId": "gid://shopify/InventoryItem/1",
                    "locationId": "gid://shopify/Location/2",
                    "quantity": 9,
                    "compareQuantity": 7,
                }
            ],
        }
