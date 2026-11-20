# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import freezegun

from odoo import Command
from odoo.exceptions import UserError, ValidationError

from .common import SaleOrderBlanketOrderCase


class TestSaleCallOffOrder(SaleOrderBlanketOrderCase):
    def test_confirm_no_blanket_id(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "A call-off order must have a blanket order."
        ):
            order.action_confirm()

    def test_confirm_blanket_id_not_blanket(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.so.id,
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "A call-off order must have a blanket order."
        ):
            order.action_confirm()

    def test_confirm_blanket_id_not_confirmed(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
            }
        )

        with self.assertRaisesRegex(
            ValidationError, "The blanket order must be confirmed"
        ):
            order.action_confirm()

    def test_confirm_blanket_id_validity_period(self):
        self.blanket_so.action_confirm()
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2024-01-01",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
            }
        )
        with freezegun.freeze_time("2024-01-01"), self.assertRaisesRegex(
            ValidationError,
            (
                "The call-off order must be within the "
                "validity period of the blanket order."
            ),
        ):
            order.action_confirm()

    @freezegun.freeze_time("2025-02-01")
    def test_confirm_ok(self):
        self.blanket_so.action_confirm()
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2025-02-01",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
            }
        )
        order.action_confirm()
        self.assertIn(order.state, ["sale", "done"])

    @freezegun.freeze_time("2025-02-01")
    def test_order_line_constrains(self):
        self.blanket_so.action_confirm()

        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_3.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                ],
            }
        )
        with self.assertRaisesRegex(
            ValidationError,
            ("The product is not part of linked blanket order"),
        ), self.env.cr.savepoint():
            order.action_confirm()

        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 100.0,
                        }
                    ),
                ],
            }
        )
        with self.assertRaisesRegex(
            ValidationError,
            (
                "The quantity to procure is greater than the quantity remaining "
                "to deliver"
            ),
        ):
            order.action_confirm()

    def test_order_line_attributes(self):
        self.blanket_so.action_confirm()
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2025-02-01",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                ],
            }
        )
        blanket_line = self.blanket_so.order_line.filtered(
            lambda line: line.product_id == self.product_1
        )[0]
        self.assertRecordValues(
            order.order_line,
            [
                {
                    "product_uom_qty": 10.0,
                    "price_unit": 0.0,
                    "qty_to_deliver": 10.0,
                    "qty_to_invoice": 0.0,
                    "qty_delivered": 0.0,
                    "display_qty_widget": True,
                    "virtual_available_at_date": blanket_line.virtual_available_at_date,
                    "scheduled_date": blanket_line.scheduled_date,
                    "forecast_expected_date": blanket_line.forecast_expected_date,
                    "free_qty_today": blanket_line.free_qty_today,
                    "qty_available_today": blanket_line.qty_available_today,
                    "price_tax": 0.0,
                    "price_total": 0.0,
                    "tax_id": [],
                }
            ],
        )
        # once confirmed, the quantity to deliver should become 0 and the
        # display_qty_widget should be False
        with freezegun.freeze_time("2025-02-01"):
            order.action_confirm()
        self.assertRecordValues(
            order.order_line,
            [
                {
                    "product_uom_qty": 10.0,
                    "price_unit": 0.0,
                    "qty_to_deliver": 0.0,
                    "qty_to_invoice": 0.0,
                    "qty_delivered": 0.0,
                    "display_qty_widget": False,
                }
            ],
        )


