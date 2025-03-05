# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from odoo.exceptions import UserError
from odoo.tests import common


class TestRecursion(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department_obj = cls.env["res.partner.department"]

        # Instances
        cls.dpt1 = cls.department_obj.create({"name": "Dpt. 1"})
        cls.dpt2 = cls.department_obj.create(
            {"name": "Dep. 2", "parent_id": cls.dpt1.id}
        )

    def test_recursion(self):
        """Testing recursion"""
        self.dpt3 = self.department_obj.create(
            {"name": "Dep. 3", "parent_id": self.dpt2.id}
        )
        # Creating a parent's child department using dpt1.
        with self.assertRaises(UserError):
            self.dpt1.write(vals={"parent_id": self.dpt3.id})

    def test_order(self):
        dpt3 = self.env["res.partner.department"].create({"name": "A"})
        dpts = self.env["res.partner.department"].search(
            [("id", "in", (self.dpt1 | self.dpt2 | dpt3).ids)]
        )
        self.assertRecordValues(
            dpts,
            [
                {"name": "A", "display_name": "A"},
                {"name": "Dpt. 1", "display_name": "Dpt. 1"},
                {"name": "Dep. 2", "display_name": "Dpt. 1 / Dep. 2"},
            ],
        )
