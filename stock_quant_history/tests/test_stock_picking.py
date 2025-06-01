# Copyright 2025 Foodles (https://www.foodles.co/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from freezegun import freeze_time
from setuptools.config._validate_pyproject import ValidationError

from odoo.tests import tagged, users

from . import common


@tagged("post_install", "-at_install")
@freeze_time("2022-06-01 12:00+00")
class TestStockPickingLock(common.TestStockQuantHistoryCommon):
    """Test the lock constraint functionality on picking.
          ┌────────────────────────┐
          │(unlock, no history) TC3│
          ▼                        │
    ┌───────────┐            ┌─────┴─────┐
    │ Unlocked  ├───────────►│  Locked   │
    └───────────┘ (lock) TC1 └─────┬─────┘
                                   │
    (unlock, history exists) TC2   ▼
                             ┌───────────┐
                             │ Exception │
                             └───────────┘
    """

    def setUp(self):
        super().setUp()
        customer_location = self.env.ref("stock.stock_location_customers")
        # prepare a snapshot
        self.picking = self.env["stock.picking"].create(
            {
                "name": "Test Picking",
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.location.id,
                "location_dest_id": customer_location.id,
                "is_locked": False,
            }
        )
        self.move_line = self.env["stock.move.line"].create(
            {
                "product_id": self.product.id,
                "location_id": self.location.id,
                "location_dest_id": customer_location.id,
                "picking_id": self.picking.id,
                "product_uom_id": self.product.uom_id.id,
                "product_uom_qty": 1,
                "lot_id": self.lot.id,
            }
        )

    @users("stock_manager")
    def test1_lock_unlock_without_history(self):
        """Test the lock functionality."""
        # Assign and confirm the picking to be locked
        self.picking.action_assign()
        self.picking.action_confirm()
        # This picking should be unlocked (no changes on standard behavior)
        self.picking.write({"is_locked": True})
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        self.picking.write({"is_locked": False})
        self.assertFalse(
            self.picking.is_locked, "The picking should be unlocked after toggling."
        )

    @users("stock_manager")
    def test2_unlock_with_history(self):
        """Test the unlock functionality with history."""
        # Validate and finish the picking to be locked
        self.picking.action_assign()
        self.picking.action_confirm()
        self.picking.write({"is_locked": True})
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        # Create a snapshot including this picking
        self.stock_history_now.action_generate_stock_quant_history()
        # Try to unlock the picking
        with self.assertRaises(ValidationError):
            self.picking.write({"is_locked": False})

    @users("stock_manager")
    def test3_unlock_with_past_history(self):
        """Test the unlock functionality without history."""
        # Create a snapshot before confirming the picking
        self.stock_history_now.action_generate_stock_quant_history()
        self.assertIn(
            self.lot,
            self.stock_history_now.stock_quant_history_ids.mapped("lot_id"),
            "The snapshot should have the lot of the move line.",
        )
        # Validate and finish the picking to be locked
        self.picking.action_assign()
        self.picking.action_confirm()
        self.picking.write({"is_locked": True})
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        # This picking should be unlocked (no changes on standard behavior)
        self.picking.write({"is_locked": False})
        self.assertFalse(
            self.picking.is_locked, "The picking should be unlocked after toggling."
        )

    @users("stock_manager")
    def test_lock_done_picking_on_snapshot_creation_with_option(self):
        """Test that the picking is locked when a snapshot is created."""
        self.env.company.stock_history_snapshot_auto_locks_picking = True
        # Validate and finish the picking to be locked
        self.picking.action_assign()
        self.picking.action_confirm()
        # Create a snapshot including this picking
        self.stock_history_now.action_generate_stock_quant_history()
        # The picking should be locked after the snapshot creation
        self.assertTrue(
            self.picking.is_locked, "The picking should be locked after snapshot."
        )

    @users("stock_manager")
    def test_lock_done_picking_on_snapshot_creation_no_option(self):
        """Test that the picking is not locked when a snapshot is created without the
        option set (default behavior)."""
        # Validate and finish the picking to be locked
        self.picking.action_assign()
        self.picking.action_confirm()
        self.stock_history_now.action_generate_stock_quant_history()
        # The picking should remain unlocked after the snapshot creation
        self.assertFalse(
            self.picking.is_locked, "The picking should remain unlocked after snapshot."
        )

    @users("stock_manager")
    def test_unlocked_pending_picking_on_snapshot_creation(self):
        """Test that the picking remains unlocked when a snapshot is created."""
        # Create a snapshot including this picking
        self.stock_history_now.action_generate_stock_quant_history()
        # The picking should remain unlocked after the snapshot creation
        self.assertFalse(
            self.picking.is_locked, "The picking should remain unlocked after snapshot."
        )