class TestSaleCallOffOrderProcessing(SaleOrderBlanketOrderCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_so.action_confirm()

    @freezegun.freeze_time("2025-02-01")
    def test_processing(self):
        # Create a call-off order without reservation
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                ],
            }
        )
        order.action_confirm()
        self.assertIn(order.state, ["sale", "done"])
        self.assertRecordValues(
            order.order_line,
            [
                {
                    "product_uom_qty": 10.0,
                    "price_unit": 0.0,
                    "qty_to_deliver": 0.0,
                    "qty_to_invoice": 0.0,
                    "qty_delivered": 0.0,
                    "display_qty_widget": False,
                },
                {
                    "product_uom_qty": 10.0,
                    "price_unit": 0.0,
                    "qty_to_deliver": 0.0,
                    "qty_to_invoice": 0.0,
                    "qty_delivered": 0.0,
                    "display_qty_widget": False,
                },
            ],
        )

        # The lines should be linked to moves linked to a blanked order line
        for line in order.order_line:
            self.assertTrue(line.blanket_move_ids)
            sale_line = line.blanket_move_ids.sale_line_id
            self.assertEqual(sale_line.product_id, line.product_id)
            self.assertEqual(sale_line.order_id, self.blanket_so)
            self.assertEqual(line.blanket_line_id, sale_line)

        # process the picking
        picking = line.blanket_move_ids.picking_id
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.qty_done = move_line.reserved_uom_qty
        picking._action_done()

        blanket_lines = self.blanket_so.order_line

        # part of the quantity into the blanket order are now delivered
        for product in [self.product_1, self.product_2]:
            self.assertEqual(
                sum(
                    blanket_lines.filtered(
                        lambda line, product=product: line.product_id == product
                    ).mapped("qty_delivered")
                ),
                10.0,
            )

    @freezegun.freeze_time("2025-02-01")
    def test_no_reservation_processing_2(self):
        # In this test we create a call-off order with 1 lines
        # for product 1 where the quantity to deliver is greater
        # than the quantity defined per line in the blanket order.
        # On the blanket order we have 2 lines for product 1 with
        # 10.0 quantity each.
        # The call-off order will have 1 line for product 1 with
        # 15.0 quantity.

        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 15.0,
                        }
                    ),
                ],
            }
        )
        order.action_confirm()
        self.assertIn(order.state, ["sale", "done"])

        # process the picking
        picking = order.order_line.blanket_move_ids.picking_id
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.qty_done = move_line.reserved_uom_qty
        picking._action_done()

        # part of the quantity into the blanket order are now delivered
        blanket_lines = self.blanket_so.order_line.filtered(
            lambda line: line.product_id == self.product_1
        )
        self.assertEqual(len(blanket_lines), 2)
        self.assertEqual(
            sum(blanket_lines.mapped("qty_delivered")),
            15.0,
        )

        # the call-off order line has been split into 2 lines, each one linked to
        # a different blanket order line
        self.assertEqual(len(order.order_line), 2)
        self.assertEqual(
            order.order_line.blanket_line_id,
            blanket_lines,
        )

    def _create_call_off_order(self, product_uom_qty, commitment_date=None):
        return self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "commitment_date": commitment_date,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": product_uom_qty,
                        }
                    ),
                ],
            }
        )

    @freezegun.freeze_time("2025-02-01")
    def test_cancel_call_off_order(self):
        blanket_line = self.blanket_so.order_line.filtered(
            lambda line: line.product_id == self.product_1
        )[0]
        remaining_qty = blanket_line.call_off_remaining_qty
        order = self._create_call_off_order(5.0, commitment_date="2025-02-10 10:00:00")
        order.action_confirm()
        moves = order.order_line.blanket_move_ids
        group = moves.group_id
        self.assertTrue(group)
        self.assertEqual(blanket_line.call_off_remaining_qty, remaining_qty - 5.0)

        order._action_cancel()

        self.assertEqual(order.state, "cancel")
        self.assertEqual(set(moves.mapped("state")), {"cancel"})
        self.assertFalse(group.exists())
        self.assertEqual(blanket_line.call_off_remaining_qty, remaining_qty)
        self.assertEqual(blanket_line.qty_to_procure, blanket_line.product_uom_qty)

    @freezegun.freeze_time("2025-02-01")
    def test_cancel_call_off_order_sharing_group(self):
        # Only the moves of the canceled call-off order are canceled and the
        # procurement group shared with another call-off order is kept.
        order_1 = self._create_call_off_order(
            5.0, commitment_date="2025-02-10 10:00:00"
        )
        order_1.action_confirm()
        order_2 = self._create_call_off_order(
            3.0, commitment_date="2025-02-10 10:00:00"
        )
        order_2.action_confirm()
        moves_1 = order_1.order_line.blanket_move_ids
        moves_2 = order_2.order_line.blanket_move_ids
        group = moves_1.group_id
        self.assertEqual(group, moves_2.group_id)

        order_1._action_cancel()

        self.assertEqual(set(moves_1.mapped("state")), {"cancel"})
        self.assertNotIn("cancel", moves_2.mapped("state"))
        self.assertTrue(group.exists())
        self.assertEqual(moves_2.picking_id.sale_id, self.blanket_so)

        order_2._action_cancel()
        self.assertFalse(group.exists())

    @freezegun.freeze_time("2025-02-01")
    def test_cancel_call_off_order_multi_steps(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )
        warehouse.delivery_steps = "pick_ship"
        order = self._create_call_off_order(5.0, commitment_date="2025-02-10 10:00:00")
        order.action_confirm()
        ship_moves = order.order_line.blanket_move_ids
        pick_moves = ship_moves.move_orig_ids
        self.assertTrue(pick_moves)
        group = ship_moves.group_id

        order._action_cancel()

        # The upstream moves only feeding the moves of the call-off order are
        # also canceled
        self.assertEqual(set(ship_moves.mapped("state")), {"cancel"})
        self.assertEqual(set(pick_moves.mapped("state")), {"cancel"})
        self.assertFalse(group.exists())

    @freezegun.freeze_time("2025-02-01")
    def test_cancel_call_off_order_multi_steps_merged_moves(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )
        warehouse.delivery_steps = "pick_ship"
        order_1 = self._create_call_off_order(
            5.0, commitment_date="2025-02-10 10:00:00"
        )
        order_1.action_confirm()
        order_2 = self._create_call_off_order(
            3.0, commitment_date="2025-02-10 10:00:00"
        )
        order_2.action_confirm()
        ship_moves_1 = order_1.order_line.blanket_move_ids
        ship_moves_2 = order_2.order_line.blanket_move_ids
        # The pick moves of the call-off orders are merged into a single
        # operation
        pick_move = ship_moves_1.move_orig_ids
        self.assertEqual(len(pick_move), 1)
        self.assertEqual(pick_move, ship_moves_2.move_orig_ids)
        self.assertEqual(pick_move.product_uom_qty, 8.0)
        pick_move._action_assign()
        self.assertEqual(pick_move.reserved_availability, 8.0)
        move_line = pick_move.move_line_ids
        self.assertEqual(len(move_line), 1)

        order_1._action_cancel()

        # The qty of the pick move feeding the canceled call-off order is
        # removed from the merged pick move
        self.assertEqual(set(ship_moves_1.mapped("state")), {"cancel"})
        self.assertNotIn("cancel", ship_moves_2.mapped("state"))
        self.assertEqual(pick_move.state, "assigned")
        self.assertEqual(pick_move.product_uom_qty, 3.0)
        self.assertEqual(pick_move.reserved_availability, 3.0)
        # The existing reservation is decreased, not done again
        self.assertEqual(pick_move.move_line_ids, move_line)
        self.assertEqual(move_line.reserved_uom_qty, 3.0)
        quants = self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product_1.id),
                ("location_id", "=", move_line.location_id.id),
            ]
        )
        self.assertEqual(sum(quants.mapped("reserved_quantity")), 3.0)
        self.assertEqual(pick_move.move_dest_ids, ship_moves_2)
        self.assertEqual(len(pick_move.picking_id.move_ids), 1)

    @freezegun.freeze_time("2025-02-01")
    def test_cancel_call_off_order_delivered(self):
        order = self._create_call_off_order(5.0, commitment_date="2025-02-10 10:00:00")
        order.action_confirm()
        picking = order.order_line.blanket_move_ids.picking_id
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.qty_done = move_line.reserved_uom_qty
        picking._action_done()
        with self.assertRaisesRegex(UserError, "already been delivered"):
            order._action_cancel()


class TestSaleAutoDoneCallOffOrderProcessing(TestSaleCallOffOrderProcessing):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id += cls.env.ref("sale.group_auto_done_setting")
