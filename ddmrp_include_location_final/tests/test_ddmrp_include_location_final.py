# Copyright 2025 ForgeFlow S.L. (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.ddmrp.tests.common import TestDdmrpCommon


class TestDdmrp(TestDdmrpCommon):
    def test_01_incoming_quantity_from_final_location(self):
        picking = self.pickingModel.with_user(self.user).create(
            {
                "picking_type_id": self.picking_type_in.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.warehouse.wh_input_stock_loc_id.id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test move",
                            "product_id": self.productA.id,
                            "product_uom": self.productA.uom_id.id,
                            "product_uom_qty": 20,
                            "location_id": self.supplier_location.id,
                            "location_dest_id": self.warehouse.wh_input_stock_loc_id.id,
                            "location_final_id": self.binA.id,
                        },
                    )
                ],
            }
        )
        picking.action_confirm()
        self.bufferModel.cron_ddmrp()
        # The move with final location is detected.
        self.assertEqual(self.buffer_a.incoming_dlt_qty, 20.0)
        picking2 = self.pickingModel.with_user(self.user).create(
            {
                "picking_type_id": self.picking_type_in.id,
                "location_id": self.warehouse.wh_input_stock_loc_id.id,
                "location_dest_id": self.binA.id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test move",
                            "product_id": self.productA.id,
                            "product_uom": self.productA.uom_id.id,
                            "product_uom_qty": 20,
                            "location_id": self.warehouse.wh_input_stock_loc_id.id,
                            "location_dest_id": self.binA.id,
                            "move_orig_ids": [(4, picking.move_ids.id)],
                        },
                    )
                ],
            }
        )
        picking2.action_confirm()
        self.bufferModel.cron_ddmrp()
        # The move with final location is now ignored, and only counts the one incoming.
        self.assertEqual(self.buffer_a.incoming_dlt_qty, 20.0)
