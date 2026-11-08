# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.stock_removal_zone_fifo.tests.common import ZoneFifoCommon


class TestZoneFifoLocationZone(ZoneFifoCommon):
    """Only _get_zone_location is overridden here, so only it is tested.
    What is done with the zones it returns is tested in stock_removal_zone_fifo."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (cls.zone_a | cls.zone_b).write({"is_zone": True})

    def test_zone_is_the_flagged_location(self):
        self.assertEqual(self.bin_a1._get_zone_location(), self.zone_a)
        self.assertEqual(self.bin_a2._get_zone_location(), self.zone_a)
        self.assertEqual(self.bin_b1._get_zone_location(), self.zone_b)
        self.assertFalse(self.loc_outside._get_zone_location())

    def test_unflagged_locations_are_in_no_zone(self):
        """This module takes the definition over, so the removal strategy of an
        ancestor no longer draws a zone."""
        (self.zone_a | self.zone_b).write({"is_zone": False})
        self.assertTrue(self.zone_a.removal_strategy_id)
        self.assertFalse(self.bin_a1._get_zone_location())
        self.assertFalse(self.bin_b1._get_zone_location())
