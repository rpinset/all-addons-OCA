# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductIsBulk(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product1 = cls.product_obj.create(
            {"name": "Test Product 1", "uom_id": cls.uom_unit.id}
        )

    def test_01_change_uom(self):
        self.assertEqual(self.product1.is_bulk, False)
        self.product1.uom_id = self.uom_kg
        self.product1._compute_is_bulk()
        self.assertEqual(self.product1.is_bulk, True)
