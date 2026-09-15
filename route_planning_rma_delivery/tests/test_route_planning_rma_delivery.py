# Copyright 2025-2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tools import mute_logger

from odoo.addons.route_planning_rma.tests.common import TestRoutePlanningRmaCommon


class TestRoutePlanningRmaDelivery(TestRoutePlanningRmaCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.rma_delivery_strategy = "rma_method"
        cls.env.company.rma_reception_strategy = "rma_method"
        cls.carrier_product = cls.env.ref("route_planning_delivery.product_route_demo")
        cls.carrier = cls.env["delivery.carrier"].create(
            {"name": "Test carrier", "product_id": cls.carrier_product.id}
        )
        cls.carrier_route = cls.env.ref(
            "route_planning_delivery.delivery_carrier_route_demo"
        )
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

    @mute_logger("odoo.models.unlink")
    def test_rma_choose_delivery_carrier(self):
        self.partner_1.route_area_id = False
        wizard = self._rma_stock_return_wizard()
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
        self.assertTrue(rma)
        self.assertEqual(rma.state, "confirmed")
        self.assertFalse(rma.carrier_id)
        self.assertFalse(rma.reception_route_area_id)
        self.assertFalse(rma.route_area_id)
        reception_picking = rma.reception_move_id.picking_id
        # Change reception carrier (area_north)
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "reception")
        self.assertFalse(wizard_form.carrier_id)
        self.assertFalse(wizard_form.route_area_id)
        wizard_form.carrier_id = self.carrier_route
        wizard_form.route_area_id = self.area_north
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.reception_carrier_id, self.carrier_route)
        self.assertEqual(rma.reception_route_area_id, self.area_north)
        self.assertEqual(reception_picking.carrier_id, self.carrier_route)
        self.assertEqual(reception_picking.route_area_id, self.area_north)
        self.assertTrue(reception_picking.route_checkpoint_ids)
        self.assertEqual(
            reception_picking.route_checkpoint_ids.route_id.route_area_id,
            self.area_north,
        )
        # Change reception route (area_south)
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "reception")
        self.assertEqual(wizard_form.carrier_id, self.carrier_route)
        self.assertEqual(wizard_form.route_area_id, self.area_north)
        wizard_form.route_area_id = self.area_south
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.reception_carrier_id, self.carrier_route)
        self.assertEqual(rma.reception_route_area_id, self.area_south)
        self.assertEqual(reception_picking.carrier_id, self.carrier_route)
        self.assertEqual(reception_picking.route_area_id, self.area_south)
        self.assertTrue(reception_picking.route_checkpoint_ids)
        self.assertEqual(
            reception_picking.route_checkpoint_ids.route_id.route_area_id,
            self.area_south,
        )
        # Change reception carrier
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "reception")
        self.assertEqual(wizard_form.carrier_id, self.carrier_route)
        self.assertEqual(wizard_form.route_area_id, self.area_south)
        wizard_form.carrier_id = self.carrier
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.reception_carrier_id, self.carrier)
        self.assertFalse(rma.reception_route_area_id)
        self.assertEqual(reception_picking.carrier_id, self.carrier)
        self.assertFalse(reception_picking.route_area_id)
        self.assertFalse(reception_picking.route_checkpoint_ids)
        reception_picking.button_validate()
        self.assertEqual(reception_picking.state, "done")
        self.assertEqual(rma.state, "received")
        # Create return
        res = rma.action_return()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        wizard = wizard_form.save()
        wizard.action_deliver()
        self.assertTrue(rma.delivery_move_ids.picking_id)
        rma_picking = rma.delivery_move_ids.picking_id
        self.assertFalse(rma_picking.carrier_id)
        self.assertFalse(rma_picking.route_area_id)
        # Change delivery route (area_north)
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "delivery")
        self.assertFalse(wizard_form.carrier_id)
        self.assertFalse(wizard_form.route_area_id)
        wizard_form.carrier_id = self.carrier_route
        wizard_form.route_area_id = self.area_north
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.carrier_id, self.carrier_route)
        self.assertEqual(rma.route_area_id, self.area_north)
        self.assertEqual(rma_picking.carrier_id, self.carrier_route)
        self.assertEqual(rma_picking.route_area_id, self.area_north)
        # Change delivery route (area_south)
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "delivery")
        self.assertEqual(wizard_form.carrier_id, self.carrier_route)
        self.assertEqual(wizard_form.route_area_id, self.area_north)
        wizard_form.route_area_id = self.area_south
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.carrier_id, self.carrier_route)
        self.assertEqual(rma.route_area_id, self.area_south)
        self.assertEqual(rma_picking.carrier_id, self.carrier_route)
        self.assertEqual(rma_picking.route_area_id, self.area_south)
        # Change delivery carrier
        res = rma.action_open_choose_carrier_wizard()
        wizard_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        self.assertEqual(wizard_form.carrier_type, "delivery")
        self.assertEqual(wizard_form.carrier_id, self.carrier_route)
        self.assertEqual(wizard_form.route_area_id, self.area_south)
        wizard_form.carrier_id = self.carrier
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.assertEqual(rma.carrier_id, self.carrier)
        self.assertFalse(rma.route_area_id)
        self.assertEqual(rma_picking.carrier_id, self.carrier)
        self.assertFalse(rma_picking.route_area_id)
        rma_picking.button_validate()
        self.assertEqual(rma_picking.state, "done")
        self.assertEqual(rma.state, "returned")

    def test_rma_onchange_route_area(self):
        self.company.rma_delivery_strategy = "rma_method"
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
        rma_form = Form(rma)
        rma_form.carrier_id = self.carrier_route
        rma_form.route_area_id = self.area_north
        rma_form.carrier_id = self.carrier
        self.assertFalse(rma_form.route_area_id)

    def test_rma_write_validations(self):
        self.company.rma_reception_strategy = "rma_method"
        self.company.rma_delivery_strategy = "rma_method"
        wizard = self._rma_stock_return_wizard()
        picking_action = wizard.action_create_returns()
        picking_return = self.env["stock.picking"].browse(picking_action["res_id"])
        rma = picking_return.move_ids.rma_receiver_ids
        rma.write(
            {
                "reception_carrier_id": self.carrier.id,
                "reception_route_area_id": self.area_north.id,
            }
        )
        self.assertEqual(rma.reception_carrier_id, self.carrier)
        # self.assertFalse(rma.reception_route_area_id)
        rma.write(
            {"carrier_id": self.carrier_route.id, "route_area_id": self.area_north.id}
        )
        self.assertEqual(rma.carrier_id, self.carrier_route)
        self.assertEqual(rma.route_area_id, self.area_north)

    def test_rma_onchange_recception_route_area(self):
        self.company.rma_reception_strategy = "rma_method"
        rma_form = Form(self.env["rma"])
        rma_form.reception_carrier_id = self.carrier_route
        rma_form.reception_route_area_id = self.area_north
        rma_form.reception_carrier_id = self.carrier
        self.assertFalse(rma_form.reception_route_area_id)
