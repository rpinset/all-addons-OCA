# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, datetime

import freezegun

from odoo import Command
from odoo.exceptions import ValidationError

from .common import SaleOrderBlanketOrderStockPrebookReleaseCase


class TestSaleOrderBlanketOrderStockPrebookRelease(
    SaleOrderBlanketOrderStockPrebookReleaseCase
):
    def test_blanket_move_date_priority(self):
        self.assertFalse(self.blanket_so.blanket_move_date_priority)

        # the move date priority is computed when the blanket order is confirmed
        self.blanket_so.action_confirm()
        self.assertTrue(self.blanket_so.blanket_move_date_priority)
        # the move date priority must be the validity start date of the blanket order
        # incremented by the x seconds where x is the number of confirmed blanket orders
        # with the same validity start date
        # At this point we have only one confirmed blanket order with the same validity
        # start date
        move_date_priority = self.blanket_so.blanket_move_date_priority
        self.assertEqual(
            move_date_priority,
            self._date_to_datetime(
                self.blanket_so.blanket_validity_start_date, nb_seconds=0
            ),
        )
        # if we create a new blanket order with the same validity start date and confirm
        # it the move date priority of the first blanket order must be incremented by 1
        # second
        new_blanket_so = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner_delta.id,
                "blanket_validity_start_date": "2025-01-01",
                "blanket_validity_end_date": "2025-12-31",
                "blanket_reservation_strategy": "at_confirm",
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product2.id,
                            "product_uom_qty": 10.0,
                            "price_unit": 100.0,
                        },
                    ),
                ],
            }
        )
        new_blanket_so.action_confirm()
        self.assertEqual(
            new_blanket_so.blanket_move_date_priority,
            self._date_to_datetime(
                new_blanket_so.blanket_validity_start_date, nb_seconds=1
            ),
        )

        # if we create a new blanket order with a different validity start date
        # the move date priority of the first blanket order must be the validity start
        # date incremented by 0 seconds
        new_blanket_so = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner_delta.id,
                "blanket_validity_start_date": "2026-01-01",
                "blanket_validity_end_date": "2026-12-31",
                "blanket_reservation_strategy": "at_confirm",
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product2.id,
                            "product_uom_qty": 10.0,
                            "price_unit": 100.0,
                        },
                    ),
                ],
            }
        )
        new_blanket_so.action_confirm()
        self.assertEqual(
            new_blanket_so.blanket_move_date_priority,
            self._date_to_datetime(
                new_blanket_so.blanket_validity_start_date, nb_seconds=0
            ),
        )

    def test_date_priority_on_prebook_moves_blanket_orders(self):
        """For blanket orders, the prebook moves must have the date priority set to the
        blanket move date priority"""
        self.blanket_so.action_confirm()
        prebook_moves = self.blanket_so.order_line.move_ids.filtered(
            "used_for_sale_reservation"
        )
        self.assertTrue(prebook_moves)
        for move in prebook_moves:
            self.assertEqual(
                move.date_priority, self.blanket_so.blanket_move_date_priority
            )

    def test_date_priority_on_prebook_moves_regular_orders(self):
        """For normal order, in case of prebooking, the date priority must be the
        datetime at confirmation"""
        new_so = self.env["sale.order"].create(
            {
                "partner_id": self.partner_delta.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product1.id,
                            "product_uom_qty": 10.0,
                            "price_unit": 100.0,
                        },
                    ),
                ],
            }
        )
        with freezegun.freeze_time("2020-01-01 00:00:00"):
            new_so.reserve_stock()
            now = datetime(2020, 1, 1, 0, 0, 0)
            prebook_moves = new_so.order_line.move_ids.filtered(
                "used_for_sale_reservation"
            )
            self.assertTrue(prebook_moves)
            for move in prebook_moves:
                self.assertEqual(move.date_priority, now)

    def test_date_priority_on_preparation_moves(self):
        """For blanket oders, the preparation moves must have the date priority set to
        the blanket move date priority"""
        self.blanket_so.action_confirm()

        with freezegun.freeze_time("2025-02-01"):
            order = self.env["sale.order"].create(
                {
                    "order_type": "call_off",
                    "partner_id": self.partner_delta.id,
                    "blanket_order_id": self.blanket_so.id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product1.id,
                                "product_uom_qty": 10.0,
                            }
                        ),
                    ],
                }
            )
            order.action_confirm()

        # the date_priority on the moves linked to the blanket order
        # for the preparation must be blanket_move_date_priority
        self.assertTrue(
            order.order_line.blanket_move_ids.filtered(
                lambda m: not m.used_for_sale_reservation
            )
        )
        for move in order.order_line.blanket_move_ids:
            self.assertEqual(
                move.date_priority, self.blanket_so.blanket_move_date_priority
            )

    @freezegun.freeze_time("2025-01-01 00:00:00")
    def test_date_priority_after_blanket_validity_start_date_change(self):
        self.blanket_so.action_confirm()
        self.assertEqual(self.blanket_so.blanket_validity_start_date, date(2025, 1, 1))
        self.assertEqual(self.blanket_so.commitment_date.date(), date(2025, 1, 1))
        call_off_so = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2025-02-01",
                "partner_id": self.partner_delta.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product1.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                ],
            }
        )
        call_off_so.action_confirm()

        picking = call_off_so.order_line.blanket_move_ids.picking_id
        picking.action_assign()
        out_moves = picking.move_ids
        self.assertEqual(
            out_moves.date_priority.date(), self.blanket_so.blanket_validity_start_date
        )
        validity_start_date = date(2025, 1, 2)
        self.blanket_so.blanket_validity_start_date = validity_start_date
        self.assertEqual(self.blanket_so.commitment_date.date(), validity_start_date)
        self.assertEqual(
            out_moves.date_priority.date(), self.blanket_so.blanket_validity_start_date
        )

    def test_confirm_dates_validation_not_broken_on_confirm(self):
        """Ensure the dates validation occurs when confirming a blanket order."""
        self.blanket_so.write(
            {"blanket_validity_start_date": False, "blanket_validity_end_date": False}
        )
        with self.assertRaises(ValidationError):
            self.blanket_so.action_confirm()

    def test_set_blanket_move_date_priority_skips_without_start_date(self):
        self.env["sale.order"]._set_blanket_move_date_priority()

        self.blanket_so.write({"blanket_validity_start_date": False})
        self.blanket_so._set_blanket_move_date_priority()
        self.assertFalse(self.blanket_so.blanket_move_date_priority)

    def test_inverse_commitment_date_updates_validity_start_date_when_confirmed(self):
        """Changing commitment_date on a confirmed blanket order must sync
        blanket_validity_start_date without recomputing move date priorities."""
        self.blanket_so.action_confirm()
        original_priority = self.blanket_so.blanket_move_date_priority
        self.assertTrue(original_priority)

        new_date = date(2025, 3, 1)
        self.blanket_so.commitment_date = new_date

        self.assertEqual(
            self.blanket_so.blanket_validity_start_date,
            new_date,
            "blanket_validity_start_date must be updated when commitment_date changes",
        )
        # _set_blanket_move_date_priority must NOT have been triggered again
        # (the context from_inverse_commitment_date prevents it)
        self.assertEqual(
            self.blanket_so.blanket_move_date_priority,
            original_priority,
            (
                "blanket_move_date_priority must not change "
                "when updating via commitment_date"
            ),
        )

    def test_inverse_commitment_date_skips_draft_blanket_orders(self):
        """Changing commitment_date on a draft blanket order must not affect
        blanket_validity_start_date."""
        self.assertEqual(self.blanket_so.state, "draft")
        original_start = self.blanket_so.blanket_validity_start_date

        self.blanket_so.commitment_date = date(2025, 3, 1)

        self.assertEqual(
            self.blanket_so.blanket_validity_start_date,
            original_start,
            "Draft blanket orders must not be affected by commitment_date inverse",
        )

    def test_inverse_blanket_validity_start_date_skips_with_context(self):
        """_inverse_blanket_validity_start_date must return early when
        from_inverse_commitment_date is in the context, leaving commitment_date
        and move date_priorities untouched."""
        self.blanket_so.action_confirm()
        original_commitment = self.blanket_so.commitment_date
        original_priority = self.blanket_so.blanket_move_date_priority

        new_date = date(2025, 3, 1)
        self.blanket_so.with_context(from_inverse_commitment_date=True).write(
            {"blanket_validity_start_date": new_date}
        )

        self.assertEqual(
            self.blanket_so.blanket_validity_start_date,
            new_date,
            "blanket_validity_start_date must be updated",
        )
        self.assertEqual(
            self.blanket_so.commitment_date,
            original_commitment,
            "commitment_date must not change when from_inverse_commitment_date is set",
        )
        self.assertEqual(
            self.blanket_so.blanket_move_date_priority,
            original_priority,
            (
                "blanket_move_date_priority must not change "
                "when from_inverse_commitment_date is set"
            ),
        )

    def test_inverse_blanket_validity_start_date_skips_draft(self):
        """_inverse_blanket_validity_start_date must not update commitment_date or
        recompute priorities for draft blanket orders."""
        self.assertEqual(self.blanket_so.state, "draft")
        # Commitment date is not set on a draft order
        self.assertFalse(self.blanket_so.commitment_date)

        self.blanket_so.write({"blanket_validity_start_date": date(2025, 3, 1)})

        self.assertFalse(
            self.blanket_so.commitment_date,
            (
                "commitment_date must not be set by "
                "_inverse_blanket_validity_start_date on draft"
            ),
        )
        self.assertFalse(self.blanket_so.blanket_move_date_priority)

    def test_prepare_procurement_values_sets_date_priority_for_blanket_at_confirm(
        self,
    ):
        """_prepare_procurement_values must include date_priority equal to
        blanket_move_date_priority for blanket orders with at_confirm strategy."""
        self.blanket_so.action_confirm()
        expected_priority = self.blanket_so.blanket_move_date_priority
        self.assertTrue(expected_priority)

        line = self.blanket_so.order_line[0]
        values = line._prepare_procurement_values()

        self.assertIn("date_priority", values)
        self.assertEqual(values["date_priority"], expected_priority)
