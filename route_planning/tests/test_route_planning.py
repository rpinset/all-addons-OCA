# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import users
from odoo.tools import mute_logger

from .common import RouteCommon


class TestRoutePlanning(RouteCommon):
    def test_route_constraints(self):
        route = self._create_route(self.area_north)
        # try plan with no checkpoints
        with self.assertRaisesRegex(
            UserError,
            "Not enough addresses with coordinates for optimisation",
        ):
            route.action_planned()
        # create checkpoint and planned
        checkpoint1 = self._create_checkpoint(route, self.partner_1)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        # try plan again
        with self.assertRaisesRegex(
            UserError,
            "Only draft routes can be planned",
        ):
            route.action_planned()
        # try delete non-draft route
        with self.assertRaisesRegex(
            UserError,
            "You cannot delete routes that are not in draft state",
        ):
            route.unlink()
        with self.assertRaisesRegex(
            UserError,
            "You cannot delete checkpoints that are not in draft state",
        ):
            checkpoint1.unlink()
        with self.assertRaisesRegex(
            UserError,
            r"Checkpoint .* does not have valid coordinates",
        ):
            self.env["route.checkpoint"].create(
                {"route_id": route.id, "latitude": 0.0, "longitude": 0.0}
            )

    def test_route_area_code_unique_constraint(self):
        self.env["route.area"].create({"code": "CODE", "name": "Area"})
        with (
            mute_logger("odoo.sql_db"),
            self.assertRaises(UniqueViolation),
            self.cr.savepoint(),
        ):
            self.env["route.area"].create({"code": "CODE", "name": "Area"})

    @users("route_manager")
    def test_visit_window_time(self):
        VisitWindowTemplateLine = self.env["route.visitwindow.template.line"]
        visit_window_template = self.VisitWindowTemplate.create(
            {"name": "New Template"}
        )
        VisitWindowTemplateLine.create(
            {
                "template_id": visit_window_template.id,
                "day_of_week": "0",
                "time_from": 8.0,
                "time_to": 12.0,
            }
        )
        with self.assertRaisesRegex(
            UserError,
            "The time from must be earlier than the time to.",
        ):
            VisitWindowTemplateLine.create(
                {
                    "template_id": visit_window_template.id,
                    "day_of_week": "1",
                    "time_from": 14.0,
                    "time_to": 10.0,
                }
            )

    @users("route_user1")
    def test_route_flow(self):
        """
        Test that checkpoints are ordered when planning a route.
        All partners without visit windows. Taken from the area start time.
        Expected order after planning:
        checkpoint1: partner1
        checkpoint2: partner2
        checkpoint3: partner3
        """
        partners = self.partner_1 + self.partner_2 + self.partner_3
        route = self._create_route_and_checkpoints(self.area_north, partners)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids.sorted("sequence")
        self.assertEqual(checkpoint1.sequence, 1)
        self.assertEqual(checkpoint2.sequence, 2)
        self.assertEqual(checkpoint3.sequence, 3)
        self.assertGreaterEqual(checkpoint1.schedule_time, 8.0)
        self.assertLessEqual(checkpoint1.schedule_time, 9.0)
        self.assertGreaterEqual(checkpoint2.schedule_time, 8.3)
        self.assertLessEqual(checkpoint2.schedule_time, 9.5)
        self.assertGreaterEqual(checkpoint3.schedule_time, 9.0)
        self.assertLessEqual(checkpoint3.schedule_time, 10.3)
        self.assertEqual(checkpoint1.partner_id, self.partner_1)
        self.assertEqual(checkpoint2.partner_id, self.partner_2)
        self.assertEqual(checkpoint3.partner_id, self.partner_3)
        checkpoint1.action_done()
        self.assertEqual(checkpoint1.state, "done")
        with self.assertRaisesRegex(
            UserError,
            "You cannot set the sequence of checkpoint",
        ):
            checkpoint2.write({"sequence": 1})
        with self.assertRaisesRegex(
            UserError,
            "You must mark previous checkpoints as done.",
        ):
            checkpoint3.action_done()
        checkpoint1.action_back_to_planned()
        self.assertEqual(checkpoint1.state, "planned")

    @users("route_user1")
    def test_route_with_waiting_time(self):
        """
        Test that checkpoints are ordered when planning a route.
        All partners without visit windows. Taken from the area start time.
        The waiting time is set in the route area, 30 minutes.
        Expected order after planning:
        checkpoint1: partner1
        checkpoint2: partner2
        checkpoint3: partner3
        """
        partners = self.partner_1 + self.partner_2 + self.partner_3
        self.area_north.waiting_time = 0.50  # 30 minutes
        route = self._create_route_and_checkpoints(self.area_north, partners)
        route.action_planned()
        self.assertEqual(route.waiting_time, 0.5)
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids.sorted("sequence")
        self.assertEqual(checkpoint1.sequence, 1)
        self.assertEqual(checkpoint2.sequence, 2)
        self.assertEqual(checkpoint3.sequence, 3)
        self.assertGreaterEqual(checkpoint1.schedule_time, 8.5)
        self.assertLessEqual(checkpoint1.schedule_time, 9.0)
        self.assertGreaterEqual(checkpoint2.schedule_time, 9.0)
        self.assertLessEqual(checkpoint2.schedule_time, 9.5)
        self.assertGreaterEqual(checkpoint3.schedule_time, 9.5)
        self.assertLessEqual(checkpoint3.schedule_time, 10.3)
        self.assertEqual(checkpoint1.partner_id, self.partner_1)
        self.assertEqual(checkpoint2.partner_id, self.partner_2)
        self.assertEqual(checkpoint3.partner_id, self.partner_3)

    @users("route_user1")
    def test_route_flow_with_visit_window(self):
        """
        Test that checkpoints are ordered according to visit windows
        when planning a route.
        partner1: without visit window, taken from the area start time
        partner2: without visit window, taken from the area start time
        partner3: with visit window 8am-9am
        Expected order after planning:
        checkpoint1: partner3
        checkpoint2: partner2
        checkpoint3: partner1
        """
        all_days_template = [
            Command.create(
                {
                    "day_of_week": day_of_week,
                    "time_from": 8.0,
                    "time_to": 9.0,
                }
            )
            for day_of_week in self.all_days
        ]
        self.partner_3.route_visitwindow_ids = [Command.clear()] + all_days_template
        partners = self.partner_1 + self.partner_2 + self.partner_3
        route = self._create_route_and_checkpoints(self.area_north, partners)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids.sorted("sequence")
        self.assertEqual(checkpoint1.sequence, 1)
        self.assertEqual(checkpoint2.sequence, 2)
        self.assertEqual(checkpoint3.sequence, 3)
        self.assertGreaterEqual(checkpoint1.schedule_time, 8.0)
        self.assertLessEqual(checkpoint1.schedule_time, 9.0)
        self.assertGreaterEqual(checkpoint2.schedule_time, 8.3)
        self.assertLessEqual(checkpoint2.schedule_time, 9.5)
        self.assertGreaterEqual(checkpoint3.schedule_time, 9.0)
        self.assertLessEqual(checkpoint3.schedule_time, 10.3)
        self.assertEqual(checkpoint1.partner_id, self.partner_3)
        self.assertEqual(checkpoint2.partner_id, self.partner_2)
        self.assertEqual(checkpoint3.partner_id, self.partner_1)

    @users("route_user1")
    def test_route_flow_with_reschedule(self):
        """
        Test that checkpoints are ordered when planning a route.
        All partners without visit windows. Taken from the area start time.
        Expected order after planning:
        checkpoint1: partner1
        checkpoint2: partner2
        checkpoint3: partner3
        Reschedule partner3 before of checkpoint1
        Expected order after reschedule:
        checkpoint1: partner3
        checkpoint2: partner2
        checkpoint3: partner1
        """
        partners = self.partner_1 + self.partner_2 + self.partner_3
        route = self._create_route_and_checkpoints(self.area_north, partners)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids.sorted("sequence")
        self.assertEqual(checkpoint1.sequence, 1)
        self.assertEqual(checkpoint2.sequence, 2)
        self.assertEqual(checkpoint3.sequence, 3)
        self.assertGreaterEqual(checkpoint1.schedule_time, 8.0)
        self.assertLessEqual(checkpoint1.schedule_time, 9.0)
        self.assertGreaterEqual(checkpoint2.schedule_time, 8.3)
        self.assertLessEqual(checkpoint2.schedule_time, 9.5)
        self.assertGreaterEqual(checkpoint3.schedule_time, 9.0)
        self.assertLessEqual(checkpoint3.schedule_time, 10.3)
        self.assertEqual(checkpoint1.partner_id, self.partner_1)
        self.assertEqual(checkpoint2.partner_id, self.partner_2)
        self.assertEqual(checkpoint3.partner_id, self.partner_3)
        # Reschedule checkpoint3 before checkpoint1
        # update the sequence directly because the widget handle do it in the UI
        route.write(
            {
                "checkpoint_ids": [
                    Command.update(checkpoint3.id, {"sequence": 1}),
                    Command.update(checkpoint1.id, {"sequence": 2}),
                    Command.update(checkpoint2.id, {"sequence": 3}),
                ]
            }
        )
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids.sorted("sequence")
        self.assertGreaterEqual(checkpoint1.schedule_time, 8.0)
        self.assertLessEqual(checkpoint1.schedule_time, 9.0)
        self.assertGreaterEqual(checkpoint2.schedule_time, 8.3)
        self.assertLessEqual(checkpoint2.schedule_time, 9.5)
        self.assertGreaterEqual(checkpoint3.schedule_time, 9.0)
        self.assertLessEqual(checkpoint3.schedule_time, 10.3)
        self.assertEqual(checkpoint1.partner_id, self.partner_3)
        self.assertEqual(checkpoint2.partner_id, self.partner_2)
        self.assertEqual(checkpoint3.partner_id, self.partner_1)

    @users("route_user1")
    def test_route_incident(self):
        """Test route and checkpoint incident handling
        checkpoint 1: done
        checkpoint 2: incident with reschedule
        checkpoint 3: incident without reschedule
        After that, checkpoint 2 should be rescheduled to a new route
        """
        partners = self.partner_1 + self.partner_2 + self.partner_3
        route = self._create_route_and_checkpoints(self.area_north, partners)
        route.action_planned()
        self.assertEqual(route.state, "planned")
        checkpoint1, checkpoint2, checkpoint3 = route.checkpoint_ids
        checkpoint1.action_done()
        self._create_incident(
            checkpoint2, self.incident_reschedule, "Reschedule to tomorrow"
        )
        self._create_incident(checkpoint3, self.incident_no_reschedule)
        self.assertEqual(checkpoint2.state, "incident")
        self.assertEqual(checkpoint2.incident_type_id, self.incident_reschedule)
        self.assertEqual(checkpoint2.note, "Reschedule to tomorrow")
        self.assertEqual(checkpoint3.state, "incident")
        self.assertEqual(checkpoint3.incident_type_id, self.incident_no_reschedule)
        self.assertFalse(checkpoint3.note)
        # Create a new route
        # checkpoint2 should be rescheduled
        # checkpoint3 should not be rescheduled
        new_route = self._create_route(self.area_north)
        new_route.action_planned()
        self.assertEqual(len(new_route.checkpoint_ids), 1)
        new_checkpoint = new_route.checkpoint_ids[0]
        self.assertEqual(new_checkpoint.origin_checkpoint_id, checkpoint2)
        self.assertIn(self.route_user1.partner_id, new_checkpoint.message_partner_ids)
