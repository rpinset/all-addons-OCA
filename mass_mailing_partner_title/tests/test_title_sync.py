from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestMassMailingPartnerTitle(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.list_model = cls.env["mailing.list"]
        cls.contact_model = cls.env["mailing.contact"]
        cls.partner_model = cls.env["res.partner"]
        cls.title_mr = cls.env["res.partner.title"].create({"name": "Mr."})
        cls.title_dr = cls.env["res.partner.title"].create({"name": "Dr."})
        cls.list_normal = cls.list_model.create({"name": "List"})
        cls.list_mandatory = cls.list_model.create(
            {"name": "Mandatory", "partner_mandatory": True}
        )

    def test_contact_copies_partner_title(self):
        partner = self.partner_model.create(
            {
                "name": "Partner A",
                "email": "partner.a@example.com",
                "title_id": self.title_mr.id,
            }
        )
        contact = self.contact_model.create(
            {
                "partner_id": partner.id,
                "email": partner.email,
                "list_ids": [Command.set(self.list_normal.ids)],
            }
        )
        self.assertEqual(contact.title_id, self.title_mr)

    def test_partner_write_updates_contact_title(self):
        partner = self.partner_model.create(
            {
                "name": "Partner B",
                "email": "partner.b@example.com",
                "title_id": self.title_mr.id,
            }
        )
        contact = self.contact_model.create(
            {
                "partner_id": partner.id,
                "email": partner.email,
                "list_ids": [Command.set(self.list_normal.ids)],
            }
        )
        partner.write({"title_id": self.title_dr.id})
        self.assertEqual(contact.title_id, self.title_dr)

    def test_partner_created_from_contact_keeps_title(self):
        contact = self.contact_model.create(
            {
                "name": "Partner C",
                "email": "partner.c@example.com",
                "title_id": self.title_dr.id,
                "list_ids": [Command.set(self.list_mandatory.ids)],
            }
        )
        self.assertTrue(contact.partner_id)
        self.assertEqual(contact.partner_id.title_id, self.title_dr)

    def test_contact_write_partner_updates_title(self):
        partner = self.partner_model.create(
            {
                "name": "Partner A",
                "email": "partner.a@example.com",
                "title_id": self.title_dr.id,
            }
        )
        partner_2 = self.partner_model.create(
            {
                "name": "Partner B",
                "email": "partner.a@example.com",
                "title_id": self.title_mr.id,
            }
        )
        contact = self.contact_model.create(
            {
                "partner_id": partner.id,
                "email": partner.email,
                "list_ids": [Command.set(self.list_normal.ids)],
            }
        )

        self.assertEqual(contact.title_id, self.title_dr)

        contact.write({"partner_id": partner_2.id})
        self.assertEqual(contact.title_id, self.title_mr)
