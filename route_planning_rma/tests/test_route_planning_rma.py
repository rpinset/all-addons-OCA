# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tools import mute_logger

from .common import TestRoutePlanningRmaCommon


class TestRoutePlanningRma(TestRoutePlanningRmaCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        picking_form = Form(
            cls.env["stock.picking"].with_context(
                default_picking_type_id=cls.warehouse.out_type_id.id
            )
        )
        picking_form.partner_id = cls.partner_1
        with picking_form.move_ids_without_package.new() as line_form:
            line_form.product_id = cls.product_a
            line_form.product_uom_qty = 1
        cls.picking = picking_form.save()
        cls.picking.action_confirm()
        cls.picking.button_validate()

    @classmethod
    def _rma_stock_return_wizard(cls):
        stock_return_picking_form = Form(
            cls.env["stock.return.picking"].with_context(
                active_ids=cls.picking.ids,
                active_id=cls.picking.id,
                active_model=cls.picking._name,
            )
        )
        stock_return_picking_form.create_rma = True
        stock_return_picking_form.rma_operation_id = cls.operation
        return_wizard = stock_return_picking_form.save()
        for move in cls.picking.move_ids_without_package:
            return_wizard.product_return_moves.filtered(
                lambda x, move=move: x.move_id == move
            ).quantity = move.quantity
        return return_wizard

    def test_rma_with_route_area(self):
        wizard = self._rma_stock_return_wizard()
        wizard.reception_route_area_id = self.area_north
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
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
        # Create return
        rma.route_area_id = self.area_south
        res = rma.action_return()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard = wizard_form.save()
        wizard.action_deliver()
        self.assertTrue(rma.delivery_move_ids.picking_id)
        rma_picking = rma.delivery_move_ids.picking_id
        self.assertEqual(rma_picking.route_area_id, self.area_south)
        self.assertEqual(rma_picking.location_dest_id, self.area_south.location_id)
        # Change route area
        rma.route_area_id = self.area_north
        self.assertEqual(rma_picking.route_area_id, self.area_north)
        self.assertEqual(rma_picking.location_dest_id, self.area_north.location_id)
        rma_picking.move_ids.quantity = rma_picking.move_ids.product_uom_qty
        rma_picking.button_validate()
        self.assertEqual(rma_picking.state, "done")
        next_rma_picking = rma_picking._get_next_transfers()
        self.assertTrue(next_rma_picking)
        self.assertEqual(next_rma_picking.route_area_id, self.area_north)
        self.assertEqual(next_rma_picking.location_id, self.area_north.location_id)
        checkpoint = next_rma_picking.route_checkpoint_ids
        checkpoint.route_id.action_planned()
        next_rma_picking.button_validate()
        self.assertEqual(next_rma_picking.state, "done")

    def test_rma_without_route_area(self):
        self.partner_1.route_area_id = False
        wizard = self._rma_stock_return_wizard()
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        rma.reception_move_id.quantity = rma.product_uom_qty
        rma.reception_move_id.picking_id.button_validate()
        # Create return
        res = rma.action_return()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard = wizard_form.save()
        wizard.action_deliver()
        self.assertTrue(rma.delivery_move_ids.picking_id)
        rma_picking = rma.delivery_move_ids.picking_id
        self.assertFalse(rma_picking.route_area_id)
        self.assertNotEqual(rma_picking.location_dest_id, self.area_north.location_id)
        rma_picking.button_validate()
        self.assertEqual(rma_picking.state, "done")
        next_rma_picking = rma_picking._get_next_transfers()
        self.assertFalse(next_rma_picking)

    @mute_logger("odoo.models.unlink")
    def test_rma_route_area_change(self):
        wizard = self._rma_stock_return_wizard()
        wizard.reception_route_area_id = self.area_north
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
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
        # Create out picking + change route area
        rma.operation_id.action_create_delivery = "manual_on_confirm"
        rma.route_area_id = self.area_north
        res = rma.action_return()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard = wizard_form.save()
        wizard.action_deliver()
        out_picking = rma.delivery_move_ids.picking_id
        self.assertEqual(out_picking.route_area_id, self.area_north)
        self.assertEqual(
            rma.delivery_move_ids.location_dest_id, self.area_north.location_id
        )
        self.assertEqual(out_picking.location_dest_id, self.area_north.location_id)
        self.assertFalse(out_picking.has_route_planning)
        rma.route_area_id = self.area_south
        self.assertEqual(out_picking.route_area_id, self.area_south)
        self.assertEqual(
            out_picking.move_ids.location_dest_id, self.area_south.location_id
        )
        self.assertEqual(out_picking.location_dest_id, self.area_south.location_id)
        self.assertFalse(out_picking.has_route_planning)
        rma.route_area_id = False
        self.assertFalse(out_picking.route_area_id)
        self.assertNotEqual(
            out_picking.move_ids.location_dest_id, self.area_south.location_id
        )
        self.assertNotEqual(out_picking.location_dest_id, self.area_south.location_id)
        self.assertFalse(out_picking.has_route_planning)

    @mute_logger("odoo.models.unlink")
    def test_rma_rma_route_area_change(self):
        self.env.company.rma_new_rma_button_from_rma = True
        wizard = self._rma_stock_return_wizard()
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        reception_picking = rma.reception_move_id.picking_id
        reception_picking.button_validate()
        self.assertEqual(reception_picking.state, "done")
        self.assertEqual(rma.state, "received")
        res = rma.action_return()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard = wizard_form.save()
        wizard.action_deliver()
        out_picking = rma.delivery_move_ids.picking_id
        out_picking.button_validate()
        self.assertEqual(out_picking.state, "done")
        self.assertEqual(rma.state, "returned")
        # new rma
        res = rma.action_create_rma()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard_form.reception_route_area_id = self.area_north
        wizard = wizard_form.save()
        new_rma = wizard.create_rma()
        self.assertTrue(new_rma)
        self.assertEqual(new_rma.state, "confirmed")
        self.assertEqual(new_rma.reception_route_area_id, self.area_north)
        reception_picking_extra = new_rma.reception_move_id.picking_id
        self.assertEqual(reception_picking_extra.route_area_id, self.area_north)
        self.assertEqual(
            new_rma.reception_move_id.location_dest_id, self.area_north.location_id
        )
        self.assertEqual(
            reception_picking_extra.location_dest_id, self.area_north.location_id
        )
        self.assertTrue(reception_picking_extra.has_route_planning)
        in_checkpoint_0 = reception_picking_extra.route_checkpoint_ids
        new_rma.reception_route_area_id = self.area_south
        self.assertEqual(reception_picking_extra.route_area_id, self.area_south)
        self.assertEqual(
            new_rma.reception_move_id.location_dest_id, self.area_south.location_id
        )
        self.assertEqual(
            reception_picking_extra.location_dest_id, self.area_south.location_id
        )
        self.assertFalse(in_checkpoint_0.exists())
        self.assertTrue(reception_picking_extra.has_route_planning)
