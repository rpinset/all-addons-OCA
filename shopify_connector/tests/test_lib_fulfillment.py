from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.fulfillment import (
    FulfillmentAllocationError,
    allocate_fulfillment_lines,
    build_tracking_payload,
)


def _order(order_id, location_id, line_id, remaining, *, move=False, held=False):
    return {
        "id": order_id,
        "location_id": location_id,
        "status": "ON_HOLD" if held else "OPEN",
        "held": held,
        "supported_actions": ["MOVE"] if move else [],
        "line_items": [
            {
                "id": f"{order_id}-line",
                "line_id": line_id,
                "remaining_quantity": remaining,
            }
        ],
    }


class TestShopifyLibFulfillment(TransactionCase):
    def test_allocation_splits_partial_across_fulfillment_orders(self):
        result = allocate_fulfillment_lines(
            [{"move_id": 7, "line_id": "line-1", "quantity": 5}],
            [
                _order("fo-1", "location-1", "line-1", 2),
                _order("fo-2", "location-1", "line-1", 4),
            ],
            target_location_id="location-1",
        )
        assert result["groups"] == [
            {
                "fulfillment_order_id": "fo-1",
                "location_id": "location-1",
                "move_required": False,
                "line_items": [{"id": "fo-1-line", "quantity": 2}],
            },
            {
                "fulfillment_order_id": "fo-2",
                "location_id": "location-1",
                "move_required": False,
                "line_items": [{"id": "fo-2-line", "quantity": 3}],
            },
        ]
        assert result["warnings"] == []

    def test_allocation_marks_movable_location_mismatch(self):
        result = allocate_fulfillment_lines(
            [{"name": "Widget", "line_id": "line-1", "quantity": 1}],
            [_order("fo-1", "location-2", "line-1", 1, move=True)],
            target_location_id="location-1",
        )
        assert result["move_fulfillment_order_ids"] == ["fo-1"]
        assert result["groups"][0]["move_required"] is True

    def test_over_delivery_clamps_to_shopify_remaining(self):
        result = allocate_fulfillment_lines(
            [{"name": "Widget", "line_id": "line-1", "quantity": 5}],
            [_order("fo-1", "location-1", "line-1", 2)],
            target_location_id="location-1",
        )
        assert result["groups"][0]["line_items"][0]["quantity"] == 2
        assert "clamped" in result["warnings"][0]

    def test_missing_binding_line_is_actionable(self):
        with self.assertRaisesRegex(
            FulfillmentAllocationError, "no Shopify order-line"
        ):
            allocate_fulfillment_lines(
                [{"name": "Widget", "quantity": 1}], [], target_location_id="location-1"
            )

    def test_held_and_unmovable_orders_are_not_allocated(self):
        with self.assertRaisesRegex(FulfillmentAllocationError, "cannot be fulfilled"):
            allocate_fulfillment_lines(
                [{"name": "Widget", "line_id": "line-1", "quantity": 1}],
                [
                    _order("fo-held", "location-1", "line-1", 1, held=True),
                    _order("fo-other", "location-2", "line-1", 1),
                ],
                target_location_id="location-1",
            )

    def test_location_mismatch_is_not_misreported_as_over_delivery(self):
        with self.assertRaisesRegex(FulfillmentAllocationError, "MOVE is unavailable"):
            allocate_fulfillment_lines(
                [{"name": "Widget", "line_id": "line-1", "quantity": 3}],
                [
                    _order("fo-local", "location-1", "line-1", 1),
                    _order("fo-other", "location-2", "line-1", 2),
                ],
                target_location_id="location-1",
            )

    def test_tracking_payload_omits_blanks_and_strips_values(self):
        assert build_tracking_payload("  1Z99 ", " UPS ", "") == {
            "number": "1Z99",
            "company": "UPS",
        }
