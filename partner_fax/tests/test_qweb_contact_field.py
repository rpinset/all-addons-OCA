# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestQwebContactField(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "fax": "1234567890",
            }
        )

    def test_qweb_contact_field_fax_displayed(self):
        Contact = self.env["ir.qweb.field.contact"]
        result = Contact.value_to_html(self.partner, {"fields": ["name", "fax"]})
        self.assertIn("1234567890", result)
        self.assertIn('itemprop="faxNumber"', result)

    def test_qweb_contact_field_fax_hidden_if_not_set(self):
        self.partner.fax = None
        Contact = self.env["ir.qweb.field.contact"]
        result = Contact.value_to_html(self.partner, {"fields": ["name", "fax"]})
        self.assertNotIn('itemprop="faxNumber"', result)

    def test_qweb_contact_field_fax_hidden_by_default(self):
        Contact = self.env["ir.qweb.field.contact"]
        result = Contact.value_to_html(self.partner, {})
        self.assertNotIn("1234567890", result)
        self.assertNotIn('itemprop="faxNumber"', result)
