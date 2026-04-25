# Copyright 2025 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
from .common import Common


class TestUpdateCarrierRoute(Common):
    def test_update_carrier_route(self):
        """Switch from one carrier to another and check routing."""
        wh_delivery_rule = self.wh.delivery_route_id.rule_ids[1]
        ship = self._create_picking_chain(self.wh, [(self.product1, 5)])
        self.assertTrue(ship.need_release)
        self.assertFalse(ship.carrier_id)
        self.assertTrue(ship.move_ids.rule_id)
        self.assertFalse(ship.move_ids.route_ids)
        # Set a carrier without route: no change expected
        ship.carrier_id = self.normal_carrier
        self.assertEqual(ship.carrier_id, self.normal_carrier)
        self.assertTrue(current_rule := ship.move_ids.rule_id)
        self.assertFalse(forced_route := ship.move_ids.route_ids)
        # Set a carrier with a route compatible with dest location (Customers)
        # => moves are rerouted
        ship_moves = ship.move_ids
        ship.carrier_id = self.the_poste_carrier
        ship2 = ship_moves.picking_id
        self.assertEqual(ship2.carrier_id, self.the_poste_carrier)
        self.assertTrue(current_rule := ship2.move_ids.rule_id)
        self.assertTrue(forced_route := ship2.move_ids.route_ids)
        self.assertEqual(current_rule, self.the_poste_delivery_rule)
        self.assertEqual(forced_route, self.the_poste_carrier.route_ids)
        # Reset to carrier without route: back on WH delivery route
        ship2_moves = ship2.move_ids
        ship2.carrier_id = self.normal_carrier
        ship3 = ship2_moves.picking_id
        self.assertEqual(ship3.carrier_id, self.normal_carrier)
        self.assertTrue(current_rule := ship3.move_ids.rule_id)
        self.assertTrue(forced_route := ship3.move_ids.route_ids)
        self.assertEqual(current_rule, wh_delivery_rule)
        self.assertEqual(forced_route, wh_delivery_rule.route_id)

    def test_release_carrier_route(self):
        """Release/unrelease a delivery order with a new carrier."""
        wh_pick_rule = self.wh.delivery_route_id.rule_ids[0]
        wh_delivery_rule = self.wh.delivery_route_id.rule_ids[1]
        ship = self._create_picking_chain(self.wh, [(self.product1, 5)])
        self._update_qty_in_location(self.wh.lot_stock_id, self.product1, 5)
        self.assertTrue(ship.need_release)
        self.assertTrue(ship.release_ready)
        # When releasing, the ship will take the usual WH delivery route
        ship.release_available_to_promise()
        pick = ship.move_ids.move_orig_ids.picking_id
        self.assertTrue(pick)
        self.assertEqual(pick.move_ids.rule_id, wh_pick_rule)
        self.assertEqual(pick.picking_type_id, wh_pick_rule.picking_type_id)
        # Unrelease, switch to carrier w/ route and release:
        #   - taking the new route
        #   - assign moves to another ship transfer
        ship.unrelease()
        ship_moves = ship.move_ids
        ship.carrier_id = self.the_poste_carrier
        ship2 = ship_moves.picking_id
        self.assertEqual(ship2.move_ids.rule_id, self.the_poste_delivery_rule)
        ship2.release_available_to_promise()
        pick = ship2.move_ids.move_orig_ids.picking_id
        self.assertTrue(pick)
        self.assertEqual(pick.move_ids.rule_id, self.the_poste_pick_rule)
        self.assertEqual(pick.picking_type_id, self.the_poste_pick_rule.picking_type_id)
        # Unrelease, switch to carrier w/o route and release: back on WH delivery route
        ship2.unrelease()
        ship2_moves = ship2.move_ids
        ship2.carrier_id = self.normal_carrier
        ship3 = ship2_moves.picking_id
        self.assertEqual(ship3.move_ids.rule_id, wh_delivery_rule)
        ship3.release_available_to_promise()
        pick = ship3.move_ids.move_orig_ids.picking_id
        self.assertTrue(pick)
        self.assertEqual(pick.move_ids.rule_id, wh_pick_rule)
        self.assertEqual(pick.picking_type_id, wh_pick_rule.picking_type_id)
