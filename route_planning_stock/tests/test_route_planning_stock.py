# Copyright 2025 Tecnativa - Carlos Lopez
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import RecordCapturer, users
from odoo.tools import mute_logger

from odoo.addons.route_planning.tests.common import RouteCommon


class TestRoutePlanningStock(RouteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                test_route_planning_require_warehouse=True,
            )
        )
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.area_north.warehouse_id = cls.warehouse
        cls.area_south.warehouse_id = cls.warehouse
        cls.picking_type = cls.warehouse.out_type_id
        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "is_storable": True}
        )
        # Create quants for products to ensure stock availability
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product_a.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "quantity": 10.0,
            }
        )
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.picking_type.id,
                "partner_id": cls.partner_1.id,
                "location_dest_id": cls.area_north.location_id.id,
                "route_area_id": cls.area_north.id,
                "move_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_a.id,
                            "product_uom_qty": 1,
                            "name": cls.product_a.display_name,
                        }
                    )
                ],
            }
        )

    @mute_logger("odoo.models.unlink")
    def test_unlink_incident_type(self):
        """
        Test that trying to delete the incident type used for
        picking cancellation raises a UserError.
        """
        with self.assertRaisesRegex(
            Exception,
            "You cannot delete this incident type",
        ):
            incident_type = self.env.ref("route_planning_stock.route_incident_cancel")
            incident_type.unlink()
        new_incident_type = self.env["route.incident.type"].create(
            {"name": "Test Incident Type", "rescheduled": False}
        )
        # This one should be deletable
        new_incident_type.unlink()

    def test_create_area(self):
        """
        Test that creating a route area without a warehouse raises a UserError
        and that creating it with a warehouse
        works fine and creates the necessary stock records.
        """
        with self.assertRaisesRegex(
            Exception,
            "You must set a warehouse for the Route Areas created.",
        ):
            self.env["route.area"].create(
                {"name": "Area without warehouse", "code": "AWO", "warehouse_id": False}
            )
        new_area = self.env["route.area"].create(
            {
                "name": "Area with warehouse",
                "code": "RTW",
                "warehouse_id": self.warehouse.id,
            }
        )
        self.assertTrue(new_area.location_id)
        self.assertEqual(new_area.location_id.usage, "transit")

    def test_auto_route_assignment(self):
        """Test that a route and checkpoint are created upon confirming a picking."""
        with RecordCapturer(
            self.env["route.route"], [("route_area_id", "=", self.area_north.id)]
        ) as capture:
            self.picking.button_validate()
        next_picking = self.picking._get_next_transfers()
        self.assertEqual(next_picking.route_area_id, self.picking.route_area_id)
        # To prevent the next lines from being added to the same picking
        next_picking.do_print_picking()
        self.assertEqual(next_picking.route_area_id, self.area_north)
        route = capture.records
        self.assertEqual(len(route), 1)
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        self.assertEqual(len(checkpoint), 1)
        # create another picking to same area and confirm it.
        # It should be assigned to the same route
        picking_2 = self.picking.copy(
            {
                "partner_id": self.partner_2.id,
                "route_area_id": self.area_north.id,
            }
        )
        picking_2.button_validate()
        next_picking2 = picking_2._get_next_transfers()
        self.assertEqual(next_picking2.route_area_id, picking_2.route_area_id)
        # To prevent the next lines from being added to the same picking
        next_picking2.do_print_picking()
        checkpoint2 = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking2.id)]
        )
        self.assertEqual(len(checkpoint2), 1)
        self.assertEqual(
            checkpoint2.route_id,
            route,
        )
        # Create a picking without partner, it should not get a route
        picking_3 = self.picking.copy({"partner_id": False})
        self.assertFalse(picking_3.route_area_id)
        picking_3.button_validate()
        next_picking3 = picking_3._get_next_transfers()
        checkpoint3 = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking3.id)]
        )
        self.assertFalse(checkpoint3)
        checkpoint.route_id.action_planned()
        self.assertEqual(checkpoint.route_id.state, "planned")
        checkpoint.action_done()
        self.assertEqual(checkpoint.route_id.state, "in_progress")
        self.assertEqual(checkpoint.state, "done")
        self.assertEqual(next_picking.state, "done")
        with self.assertRaisesRegex(
            UserError,
            "You cannot move back to planned a checkpoint with a done picking.",
        ):
            checkpoint.action_back_to_planned()
        checkpoint2.action_back_to_planned()
        self.assertEqual(checkpoint.route_id.state, "in_progress")
        self.assertEqual(checkpoint2.state, "planned")
        self.assertEqual(next_picking2.state, "assigned")

    @mute_logger("odoo.models.unlink")
    def test_action_cancel(self):
        """Test that cancelling a picking unlink its checkpoint."""
        self.picking.button_validate()
        next_picking = self.picking._get_next_transfers()
        self.assertEqual(next_picking.route_area_id, self.picking.route_area_id)
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        self.assertEqual(len(checkpoint), 1)
        next_picking.action_cancel()
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        incident_type = self.env.ref("route_planning_stock.route_incident_cancel")
        self.assertEqual(checkpoint.state, "incident")
        self.assertEqual(checkpoint.incident_type_id, incident_type)

    @mute_logger("odoo.models.unlink")
    def test_action_picking_done(self):
        """Test that validating a picking updates its checkpoint."""
        self.picking.button_validate()
        next_picking = self.picking._get_next_transfers()
        self.assertEqual(next_picking.route_area_id, self.picking.route_area_id)
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        self.assertEqual(len(checkpoint), 1)
        with self.assertRaisesRegex(
            Exception,
            "This picking cannot be validated yet",
        ):
            next_picking.button_validate()
        checkpoint.route_id.action_planned()
        next_picking.button_validate()
        self.assertEqual(checkpoint.state, "done")

    def test_route_incident(self):
        """Test route and checkpoint incident handling
        checkpoint 1: done
        checkpoint 2: incident with reschedule
        After that, checkpoint 2 should be rescheduled to a new route
        """
        picking_2 = self.picking.copy(
            {
                "partner_id": self.partner_2.id,
                "route_area_id": self.area_north.id,
            }
        )
        with RecordCapturer(
            self.env["route.route"], [("route_area_id", "=", self.area_north.id)]
        ) as capture:
            self.picking.button_validate()
            next_picking = self.picking._get_next_transfers()
            # To prevent the next lines from being added to the same picking
            next_picking.do_print_picking()
            picking_2.button_validate()
            next_picking2 = picking_2._get_next_transfers()
        route = capture.records
        self.assertEqual(len(route), 1)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2 = route.checkpoint_ids
        checkpoint1.action_done()
        self._create_incident(
            checkpoint2, self.incident_reschedule, "Reschedule to tomorrow"
        )
        self.assertEqual(checkpoint2.state, "incident")
        self.assertEqual(checkpoint2.incident_type_id, self.incident_reschedule)
        # Create a new route
        # checkpoint2 should be rescheduled
        new_route = self._create_route(self.area_north)
        new_route.action_planned()
        self.assertEqual(len(new_route.checkpoint_ids), 1)
        new_checkpoint = new_route.checkpoint_ids[0]
        self.assertEqual(new_checkpoint.origin_checkpoint_id, checkpoint2)
        self.assertEqual(new_checkpoint.picking_id, next_picking2)

    @users("route_user1")
    def test_checkpoint_partial_validation(self):
        """Test checkpoint validation with partial delivery from checkpoint."""
        self.picking.move_ids.product_uom_qty = 10.0
        # enable tracking to test followers
        self.picking.with_context(tracking_disable=False).button_validate()
        next_picking = self.picking._get_next_transfers()
        # Find the checkpoint created for this picking
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        self.assertEqual(len(checkpoint), 1)
        checkpoint.route_id.action_planned()
        # Simulate partial delivery
        next_picking.move_ids.quantity = 6.0
        checkpoint.with_context(tracking_disable=False).action_done()
        self.assertEqual(checkpoint.state, "done")
        self.assertEqual(checkpoint.route_id.state, "done")
        self.assertEqual(next_picking.state, "done")
        backorder = self.env["stock.picking"].search(
            [("backorder_id", "=", next_picking.id)]
        )
        self.assertTrue(backorder)
        self.assertEqual(backorder.move_ids.product_uom_qty, 4.0)
        self.assertEqual(backorder.route_area_id, self.area_north)
        self.assertTrue(backorder.has_route_planning)
