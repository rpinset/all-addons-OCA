# Copyright 2020 Camptocamp SA
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from .common import PromiseReleaseWeightVolumeCommon


class TestPromiseReleaseWeightVolume(PromiseReleaseWeightVolumeCommon):
    def test_estimated_weight_volume(self):
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.loc_stock, 3
        )
        delivery_pick = self._create_picking_chain(self.wh, [(self.product1, 5)])
        # Ensure _get_processed_quantity overrides values
        # from hooks in stock_picking_volume and delivery_total_weight_from_packaging
        self.assertAlmostEqual(delivery_pick._get_estimated_weight(), 30.0)

        delivery_pick.move_ids._compute_volume()  # force recompute
        self.assertAlmostEqual(delivery_pick.volume, 30.0)
