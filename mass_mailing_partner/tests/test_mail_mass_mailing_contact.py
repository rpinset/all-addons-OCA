# Copyright 2015 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Javier Iniesta <javieria@antiun.com>
# Copyright 2020 Tecnativa - Manuel Calero
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command
from odoo.tools import mute_logger

from ..hooks import post_init_hook
from . import base


class MailMassMailingContactCase(base.BaseCase):
    @mute_logger("odoo.models.unlink")
    def test_mailing_contact_email(self):
        partner_1 = self.env["res.partner"].create(
            {
                "name": "Test partner 1",
                "email": "partner1@test.com",
            }
        )
        self.assertFalse(partner_1.mass_mailing_contact_ids)
        partner_2 = self.env["res.partner"].create(
            {
                "name": "Test partner 2",
                "email": "partner2@test.com",
            }
        )

        self.assertFalse(partner_2.mass_mailing_contact_ids)
        contact_1 = self.env["mailing.contact"].create(
            {
                "email": partner_1.email,
                "partner_id": partner_1.id,
                "list_ids": [Command.set(self.mailing_list.ids)],
            }
        )
        self.assertEqual(contact_1, partner_1.mass_mailing_contact_ids)
        contact_2 = self.env["mailing.contact"].create(
            {
                "email": partner_2.email,
                "partner_id": partner_2.id,
                "list_ids": [Command.set(self.mailing_list.ids)],
            }
        )
        self.assertEqual(contact_2, partner_2.mass_mailing_contact_ids)
        partner_2.write({"email": "partner1@test.com"})
        self.assertEqual(contact_2.email, "partner1@test.com")
        contact_2.write({"list_ids": [Command.link(self.mailing_list2.id)]})
        self.assertEqual(contact_2.partner_id, partner_2)
        self.assertIn(contact_1, self.mailing_list.contact_ids)
        self.assertIn(contact_2, self.mailing_list.contact_ids)
        self.assertIn(contact_2, self.mailing_list2.contact_ids)
        self.assertNotEqual(contact_1.partner_id, contact_2.partner_id)

    def test_match_existing_contacts(self):
        contact = self.create_mailing_contact(
            {"email": "partner@test.com", "list_ids": [(6, 0, self.mailing_list.ids)]}
        )
        post_init_hook(self.env)
        self.assertEqual(contact.partner_id.id, self.partner.id)
        self.check_mailing_contact_partner(contact)

    def test_create_mass_mailing_contact(self):
        country_cu = self.env.ref("base.cu")
        category_8 = self.env["res.partner.category"].create(
            {"name": "Test Category 8"}
        )
        category_11 = self.env["res.partner.category"].create(
            {"name": "Test Category 11"}
        )
        contact_vals = {
            "name": "Partner test 2",
            "email": "partner2@test.com",
            "company_name": "TestCompany",
            "country_id": country_cu.id,
            "tag_ids": [(6, 0, (category_8 | category_11).ids)],
            "list_ids": [(6, 0, (self.mailing_list | self.mailing_list2).ids)],
        }
        contact = self.create_mailing_contact(contact_vals)
        self.check_mailing_contact_partner(contact)
        contact_exta = self.create_mailing_contact(
            {
                "email": "partner2@test.com",
                "list_ids": [[6, 0, [self.mailing_list2.id]]],
            }
        )
        self.check_mailing_contact_partner(contact_exta)

    def test_create_mass_mailing_contact_with_subscription(self):
        country_cu = self.env.ref("base.cu")
        category_8 = self.env["res.partner.category"].create(
            {"name": "Test Category 8"}
        )
        category_11 = self.env["res.partner.category"].create(
            {"name": "Test Category 11"}
        )
        contact_vals = {
            "name": "Partner test 2",
            "email": "partner2@test.com",
            "company_name": "TestCompany",
            "country_id": country_cu.id,
            "tag_ids": [(6, 0, (category_8 | category_11).ids)],
            "subscription_ids": [
                (0, 0, {"list_id": self.mailing_list.id}),
                (0, 0, {"list_id": self.mailing_list2.id}),
            ],
        }
        contact = self.create_mailing_contact(contact_vals)
        self.check_mailing_contact_partner(contact)
        contact_exta = self.create_mailing_contact(
            {
                "email": "partner2@test.com",
                "subscription_ids": [(0, 0, {"list_id": self.mailing_list2.id})],
            }
        )
        self.check_mailing_contact_partner(contact_exta)

    def test_write_mass_mailing_contact(self):
        contact = self.create_mailing_contact(
            {"email": "partner@test.com", "list_ids": [(6, 0, self.mailing_list.ids)]}
        )
        contact.write({"partner_id": False})
        self.check_mailing_contact_partner(contact)
        contact2 = self.create_mailing_contact(
            {
                "email": "partner2@test.com",
                "name": "Partner test 2",
                "list_ids": [(6, 0, self.mailing_list.ids)],
            }
        )
        contact2.write({"partner_id": False})
        self.assertFalse(contact2.partner_id)

    def test_onchange_partner(self):
        contact = self.create_mailing_contact(
            {"email": "partner@test.com", "list_ids": [[6, 0, [self.mailing_list.id]]]}
        )
        country_cu = self.env.ref("base.cu")
        category_8 = self.env["res.partner.category"].create(
            {"name": "Test Category 8"}
        )
        category_11 = self.env["res.partner.category"].create(
            {"name": "Test Category 11"}
        )
        partner_vals = {
            "name": "Partner test 2",
            "email": "partner2@test.com",
            "company_id": self.main_company.id,
            "country_id": country_cu.id,
            "category_id": [(6, 0, (category_8 | category_11).ids)],
        }
        partner = self.create_partner(partner_vals)
        contact.partner_id = partner
        contact._onchange_partner_mass_mailing_partner()
        self.check_mailing_contact_partner(contact)

    @mute_logger("odoo.models.unlink")
    def test_partners_merge(self):
        partner_1 = self.create_partner({"name": "Demo 1", "email": "demo1@demo.com"})
        partner_2 = self.create_partner({"name": "Demo 2", "email": "demo2@demo.com"})
        list_1 = self.create_mailing_list({"name": "List test Partners Merge 1"})
        list_2 = self.create_mailing_list({"name": "List test Partners Merge 2"})
        contact_1 = self.create_mailing_contact(
            {
                "email": partner_1.email,
                "name": partner_1.name,
                "partner_id": partner_1.id,
                "list_ids": [(6, 0, [list_1.id])],
            }
        )
        contact_2 = self.create_mailing_contact(
            {
                "email": partner_2.email,
                "name": partner_2.name,
                "partner_id": partner_2.id,
                "list_ids": [(6, 0, [list_1.id, list_2.id])],
            }
        )
        # Wizard partner merge (partner_1 + partner_2) in partner_i1
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {"state": "option"}
        )
        wizard._merge((partner_1 + partner_2).ids, partner_1)
        contact = self.env["mailing.contact"].search(
            [("id", "in", (contact_1 + contact_2).ids)]
        )
        self.assertEqual(len(contact), 1)
        self.assertEqual(contact.list_ids.ids, (list_1 + list_2).ids)
