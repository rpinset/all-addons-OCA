# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpBoMPriority(TransactionCase):
    def setUp(self):
        super().setUp()
        Product = self.env["product.product"]
        Bom = self.env["mrp.bom"]

        self.product = Product.create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )

        self.bom_low = Bom.create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "type": "normal",
                "priority": "0",  # Low
            }
        )

        self.bom_high = Bom.create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "type": "normal",
                "priority": "3",  # Very High
            }
        )

    def test_001_bom_find_(self):
        """Test that _bom_find selects the BoM with the highest priority"""
        bom_by_product = self.env["mrp.bom"]._bom_find(self.product)
        selected_bom = bom_by_product.get(self.product)

        self.assertEqual(
            selected_bom.id,
            self.bom_high.id,
            "Expected BoM with priority 3",
        )
