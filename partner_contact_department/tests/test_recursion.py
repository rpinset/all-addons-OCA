# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from odoo.exceptions import UserError
from odoo.tests import Form, common, new_test_user


class TestRecursion(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.lang"].load_lang("es_ES")
        cls.uid = new_test_user(
            cls.env, login="test_user", groups="base.group_partner_manager"
        )

        # Instances
        cls.dpt1 = cls.env["res.partner.department"].create({"name": "Dpt. 1"})
        cls.dpt2 = cls.env["res.partner.department"].create(
            {"name": "Dep. 2", "parent_id": cls.dpt1.id}
        )

    def test_recursion(self):
        """Testing recursion"""
        dpt3 = self.env["res.partner.department"].create(
            {"name": "Dep. 3", "parent_id": self.dpt2.id}
        )
        # Creating a parent's child department using dpt1.
        with self.assertRaises(UserError):
            self.dpt1.write(vals={"parent_id": dpt3.id})

    def test_order(self):
        dpt3 = self.env["res.partner.department"].create({"name": "A"})
        dpt3.with_context(lang="es_ES").name = "ES A"
        all_ids = (self.dpt1 | self.dpt2 | dpt3).ids
        dpts = self.env["res.partner.department"].search([("id", "in", all_ids)])
        self.assertRecordValues(
            dpts,
            [
                {"name": "A", "display_name": "A"},
                {"name": "Dpt. 1", "display_name": "Dpt. 1"},
                {"name": "Dep. 2", "display_name": "Dpt. 1 / Dep. 2"},
            ],
        )
        # Test order is language-aware
        self.dpt1.with_context(lang="es_ES").name = "Dpt. 1 ES"
        dpts_es = (
            self.env["res.partner.department"]
            .with_context(lang="es_ES")
            .search([("id", "in", all_ids)])
        )
        self.assertRecordValues(
            dpts_es,
            [
                {"name": "Dpt. 1 ES", "display_name": "Dpt. 1 ES"},
                {"name": "Dep. 2", "display_name": "Dpt. 1 ES / Dep. 2"},
                {"name": "ES A", "display_name": "ES A"},
            ],
        )

    def test_creation(self):
        dpt_f = Form(
            self.env["res.partner.department"],
            "partner_contact_department.res_partner_department_tree_view",
        )
        self.assertFalse(dpt_f.display_name)
        dpt_f.name = "test"
        self.assertEqual(dpt_f.display_name, "test")
        dpt_f.parent_id = self.dpt1
        self.assertEqual(dpt_f.display_name, "Dpt. 1 / test")
        dpt = dpt_f.save()
        self.assertEqual(dpt.display_name, "Dpt. 1 / test")

    def test_grandparent_rename(self):
        dpt3 = self.env["res.partner.department"].create(
            {"name": "Dep. 3", "parent_id": self.dpt2.id}
        )
        self.dpt1.name = "Dpt. 1 changed"
        self.assertEqual(dpt3.display_name, "Dpt. 1 changed / Dep. 2 / Dep. 3")
