# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools import mute_logger

from .common import TestRoutePlanningRmaSaleCommon


class TestRoutePlanningRmaSale(TestRoutePlanningRmaSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.order.route_area_id = False
        cls.order.action_confirm()
        cls.order.picking_ids.button_validate()

    def test_rma_with_route_area(self):
        # Create rma
        wizard = self._rma_sale_wizard(self.order)
        wizard.reception_route_area_id = self.area_north
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        self.assertEqual(rma.reception_route_area_id, self.area_north)
        rma.reception_move_id.quantity = rma.product_uom_qty
        reception_picking = rma.reception_move_id.picking_id
        self.assertEqual(
            reception_picking.location_dest_id, self.area_north.location_id
        )
        self.assertEqual(
            rma.reception_move_id.location_dest_id, self.area_north.location_id
        )
        self.assertTrue(reception_picking.has_route_planning)
        checkpoint = reception_picking.route_checkpoint_ids
        checkpoint.route_id.action_planned()
        reception_picking.button_validate()
        next_reception_picking = reception_picking._get_next_transfers()
        self.assertTrue(next_reception_picking)
        self.assertEqual(next_reception_picking.route_area_id, self.area_north)
        self.assertEqual(
            next_reception_picking.location_id, self.area_north.location_id
        )
        self.assertEqual(
            next_reception_picking.location_dest_id, self.warehouse.rma_loc_id
        )
        next_reception_picking.button_validate()
        self.assertEqual(next_reception_picking.state, "done")
        self.assertEqual(rma.state, "received")

    def test_rma_without_route_area(self):
        self.partner_1.route_area_id = False
        wizard = self._rma_sale_wizard(self.order)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        self.assertFalse(rma.reception_route_area_id)
        self.assertFalse(rma.reception_move_id.picking_id.route_area_id)

    @mute_logger("odoo.models.unlink")
    def test_rma_route_area_change(self):
        wizard = self._rma_sale_wizard(self.order)
        wizard.reception_route_area_id = self.area_north
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        self.assertEqual(rma.reception_route_area_id, self.area_north)
        reception_picking = rma.reception_move_id.picking_id
        self.assertEqual(reception_picking.route_area_id, self.area_north)
        self.assertEqual(
            rma.reception_move_id.location_dest_id, self.area_north.location_id
        )
        self.assertEqual(
            reception_picking.location_dest_id, self.area_north.location_id
        )
        self.assertTrue(reception_picking.has_route_planning)
        in_checkpoint_0 = reception_picking.route_checkpoint_ids
        rma.reception_route_area_id = self.area_south
        self.assertEqual(reception_picking.route_area_id, self.area_south)
        self.assertEqual(
            rma.reception_move_id.location_dest_id, self.area_south.location_id
        )
        self.assertEqual(
            reception_picking.location_dest_id, self.area_south.location_id
        )
        self.assertFalse(in_checkpoint_0.exists())
        self.assertTrue(reception_picking.has_route_planning)
        in_checkpoint_1 = reception_picking.route_checkpoint_ids
        rma.reception_route_area_id = False
        self.assertFalse(reception_picking.route_area_id)
        self.assertNotEqual(
            rma.reception_move_id.location_dest_id, self.area_south.location_id
        )
        self.assertNotEqual(
            reception_picking.location_dest_id, self.area_south.location_id
        )
        self.assertFalse(in_checkpoint_1.exists())
        self.assertFalse(reception_picking.has_route_planning)
        reception_picking.button_validate()
        self.assertEqual(reception_picking.state, "done")
