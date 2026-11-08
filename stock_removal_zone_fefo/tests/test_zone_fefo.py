# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.stock_removal_zone_fifo.tests.common import ZoneFifoCommon


class TestZoneFefo(ZoneFifoCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        zone_fefo = cls.env.ref("stock_removal_zone_fefo.removal_zone_fefo")
        # The category wins over the locations when the strategy is resolved,
        # so it has to carry Zone-Level FEFO too.
        cls.categ.removal_strategy_id = zone_fefo
        (cls.zone_a | cls.zone_b).write({"removal_strategy_id": zone_fefo.id})
        cls.product.write({"tracking": "lot", "use_expiration_date": True})

    @classmethod
    def _make_lot_quant(cls, location, quantity, removal_date, zone_in_date):
        lot = cls.env["stock.lot"].create(
            {
                "name": f"LOT-{location.name}",
                "product_id": cls.product.id,
                "removal_date": removal_date,
            }
        )
        return cls.env["stock.quant"].create(
            {
                "product_id": cls.product.id,
                "location_id": location.id,
                "lot_id": lot.id,
                "quantity": quantity,
                "in_date": zone_in_date,
                "zone_in_date": zone_in_date,
            }
        )

    def test_removal_strategy_order(self):
        order = self.env["stock.quant"]._get_removal_strategy_order("zone_fefo")
        self.assertEqual(order, "removal_date, zone_in_date, in_date, id")

    def test_standard_fefo_untouched(self):
        # not the full string: other modules may add their own sort keys to it
        order = self.env["stock.quant"]._get_removal_strategy_order("fefo")
        self.assertNotIn("zone_in_date", order)

    def test_expiry_wins_over_the_zone_entry_date(self):
        self._make_lot_quant(
            self.bin_a1,
            10,
            removal_date="2026-12-01 08:00:00",
            zone_in_date="2026-01-01 08:00:00",
        )
        self._make_lot_quant(
            self.bin_a2,
            10,
            removal_date="2026-06-01 08:00:00",
            zone_in_date="2026-05-01 08:00:00",
        )
        move = self._move(self.stock_loc, self.customer_loc, 10, done=False)
        self.assertEqual(move.move_line_ids.location_id, self.bin_a2)

    def test_zone_entry_date_breaks_an_expiry_tie(self):
        """A1 and A2 expire on the same date, so A2 wins on the zone entry."""
        same_expiry = "2026-12-01 08:00:00"
        self._make_lot_quant(
            self.bin_a1,
            10,
            removal_date=same_expiry,
            zone_in_date="2026-05-01 08:00:00",
        )
        self._make_lot_quant(
            self.bin_a2,
            10,
            removal_date=same_expiry,
            zone_in_date="2026-01-01 08:00:00",
        )
        move = self._move(self.stock_loc, self.customer_loc, 10, done=False)
        self.assertEqual(move.move_line_ids.location_id, self.bin_a2)
