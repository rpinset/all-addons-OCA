# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from .common import RouteCommon


class TestRouteSecurity(RouteCommon):
    def test_user_access_own_routes(self):
        """Test user can access routes they follow"""
        route1 = self._create_route(self.area_north)
        route2 = self._create_route(self.area_south)
        checkpoint1 = self._create_checkpoint(route2, self.partner_1)
        routes = self.Route.with_user(self.route_user1).search([])
        self.assertEqual(len(routes), 1)
        self.assertIn(self.route_user1.partner_id, route1.message_partner_ids)
        routes = self.Route.with_user(self.route_user2).search([])
        self.assertEqual(len(routes), 1)
        self.assertEqual(len(route2.checkpoint_ids), 1)
        self.assertIn(self.route_user2.partner_id, route2.message_partner_ids)
        self.assertIn(self.route_user2.partner_id, checkpoint1.message_partner_ids)
        routes = self.Route.with_user(self.route_manager).search([])
        self.assertIn(route1, routes)
        self.assertIn(route2, routes)
        # Make route_user2 follower of route1
        # now route_user2 should see both routes
        route1.message_subscribe(self.route_user2.partner_id.ids)
        routes = self.Route.with_user(self.route_user2).search([])
        self.assertEqual(len(routes), 2)
        # change the user of route2 to route_user1
        # the new user should see both routes and checkpoints(added as follower)
        route2.user_id = self.route_user1
        routes = self.Route.with_user(self.route_user1).search([])
        self.assertEqual(len(routes), 2)
        self.assertEqual(len(route2.message_partner_ids), 2)
        self.assertIn(self.route_user1.partner_id, route2.message_partner_ids)
        self.assertIn(self.route_user1.partner_id, checkpoint1.message_partner_ids)
        checkpoint2 = self._create_checkpoint(route2, self.partner_2)
        self.assertEqual(len(checkpoint2.message_partner_ids), 2)
        self.assertIn(self.route_user1.partner_id, checkpoint1.message_partner_ids)
        self.assertIn(self.route_user2.partner_id, checkpoint1.message_partner_ids)
