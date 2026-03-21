# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests.common import Form, TransactionCase


class TestPartnerStreetNumber(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env["res.country"].create(
            {
                "name": "country",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "name",
                "street": "streetname 42",
                "country_id": cls.country.id,
            }
        )

    def test_country_form(self):
        """Test the test function of the country form"""
        with Form(self.env.ref("base.nl")) as nl_form:
            nl_form.partner_street_number_test_value = "hello world"
            self.assertIn(
                "<dd>hello world</dd>", nl_form.partner_street_number_test_result
            )
            nl_form.partner_street_number_test_value = "hello world 42"
            self.assertIn(
                "<dd>hello world</dd>", nl_form.partner_street_number_test_result
            )
            self.assertIn("<dd>42</dd>", nl_form.partner_street_number_test_result)
            nl_form.partner_street_number_test_value = "hello world 42a"
            self.assertIn(
                "<dd>hello world</dd>", nl_form.partner_street_number_test_result
            )
            self.assertIn("<dd>42</dd>", nl_form.partner_street_number_test_result)
            self.assertIn("<dd>a</dd>", nl_form.partner_street_number_test_result)

    def test_wizard(self):
        """Test the bulk update wizard"""
        partner = self.partner
        country = self.country
        self.assertEqual(partner.street_name, "streetname")
        self.assertEqual(partner.street_number, "42")
        partner.street_number = "43"
        self.assertEqual(partner.street, "streetname 43")
        country.partner_street_number_format = (
            "{{object.street_number}} {{object.street_name}}"
        )
        self.env["partner.street.number.wizard"].with_context(
            active_ids=partner.ids
        ).create(
            {
                "direction": "_inverse_street_data",
            }
        ).action_set()
        self.assertEqual(partner.street, "43 streetname")

    def test_graceful_degradation(self):
        """Test that we have sensible fallbacks when the user made mistakes"""
        partner = self.partner
        country = self.country
        country.partner_street_number_regex = "(?<P"
        partner.street = "hello world 42"
        self.assertEqual(partner.street_name, "hello world 42")
        self.assertFalse(partner.street_number)
        self.assertFalse(partner.street_number2)
        country.partner_street_number_format = "{{ wrong_name.wrong_property }}"
        partner.street_name = "hello world"
        partner.street_number = "43"
        self.assertEqual(partner.street, "hello world")
