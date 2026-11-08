# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from freezegun import freeze_time

from .common import ZoneFifoCommon


class TestZoneFifo(ZoneFifoCommon):
    def test_removal_strategy_order(self):
        order = self.env["stock.quant"]._get_removal_strategy_order("zone_fifo")
        self.assertEqual(order, "zone_in_date, in_date, id")

    def test_other_strategies_untouched(self):
        Quant = self.env["stock.quant"]
        self.assertEqual(Quant._get_removal_strategy_order("fifo"), "in_date ASC, id")

    def test_zone_in_date_defaults_to_in_date(self):
        quant = self.env["stock.quant"].create(
            {
                "product_id": self.product.id,
                "location_id": self.bin_a1.id,
                "quantity": 10,
                "in_date": "2026-01-01 08:00:00",
            }
        )
        self.assertEqual(quant.zone_in_date, self._dt("2026-01-01 08:00:00"))

    def test_zone_in_date_is_never_empty(self):
        """No NULL to handle, so the ordering stays a plain ASC sort."""
        quant = self.env["stock.quant"].create(
            {
                "product_id": self.product.id,
                "location_id": self.bin_a1.id,
                "quantity": 10,
            }
        )
        self.assertTrue(quant.zone_in_date)

    def test_reservation_falls_back_on_in_date(self):
        """Equal zone entry dates are broken by the incoming date."""
        same_day = "2026-06-01 08:00:00"
        self._make_quant(
            self.bin_a1, 10, in_date="2026-03-01 08:00:00", zone_in_date=same_day
        )
        self._make_quant(
            self.bin_a2, 10, in_date="2026-01-01 08:00:00", zone_in_date=same_day
        )
        move = self._move(self.stock_loc, self.customer_loc, 10, done=False)
        self.assertEqual(move.move_line_ids.location_id, self.bin_a2)

    def test_zone_location_is_the_nearest_ancestor_with_the_strategy(self):
        self.assertEqual(self.bin_a1._get_zone_location(), self.zone_a)
        self.assertEqual(self.zone_a._get_zone_location(), self.zone_a)
        self.assertEqual(self.bin_b1._get_zone_location(), self.zone_b)
        self.assertFalse(self.loc_outside._get_zone_location())

    def test_move_inside_a_zone_keeps_the_date(self):
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.bin_a1, self.bin_a2, 10)
        self.assertEqual(
            self._quant(self.bin_a2).zone_in_date, self._dt("2026-02-01 08:00:00")
        )

    @freeze_time("2026-09-01 10:00:00")
    def test_move_to_another_zone_resets_the_date(self):
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.bin_a1, self.bin_b1, 10)
        self.assertEqual(
            self._quant(self.bin_b1).zone_in_date, self._dt("2026-09-01 10:00:00")
        )

    def test_move_out_of_every_zone_keeps_the_date(self):
        """Nothing sorts the goods there, so the setting is off by default."""
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.bin_a1, self.loc_outside, 10)
        self.assertEqual(
            self._quant(self.loc_outside).zone_in_date,
            self._dt("2026-02-01 08:00:00"),
        )

    @freeze_time("2026-09-01 10:00:00")
    def test_move_out_of_every_zone_updates_the_date_when_asked(self):
        self.env.company.zone_in_date_update_out_of_zone = True
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.bin_a1, self.loc_outside, 10)
        self.assertEqual(
            self._quant(self.loc_outside).zone_in_date, self._dt("2026-09-01 10:00:00")
        )

    def test_move_keeps_the_original_in_date(self):
        """in_date is still carried over, untouched."""
        self._make_quant(self.bin_a1, 10, in_date="2026-01-01 08:00:00")
        self._move(self.bin_a1, self.bin_a2, 10)
        self.assertEqual(
            self._quant(self.bin_a2).in_date, self._dt("2026-01-01 08:00:00")
        )

    def test_source_zone_in_date(self):
        """Reads the date of the quant the goods were taken from."""
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        # Not validated: once the move is done the emptied source quant is gone.
        move = self._move(self.bin_a1, self.bin_a2, 10, done=False)
        self.assertEqual(
            move.move_line_ids._source_zone_in_date(),
            self._dt("2026-02-01 08:00:00"),
        )

    @freeze_time("2026-09-01 10:00:00")
    def test_move_from_outside_into_a_zone_resets_the_date(self):
        self._make_quant(
            self.loc_outside,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.loc_outside, self.bin_a1, 10)
        self.assertEqual(
            self._quant(self.bin_a1).zone_in_date, self._dt("2026-09-01 10:00:00")
        )

    def test_merge_into_existing_stock_keeps_the_oldest_date(self):
        """Oldest wins, as the core does for in_date."""
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._make_quant(
            self.bin_a2,
            5,
            in_date="2026-05-01 08:00:00",
            zone_in_date="2026-05-01 08:00:00",
        )
        self._move(self.bin_a1, self.bin_a2, 10)
        self.assertEqual(
            self._quant(self.bin_a2).zone_in_date, self._dt("2026-02-01 08:00:00")
        )

    def test_merge_into_existing_stock_keeps_its_own_date(self):
        """Mirror of the case above: arriving goods never push the stock
        already there forward in the queue."""
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-05-01 08:00:00",
        )
        self._make_quant(
            self.bin_a2,
            5,
            in_date="2026-02-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        )
        self._move(self.bin_a1, self.bin_a2, 10)
        self.assertEqual(
            self._quant(self.bin_a2).zone_in_date, self._dt("2026-02-01 08:00:00")
        )

    def test_inventory_creation_is_allowed(self):
        # an inventory adjustment refuses any field it does not know about
        quant = (
            self.env["stock.quant"]
            .with_context(inventory_mode=True)
            .create(
                {
                    "product_id": self.product.id,
                    "location_id": self.bin_a1.id,
                    "inventory_quantity": 10,
                }
            )
        )
        quant.action_apply_inventory()
        self.assertEqual(quant.quantity, 10)
        self.assertTrue(quant.zone_in_date)

    def test_inventory_increase_keeps_the_date(self):
        quant = self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-01-01 08:00:00",
            zone_in_date="2026-02-01 08:00:00",
        ).with_context(inventory_mode=True)
        quant.inventory_quantity = 15
        quant.action_apply_inventory()
        self.assertEqual(quant.quantity, 15)
        self.assertEqual(quant.zone_in_date, self._dt("2026-02-01 08:00:00"))

    def test_untracked_stock_of_the_destination_is_left_alone(self):
        """A tracked line must not restamp the untracked quant of the bin,
        which a lookup by location alone also returns."""
        self.product.tracking = "lot"
        lot = self.env["stock.lot"].create(
            {"name": "LOT-A1", "product_id": self.product.id}
        )
        Quant = self.env["stock.quant"]
        untracked = Quant.create(
            {
                "product_id": self.product.id,
                "location_id": self.bin_a2.id,
                "quantity": 5,
                "in_date": "2026-09-01 08:00:00",
                "zone_in_date": "2026-09-01 08:00:00",
            }
        )
        Quant.create(
            {
                "product_id": self.product.id,
                "location_id": self.bin_a1.id,
                "lot_id": lot.id,
                "quantity": 10,
                "in_date": "2026-02-01 08:00:00",
                "zone_in_date": "2026-02-01 08:00:00",
            }
        )
        self._move(self.bin_a1, self.bin_a2, 10)
        self.assertEqual(untracked.zone_in_date, self._dt("2026-09-01 08:00:00"))
        moved = self._quant(self.bin_a2).filtered("lot_id")
        self.assertEqual(moved.zone_in_date, self._dt("2026-02-01 08:00:00"))

    def test_replenished_pallet_is_picked_last(self):
        """A2 was received before A1 but only just brought into the zone.
        Standard FIFO would pick A2; Zone-Level FIFO picks A1."""
        self._make_quant(
            self.bin_a1,
            10,
            in_date="2026-03-01 08:00:00",
            zone_in_date="2026-03-01 08:00:00",
        )
        reserve = self._make_quant(self.loc_outside, 10, in_date="2026-01-01 08:00:00")
        self._move(self.loc_outside, self.bin_a2, 10)
        self.assertFalse(reserve.exists() and reserve.quantity)

        move = self._move(self.stock_loc, self.customer_loc, 10, done=False)
        self.assertEqual(move.move_line_ids.location_id, self.bin_a1)
        # The replenished pallet still carries the old incoming date, so plain
        # FIFO would have picked it first.
        self.assertEqual(
            self._quant(self.bin_a2).in_date, self._dt("2026-01-01 08:00:00")
        )
