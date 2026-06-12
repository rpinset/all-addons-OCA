# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo import Command
from odoo.tests import Form
from odoo.tools import mute_logger

from .common import RouteCommon


class TestPartnerVisitWindow(RouteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        States = cls.env["res.country.state"]
        cls.country_spain = cls.env.ref("base.es")
        cls.country_france = cls.env.ref("base.fr")
        cls.state_madrid = States.create(
            {
                "name": "Madrid",
                "code": "MD",
                "country_id": cls.country_spain.id,
            }
        )
        cls.state_barcelona = States.create(
            {
                "name": "Barcelona",
                "code": "BCL",
                "country_id": cls.country_spain.id,
            }
        )
        cls.area_spain = cls.env["route.area"].create(
            {
                "name": "Spain Area",
                "code": "ES",
                "country_ids": [Command.set(cls.country_spain.ids)],
                "auto_assign": True,
            }
        )
        cls.area_madrid = cls.env["route.area"].create(
            {
                "name": "Madrid Area",
                "code": "MAD",
                "country_ids": [Command.set(cls.country_spain.ids)],
                "state_ids": [Command.set([cls.state_madrid.id])],
                "auto_assign": True,
            }
        )
        cls.area_madrid_center = cls.env["route.area"].create(
            {
                "name": "Madrid Center",
                "code": "MAD_C",
                "country_ids": [Command.set(cls.country_spain.ids)],
                "state_ids": [Command.set([cls.state_madrid.id])],
                "zip_ids": [
                    Command.create({"zip_from": "28000", "zip_to": "28099"}),
                    Command.create({"zip_from": "30000", "zip_to": "30099"}),
                ],
                "auto_assign": True,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Spanish Partner"})

    def test_match_by_country_only(self):
        self.assertFalse(self.partner.route_area_id)
        self.partner.country_id = self.country_spain
        self.assertEqual(self.partner.route_area_id, self.area_spain)

    def test_match_by_country_and_state(self):
        self.assertFalse(self.partner.route_area_id)
        self.partner.write(
            {
                "country_id": self.country_spain.id,
                "state_id": self.state_madrid.id,
            }
        )
        self.assertEqual(self.partner.route_area_id, self.area_madrid)
        self.partner.state_id = self.state_barcelona
        self.assertEqual(self.partner.route_area_id, self.area_spain)
        self.partner.write(
            {
                "country_id": self.country_france.id,
                "state_id": False,
            }
        )
        self.assertFalse(self.partner.route_area_id)

    def test_match_by_zip_range(self):
        # Disable other areas to test only zip range matching
        self.area_madrid.auto_assign = False
        self.area_spain.auto_assign = False
        self.assertFalse(self.partner.route_area_id)
        self.partner.write(
            {
                "country_id": self.country_spain.id,
                "state_id": self.state_madrid.id,
                "zip": "28045",
            }
        )
        self.assertEqual(self.partner.route_area_id, self.area_madrid_center)
        self.partner.zip = "29000"
        self.assertFalse(self.partner.route_area_id)
        self.partner.zip = "30000"
        self.assertEqual(self.partner.route_area_id, self.area_madrid_center)

    def test_partner_template_onchange(self):
        """Test that setting a visit window template creates visit windows"""
        self.assertFalse(self.partner_2.route_visitwindow_ids)
        with Form(self.partner_2) as partner_form:
            partner_form.route_visitwindow_template_id = self.visit_window_template
        # Should create visit windows based on template
        self.assertEqual(len(self.partner_2.route_visitwindow_ids), 7)
        self.assertFalse(self.partner_2.route_visitwindow_template_id)

    def test_partner_duplicate_day_of_week(self):
        """Test that creating duplicate visit windows for the same day fails."""
        self.env["route.partner.visitwindow"].create(
            {
                "partner_id": self.partner_2.id,
                "day_of_week": "0",  # Monday
                "time_from": 9 * 60,
                "time_to": 12 * 60,
            }
        )
        with (
            mute_logger("odoo.sql_db"),
            self.assertRaises(UniqueViolation),
            self.cr.savepoint(),
        ):
            self.env["route.partner.visitwindow"].create(
                {
                    "partner_id": self.partner_2.id,
                    "day_of_week": "0",  # Monday
                    "time_from": 14 * 60,
                    "time_to": 16 * 60,
                }
            )
