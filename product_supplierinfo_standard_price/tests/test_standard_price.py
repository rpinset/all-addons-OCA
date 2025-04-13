# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestStandardPrice(TransactionCase):
    def setUp(self):
        super().setUp()
        # Product and its supplier info
        self.office_chair = self.env.ref("product.product_delivery_01")
        self.office_chair_std_p = self.office_chair.standard_price
        self.office_chair_suppinfo = self.office_chair.variant_seller_ids[0]
        self.office_chair_suppinfo_price = self.office_chair_suppinfo.price
        # Others
        self.uom_dozen = self.env.ref("uom.product_uom_dozen")

    def test_00__get_standard_price_fields(self):
        res = self.office_chair_suppinfo._get_standard_price_fields()
        self.assertNotIn("discount", res)
        self.assertIn("price", res)

    def test_01_compute_theoritical_standard_price_no_discount(self):
        self.office_chair_suppinfo._compute_theoritical_standard_price()
        self.assertEqual(
            self.office_chair_suppinfo.theoritical_standard_price,
            self.office_chair_suppinfo_price,
        )

    def test_02_set_new_price(self):
        # Changing Standard price with supplier info
        self.office_chair_suppinfo.set_product_standard_price_from_supplierinfo()
        self.assertEqual(
            self.office_chair_suppinfo_price,
            self.office_chair.standard_price,
        )

    def test_03_change_po_uom(self):
        # Test if product standard price is well calculated with purchase uom
        self.office_chair.uom_po_id = self.uom_dozen
        self.office_chair_suppinfo.set_product_standard_price_from_supplierinfo()
        self.assertEqual(
            self.office_chair_suppinfo_price / self.uom_dozen.factor_inv,
            self.office_chair.standard_price,
        )
