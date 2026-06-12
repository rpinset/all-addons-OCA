# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import Command, fields
from odoo.tests import Form, new_test_user, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class RouteCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"].with_company(cls.company)
        cls.VisitWindowTemplate = cls.env["route.visitwindow.template"]
        cls.IncidentType = cls.env["route.incident.type"]
        cls.Route = cls.env["route.route"]
        cls.route_user1 = new_test_user(
            cls.env, "route_user1", groups="route_planning.group_route_planning_user"
        )
        cls.route_user2 = new_test_user(
            cls.env, "route_user2", groups="route_planning.group_route_planning_user"
        )
        cls.route_manager = new_test_user(
            cls.env,
            "route_manager",
            groups="route_planning.group_route_planning_manager",
        )
        cls.area_north = cls.env["route.area"].create(
            {
                "code": "NORTH",
                "name": "North Area",
                "user_id": cls.route_user1.id,
                "time_start": 8.0,
            }
        )
        cls.area_south = cls.env["route.area"].create(
            {
                "code": "SOUTH",
                "name": "South Area",
                "user_id": cls.route_user2.id,
                "time_start": 9.0,
            }
        )
        cls.all_days = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ]
        all_days_template = [
            Command.create(
                {
                    "day_of_week": day_of_week,
                    "time_from": 8.0,
                    "time_to": 18.0,
                }
            )
            for day_of_week in cls.all_days
        ]
        cls.visit_window_template = cls.VisitWindowTemplate.create(
            {
                "name": "Standard 8-18",
                "line_ids": all_days_template,
            }
        )
        cls.env.company.partner_id.write(
            {
                "partner_latitude": 40.432705895463606,
                "partner_longitude": -3.6970388945265644,
            }
        )
        cls.partner_1 = cls.Partner.create(
            {
                "name": "Customer 1",
                "street": "123 Main St",
                "city": "Madrid",
                "country_id": cls.env.ref("base.es").id,
                "route_area_id": cls.area_north.id,
                "partner_latitude": 40.41831064312621,
                "partner_longitude": -3.7143479878277055,
            }
        )
        cls.partner_2 = cls.Partner.create(
            {
                "name": "Customer 2",
                "street": "456 Oak Ave",
                "city": "Barcelona",
                "country_id": cls.env.ref("base.es").id,
                "route_area_id": cls.area_north.id,
                "partner_latitude": 40.41429270410794,
                "partner_longitude": -3.692142478954325,
            }
        )
        cls.partner_3 = cls.Partner.create(
            {
                "name": "Customer 3",
                "street": "789 Pine Rd",
                "city": "Valencia",
                "country_id": cls.env.ref("base.es").id,
                "route_area_id": cls.area_north.id,
                "partner_latitude": 40.453370156222306,
                "partner_longitude": -3.6884337678686903,
            }
        )
        cls.incident_no_reschedule = cls.IncidentType.create(
            {"name": "Customer Not Available", "rescheduled": False}
        )
        cls.incident_reschedule = cls.IncidentType.create(
            {"name": "Traffic Delay", "rescheduled": True}
        )

    def _create_route(self, area, schedule_date=None):
        if schedule_date is None:
            schedule_date = fields.Date.context_today(self.env.user)
        # enable tracking to test followers
        route_form = Form(self.Route.with_context(tracking_disable=False))
        route_form.route_area_id = area
        route_form.schedule_date = schedule_date
        return route_form.save()

    def _create_checkpoint(self, route, partner):
        # enable tracking to test followers
        return (
            self.env["route.checkpoint"]
            .with_context(tracking_disable=False)
            .create({"route_id": route.id, "partner_id": partner.id})
        )

    def _create_route_and_checkpoints(self, area, partners):
        route = self._create_route(area)
        for partner in partners:
            self._create_checkpoint(route, partner)
        return route

    def _create_incident(self, checkpoint, incident_type, note=""):
        context = {
            "active_ids": checkpoint.ids,
            "active_model": checkpoint._name,
        }
        incident_form = Form(self.env["route.create.incident"].with_context(**context))
        incident_form.incident_type_id = incident_type
        incident_form.note = note
        wizard_incident = incident_form.save()
        wizard_incident.action_create_incident()
        return wizard_incident
