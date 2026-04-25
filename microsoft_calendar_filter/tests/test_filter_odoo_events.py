# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date, datetime

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval

from ..models.res_config_settings import FILTER_ODOO_EVENTS


class TestFilterOdooEvents(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ICP = cls.env["ir.config_parameter"].sudo()

    def test_filter_validation(self):
        # Should not be able to set filter that is not a valid python list.
        with self.assertRaises(ValidationError):
            # Missing ')'
            self.ICP.set_param(FILTER_ODOO_EVENTS, "[('location', '!=', False])")
        # Should not be able to refer to field not existing on calendar.event.
        with self.assertRaises(ValidationError):
            self.ICP.set_param(
                FILTER_ODOO_EVENTS,
                "[('not_a_field', 'ilike', 'amsterdam')])",
            )
        # Set valid filter (even though no records might satisfy criteria).
        self.ICP.set_param(
            FILTER_ODOO_EVENTS,
            "[('location', 'ilike', 'amsterdam')]",
        )
        odoo_filter_txt = self.ICP.get_param(FILTER_ODOO_EVENTS)
        odoo_filter = safe_eval(odoo_filter_txt)
        self.assertEqual(odoo_filter[0][0], "location")

    def test_filter_odoo_events(self):
        """Check that events are properly filtered."""
        Partner = self.env["res.partner"]
        Users = self.env["res.users"]
        Calendar = self.env["calendar.event"]
        # Create a user.
        partner_tom = Partner.create(
            {
                "is_company": False,
                "name": "Tom Bombadill",
                "ref": "TB001",
                "email": "tom.bombadill@oldforest.middleearth",
            }
        )
        user_tom = Users.with_context(
            tracking_disable=True, no_reset_password=True
        ).create(
            {
                "name": partner_tom.name,
                "login": partner_tom.email,
                "partner_id": partner_tom.id,
            }
        )
        TomCalendar = Calendar.with_user(user_tom)
        year = date.today().year
        event_amsterdam = TomCalendar.create(
            {
                "name": "Event in De Balie",
                "start": datetime(year, 1, 15, 8, 0),
                "stop": datetime(year, 1, 15, 18, 0),
                "partner_ids": [(4, partner_tom.id)],
                "location": "Amsterdam - De Balie",
            }
        )
        event_rotterdam = TomCalendar.create(
            {
                "name": "Event in Lantaarn/Venster",
                "start": datetime(year, 1, 15, 8, 0),
                "stop": datetime(year, 1, 15, 18, 0),
                "partner_ids": [(4, partner_tom.id)],
                "location": "Rotterdam - Lantaarn/Venster",
            }
        )
        # With no filter set both events should be selected for
        # synchronization (if sync active, but that is out of test scope).
        self.ICP.set_param(FILTER_ODOO_EVENTS, "[]")
        odoo_filter_txt = self.ICP.get_param(FILTER_ODOO_EVENTS)
        self.assertEqual(odoo_filter_txt, "[]")
        events = TomCalendar._get_microsoft_records_to_sync(full_sync=False)
        self.assertIn(event_amsterdam, events)
        self.assertIn(event_rotterdam, events)
        # Actually we only want events in Amsterdam in Tom's Outlook agenda.
        self.ICP.set_param(
            FILTER_ODOO_EVENTS,
            "[('location', 'ilike', 'amsterdam')]",
        )
        # This is also in the validation test, but we need the get_param to
        # flush the change to the database.
        odoo_filter_txt = self.ICP.get_param(FILTER_ODOO_EVENTS)
        odoo_filter = safe_eval(odoo_filter_txt)
        self.assertEqual(odoo_filter[0][0], "location")
        # The method name '_get_microsoft_records_to_sync' is quite misleading,
        # it returns Odoo records to sync to microsoft, not the other way around.
        events = TomCalendar._get_microsoft_records_to_sync(full_sync=False)
        self.assertIn(event_amsterdam, events)
        self.assertNotIn(event_rotterdam, events)
