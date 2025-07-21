# Copyright 2025 Foodles (https://www.foodles.co/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from datetime import datetime

from freezegun import freeze_time

from odoo.exceptions import ValidationError
from odoo.tests import tagged, users

from . import common


@tagged("post_install", "-at_install")
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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        customer_location = cls.env.ref("stock.stock_location_customers")
        with freeze_time("2024-06-14 14:14"):
            cls._update_product_stock(5, lot=cls.lot, location=cls.location)

        cls.stock_history_now.inventory_date = datetime(2024, 6, 15, 15, 15, 15)
        cls.picking = cls.env["stock.picking"].create(
            {
                "name": "Test Picking",
                "picking_type_id": cls.env.ref("stock.picking_type_out").id,
                "location_id": cls.location.id,
                "location_dest_id": customer_location.id,
            }
        )
        cls.move_line = cls.env["stock.move"].create(
            {
                "name": "test",
                "product_id": cls.product.id,
                "location_id": cls.location.id,
                "location_dest_id": customer_location.id,
                "picking_id": cls.picking.id,
                "product_uom": cls.product.uom_id.id,
                "product_uom_qty": 1,
            }
        )

    @users("stock_manager")
    def test1_lock_unlock_without_history(self):
        """Test the lock functionality."""
        # Assign and confirm the picking to be locked
        with freeze_time("2024-06-14 20:14"):
            self._validate_picking()
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        self.picking.write({"is_locked": False})
        self.assertFalse(
            self.picking.is_locked, "The picking should be unlocked after toggling."
        )

    @users("stock_manager")
    def test2_unlock_with_history(self):
        """Test the unlock functionality with history."""
        # Validate and finish the picking to be locked
        with freeze_time("2024-06-14 20:14"):
            self._validate_picking()
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        # Create a snapshot including this picking
        self.stock_history_now._generate_stock_quant_history()
        # Try to unlock the picking
        with self.assertRaises(ValidationError):
            self.picking.write({"is_locked": False})

    def _validate_picking(self):
        self.picking.action_assign()
        self.picking.move_line_ids.qty_done = 1
        self.picking.button_validate()

    @users("stock_manager")
    def test3_unlock_with_past_history(self):
        """Test the unlock functionality without history."""
        # Create a snapshot before confirming the picking
        # Validate and finish the picking to be locked
        self.stock_history_now._generate_stock_quant_history()
        self.assertIn(
            self.lot,
            self.stock_history_now.stock_quant_history_ids.mapped("lot_id"),
            "The snapshot should have the lot of the move line.",
        )
        with freeze_time("2024-06-16 16:16"):
            self._validate_picking()
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
        self._validate_picking()
        self.assertEqual(
            self.picking.state,
            "done",
        )
        self.assertTrue(self.picking.is_locked, "The picking should be locked.")
        # Create a snapshot including this picking
        self.stock_history_now._generate_stock_quant_history()
        # The picking should be locked after the snapshot creation
        self.assertTrue(
            self.picking.is_locked, "The picking should be locked after snapshot."
        )

    @users("stock_manager")
    def test_lock_done_picking_on_snapshot_creation_no_option(self):
        """Test that the picking is not locked when a snapshot is created without the
        option set (default behavior)."""
        # Validate and finish the picking to be locked
        self.env.company.stock_history_snapshot_auto_locks_picking = False
        with freeze_time("2024-06-14 20:20"):
            self._validate_picking()
            self.picking.write({"is_locked": False})
        self.stock_history_now._generate_stock_quant_history()
        # The picking should remain unlocked after the snapshot creation
        self.assertFalse(
            self.picking.is_locked, "The picking should remain unlocked after snapshot."
        )

    @users("stock_manager")
    def test_unlocked_pending_picking_on_snapshot_creation(self):
        """Test that the picking remains unlocked when a snapshot is created."""
        self.picking.write({"is_locked": False})
        # Create a snapshot including this picking
        self.stock_history_now._generate_stock_quant_history()
        # The picking should remain unlocked after the snapshot creation
        self.assertFalse(
            self.picking.is_locked, "The picking should remain unlocked after snapshot."
        )

    @users("stock_manager")
    def test_check_unlock_allowed_pending_picking(self):
        self.picking.action_toggle_is_locked()
        self.assertFalse(self.picking.is_locked)
        self.picking.action_toggle_is_locked()
        self.assertTrue(self.picking.is_locked)
