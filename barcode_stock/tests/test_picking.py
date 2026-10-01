# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBarcodeScannerInternalTransfer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.internal_picking_type = cls.env["stock.picking.type"].search(
            [
                ("code", "=", "internal"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )
        cls.destination_location = cls.env["stock.location"].create(
            {
                "name": "Barcode Scanner Buffer",
                "usage": "internal",
                "location_id": cls.stock_location.location_id.id,
                "company_id": cls.company.id,
            }
        )
        cls.tracked_product = cls.env["product.product"].create(
            {
                "name": "Tracked Internal Product",
                "is_storable": True,
                "tracking": "lot",
            }
        )
        cls.untracked_product = cls.env["product.product"].create(
            {
                "name": "Untracked Internal Product",
                "is_storable": True,
            }
        )
        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "LOT-INT-001",
                "product_id": cls.tracked_product.id,
                "company_id": cls.company.id,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.tracked_product,
            cls.stock_location,
            5,
            lot_id=cls.lot,
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.untracked_product,
            cls.stock_location,
            8,
        )

    def test_action_barcode_scanner_check_availability_returns_line_status(self):
        result = self.env["stock.picking"].action_barcode_scanner_check_availability(
            self.stock_location.id,
            self.destination_location.id,
            [
                {
                    "product_id": self.tracked_product.id,
                    "qty": 2,
                    "lot_id": self.lot.id,
                },
                {
                    "product_id": self.untracked_product.id,
                    "qty": 10,
                    "lot_id": False,
                },
            ],
        )

        self.assertFalse(result["available"])
        self.assertEqual(len(result["lines"]), 2)
        tracked_line = next(
            line
            for line in result["lines"]
            if line["product_id"] == self.tracked_product.id
        )
        self.assertTrue(tracked_line["available"])
        untracked_line = next(
            line
            for line in result["lines"]
            if line["product_id"] == self.untracked_product.id
        )
        self.assertFalse(untracked_line["available"])

    def test_action_barcode_scanner_internal_transfer_creates_and_validates_picking(
        self,
    ):
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            self.stock_location.id,
            self.destination_location.id,
            self.env.user.id,
            [
                {
                    "product_id": self.tracked_product.id,
                    "qty": 2,
                    "lot_id": self.lot.id,
                },
                {
                    "product_id": self.untracked_product.id,
                    "qty": 3,
                    "lot_id": False,
                },
            ],
        )

        picking = self.env["stock.picking"].browse(result["picking_id"])
        self.assertTrue(picking.exists())
        self.assertEqual(picking.state, "done")
        self.assertEqual(picking.picking_type_id.code, "internal")
        self.assertEqual(picking.user_id, self.env.user)
        tracked_move_line = picking.move_line_ids.filtered(
            lambda line: line.product_id == self.tracked_product
        )
        self.assertEqual(tracked_move_line.lot_id, self.lot)
        self.assertEqual(tracked_move_line.quantity, 2)
        self.assertTrue(tracked_move_line.picked)
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.tracked_product,
                self.stock_location,
                lot_id=self.lot,
                strict=False,
            ),
            3,
        )
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.tracked_product,
                self.destination_location,
                lot_id=self.lot,
                strict=False,
            ),
            2,
        )

    def test_action_barcode_scanner_internal_transfer_requires_lot_for_tracked_product(
        self,
    ):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [
                    {
                        "product_id": self.tracked_product.id,
                        "qty": 1,
                        "lot_id": False,
                    }
                ],
            )

    def test_internal_transfer_transfers_available_when_over_requested(self):
        # Only 8 untracked units exist; requesting more transfers what is
        # available (like the back office) instead of refusing the operation.
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            self.stock_location.id,
            self.destination_location.id,
            False,
            [
                {
                    "product_id": self.untracked_product.id,
                    "qty": 999,
                    "lot_id": False,
                }
            ],
        )
        picking = self.env["stock.picking"].browse(result["picking_id"])
        self.assertEqual(picking.state, "done")
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.untracked_product, self.stock_location, strict=False
            ),
            0,
        )
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.untracked_product, self.destination_location, strict=False
            ),
            8,
        )

    def test_internal_transfer_reports_partial_allocation_per_line(self):
        # 8 untracked units on hand, 3 tracked ones asked for out of 5: the
        # summary has to tell the operator, line by line, how much of what
        # they asked for actually moved.
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            self.stock_location.id,
            self.destination_location.id,
            False,
            [
                {
                    "product_id": self.untracked_product.id,
                    "qty": 20,
                    "lot_id": False,
                },
                {
                    "product_id": self.tracked_product.id,
                    "qty": 3,
                    "lot_id": self.lot.id,
                },
            ],
        )
        self.assertFalse(result["fully_transferred"])
        summary = {line["product_id"]: line for line in result["lines"]}
        short = summary[self.untracked_product.id]
        self.assertEqual(short["requested_qty"], 20)
        self.assertEqual(short["moved_qty"], 8)
        # The line that was fully served keeps its own figures; the summary is
        # per line, not a single verdict for the whole transfer.
        served = summary[self.tracked_product.id]
        self.assertEqual(served["requested_qty"], 3)
        self.assertEqual(served["moved_qty"], 3)

    def test_internal_transfer_raises_when_no_stock(self):
        empty_product = self.env["product.product"].create(
            {"name": "No Stock Product", "is_storable": True}
        )
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [{"product_id": empty_product.id, "qty": 1, "lot_id": False}],
            )

    def test_internal_transfer_reduces_source_stock(self):
        self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            self.stock_location.id,
            self.destination_location.id,
            False,
            [{"product_id": self.untracked_product.id, "qty": 2, "lot_id": False}],
        )
        available = self.env["stock.quant"]._get_available_quantity(
            self.untracked_product,
            self.stock_location,
            strict=False,
        )
        self.assertEqual(available, 6)

    def test_internal_transfer_pulls_from_child_locations(self):
        # Stock living only in child sub-locations must be transferable from the
        # parent, taken from the children (no negative quant at the parent).
        # Regression test for the child-location availability bug.
        parent = self.env["stock.location"].create(
            {
                "name": "BC Parent",
                "usage": "internal",
                "location_id": self.stock_location.id,
                "company_id": self.company.id,
            }
        )
        child_a = self.env["stock.location"].create(
            {
                "name": "BC Child A",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        child_b = self.env["stock.location"].create(
            {
                "name": "BC Child B",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Child Loc Product", "is_storable": True}
        )
        self.env["stock.quant"]._update_available_quantity(product, child_a, 10)
        self.env["stock.quant"]._update_available_quantity(product, child_b, 15)

        # Over-request 32 against the 25 available across the children.
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            parent.id,
            self.destination_location.id,
            False,
            [{"product_id": product.id, "qty": 32, "lot_id": False}],
        )
        picking = self.env["stock.picking"].browse(result["picking_id"])
        self.assertEqual(picking.state, "done")
        Quant = self.env["stock.quant"]
        self.assertEqual(
            Quant._get_available_quantity(product, parent, strict=False), 0
        )
        # No negative quant created directly at the parent view location.
        self.assertEqual(Quant._get_available_quantity(product, parent, strict=True), 0)
        self.assertEqual(
            Quant._get_available_quantity(
                product, self.destination_location, strict=False
            ),
            25,
        )

    def test_internal_transfer_requires_origin(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                False,
                self.destination_location.id,
                False,
                [{"product_id": self.untracked_product.id, "qty": 1}],
            )

    def test_internal_transfer_requires_destination(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                False,
                False,
                [{"product_id": self.untracked_product.id, "qty": 1}],
            )

    def test_internal_transfer_requires_lines(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [],
            )

    def test_internal_transfer_rejects_invalid_location(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                999999999,
                self.destination_location.id,
                False,
                [{"product_id": self.untracked_product.id, "qty": 1}],
            )

    def test_internal_transfer_rejects_same_location(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.stock_location.id,
                False,
                [{"product_id": self.untracked_product.id, "qty": 1}],
            )

    def test_internal_transfer_rejects_unknown_product(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [{"product_id": 999999999, "qty": 1}],
            )

    def test_internal_transfer_rejects_non_positive_qty(self):
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [{"product_id": self.untracked_product.id, "qty": 0}],
            )

    def test_internal_transfer_rejects_lot_of_other_product(self):
        other_lot = self.env["stock.lot"].create(
            {
                "name": "LOT-OTHER-001",
                "product_id": self.untracked_product.id
                if self.untracked_product.tracking != "none"
                else self.tracked_product.id,
                "company_id": self.company.id,
            }
        )
        # A lot that exists but does not belong to the scanned product.
        wrong_lot = self.env["stock.lot"].create(
            {
                "name": "LOT-WRONG-001",
                "product_id": self.untracked_product.id,
                "company_id": self.company.id,
            }
        )
        self.assertTrue(other_lot)
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [
                    {
                        "product_id": self.tracked_product.id,
                        "qty": 1,
                        "lot_id": wrong_lot.id,
                    }
                ],
            )

    def test_internal_transfer_serial_one_unit_at_a_time(self):
        serial_product = self.env["product.product"].create(
            {
                "name": "Serial Internal Product",
                "is_storable": True,
                "tracking": "serial",
            }
        )
        serial_lot = self.env["stock.lot"].create(
            {
                "name": "SER-INT-001",
                "product_id": serial_product.id,
                "company_id": self.company.id,
            }
        )
        self.env["stock.quant"]._update_available_quantity(
            serial_product, self.stock_location, 1, lot_id=serial_lot
        )
        with self.assertRaises(UserError):
            self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                self.stock_location.id,
                self.destination_location.id,
                False,
                [
                    {
                        "product_id": serial_product.id,
                        "qty": 2,
                        "lot_id": serial_lot.id,
                    }
                ],
            )

    def test_internal_transfer_requires_configured_operation_type(self):
        # When neither the warehouse nor a company search yields an internal
        # operation type, the transfer is refused instead of creating one. Use
        # warehouse-less locations (so warehouse.int_type_id cannot supply one)
        # and stub the fallback search empty (an unlink would hit stock_rule FKs).
        src = self.env["stock.location"].create(
            {"name": "No-Type Src", "usage": "internal"}
        )
        dest = self.env["stock.location"].create(
            {"name": "No-Type Dest", "usage": "internal"}
        )
        self.env["stock.quant"]._update_available_quantity(
            self.untracked_product, src, 5
        )
        PickingType = type(self.env["stock.picking.type"])
        empty = self.env["stock.picking.type"].browse()
        with patch.object(PickingType, "search", return_value=empty):
            with self.assertRaises(UserError):
                self.env["stock.picking"].action_barcode_scanner_internal_transfer(
                    src.id,
                    dest.id,
                    False,
                    [{"product_id": self.untracked_product.id, "qty": 1}],
                )

    def test_internal_picking_type_falls_back_to_company_search(self):
        # Warehouse-less locations skip warehouse.int_type_id, so the company
        # search supplies the internal operation type (archived ones included).
        src = self.env["stock.location"].create(
            {"name": "Fallback Src", "usage": "internal"}
        )
        dest = self.env["stock.location"].create(
            {"name": "Fallback Dest", "usage": "internal"}
        )
        self.assertFalse(src.warehouse_id)
        picking_type = self.env[
            "stock.picking"
        ]._barcode_scanner_get_internal_picking_type(src, dest)
        self.assertEqual(picking_type.code, "internal")

    def test_internal_transfer_stops_once_requested_qty_is_met(self):
        parent = self.env["stock.location"].create(
            {
                "name": "Stop Parent",
                "usage": "internal",
                "location_id": self.stock_location.id,
                "company_id": self.company.id,
            }
        )
        child_a = self.env["stock.location"].create(
            {
                "name": "Stop Child A",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        child_b = self.env["stock.location"].create(
            {
                "name": "Stop Child B",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Stop Product", "is_storable": True}
        )
        self.env["stock.quant"]._update_available_quantity(product, child_a, 10)
        self.env["stock.quant"]._update_available_quantity(product, child_b, 10)
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            parent.id,
            self.destination_location.id,
            False,
            [{"product_id": product.id, "qty": 5}],
        )
        picking = self.env["stock.picking"].browse(result["picking_id"])
        self.assertEqual(picking.state, "done")
        self.assertTrue(result["fully_transferred"])

    def test_internal_transfer_skips_fully_reserved_quant(self):
        parent = self.env["stock.location"].create(
            {
                "name": "Res Parent",
                "usage": "internal",
                "location_id": self.stock_location.id,
                "company_id": self.company.id,
            }
        )
        child_a = self.env["stock.location"].create(
            {
                "name": "Res Child A",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        child_b = self.env["stock.location"].create(
            {
                "name": "Res Child B",
                "usage": "internal",
                "location_id": parent.id,
                "company_id": self.company.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Reserved Product", "is_storable": True}
        )
        self.env["stock.quant"]._update_available_quantity(product, child_a, 5)
        self.env["stock.quant"]._update_available_quantity(product, child_b, 5)
        # Reserve all of child_a through an outgoing picking, leaving no free qty.
        out = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": child_a.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": product.display_name,
                "product_id": product.id,
                "product_uom_qty": 5,
                "product_uom": product.uom_id.id,
                "picking_id": out.id,
                "location_id": child_a.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        out.action_confirm()
        out.action_assign()
        result = self.env["stock.picking"].action_barcode_scanner_internal_transfer(
            parent.id,
            self.destination_location.id,
            False,
            [{"product_id": product.id, "qty": 3}],
        )
        picking = self.env["stock.picking"].browse(result["picking_id"])
        self.assertEqual(picking.state, "done")


class TestStockMoveQtyProgress(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.picking_type_out = cls.env.ref("stock.picking_type_out")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "is_storable": True,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.stock_location, 100
        )

    def _create_assigned_picking(self, qty):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "name": self.product.display_name,
                "product_id": self.product.id,
                "product_uom_qty": qty,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        picking.action_confirm()
        picking.action_assign()
        return picking, move

    def test_reset_qty_progress(self):
        picking, move = self._create_assigned_picking(10)
        move_line = move.move_line_ids[0]
        move_line.qty_picked = 5
        move._compute_qty_progress()
        self.assertGreater(move.qty_done_total, 0)
        move._reset_qty_progress()
        self.assertEqual(move.qty_done_total, 0)
        self.assertEqual(move.qty_remaining, 0)
        self.assertFalse(move.is_fully_picked)

    def test_qty_remaining_computation(self):
        picking, move = self._create_assigned_picking(10)
        move_line = move.move_line_ids[0]
        move_line.qty_picked = 3
        move._compute_qty_progress()
        self.assertEqual(move.qty_done_total, 3)
        self.assertEqual(move.qty_remaining, 7)

    def test_is_fully_picked_when_qty_remaining_zero_or_less(self):
        picking, move = self._create_assigned_picking(10)
        move_line = move.move_line_ids[0]
        move_line.qty_picked = 10
        move._compute_qty_progress()
        self.assertTrue(move.is_fully_picked)
        self.assertEqual(move.qty_remaining, 0)

    def test_is_fully_picked_false_when_partial(self):
        picking, move = self._create_assigned_picking(10)
        move_line = move.move_line_ids[0]
        move_line.qty_picked = 4
        move._compute_qty_progress()
        self.assertFalse(move.is_fully_picked)
        self.assertEqual(move.qty_remaining, 6)

    def _draft_move(self, qty=10):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "name": self.product.display_name,
                "product_id": self.product.id,
                "product_uom_qty": qty,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        return picking, move

    def test_qty_progress_reset_in_install_mode(self):
        _, move = self._draft_move()
        move.with_context(install_mode=True)._compute_qty_progress()
        self.assertEqual(move.qty_done_total, 0)
        self.assertFalse(move.is_fully_picked)

    def test_qty_progress_reset_without_ready_moves(self):
        _, move = self._draft_move()  # draft picking, never assigned
        move._compute_qty_progress()
        self.assertEqual(move.qty_done_total, 0)
        self.assertEqual(move.qty_remaining, 0)


class TestStockMoveLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.product_serial = cls.env["product.product"].create(
            {
                "name": "Serial Product",
                "is_storable": True,
                "tracking": "serial",
            }
        )

    def test_serial_quantity_constraint(self):
        with self.assertRaises(UserError):
            self.env["stock.move.line"].create(
                {
                    "product_id": self.product_serial.id,
                    "location_id": self.stock_location.id,
                    "location_dest_id": self.customer_location.id,
                    "company_id": self.env.company.id,
                    "quantity": 2,
                    "product_uom_id": self.product_serial.uom_id.id,
                }
            )
