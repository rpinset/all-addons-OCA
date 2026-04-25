# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo
from odoo.fields import Command
from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@odoo.tests.tagged("post_install", "-at_install")
class TestPoSPartnerPricelistLoadBackground(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env["base"].with_context(**DISABLED_MAIL_CONTEXT).env
        cls.product_categ1 = cls.env["product.category"].create({"name": "Category 01"})
        cls.product1 = cls.env["product.product"].create(
            {"name": "Product 1", "list_price": 100}
        )
        cls.product2 = cls.env["product.product"].create(
            {"name": "Product 2", "list_price": 100, "categ_id": cls.product_categ1.id}
        )
        cls.product3 = cls.env["product.product"].create(
            {"name": "Product 3", "list_price": 80, "categ_id": cls.product_categ1.id}
        )
        cls.pricelist1 = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist_01",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.product1.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.product2.id,
                            "applied_on": "2_product_category",
                            "categ_id": cls.product_categ1.id,
                            "fixed_price": 70,
                        }
                    ),
                ],
            }
        )

        cls.pricelist2 = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist_02",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.product3.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                ],
            }
        )

    def test_get_pos_ui_partner_pricelist_background(self):
        """Test get_pos_ui_partner_pricelist_background returns the correct pricelist items"""
        pos_pricelist_items = self.env[
            "pos.session"
        ].get_pos_ui_partner_pricelist_background(self.pricelist1.id, [])[0]["items"]
        self.assertEqual(len(pos_pricelist_items), 2)
        self.pricelist1.item_ids.write(
            {
                "compute_price": "formula",
                "base": "pricelist",
                "base_pricelist_id": self.pricelist2.id,
            }
        )

        pos_pricelists = self.env[
            "pos.session"
        ].get_pos_ui_partner_pricelist_background(self.pricelist1.id, [])
        # We get partner pricelist items and base pricelist items
        self.assertEqual(len(pos_pricelists), 2)
        self.assertEqual(len(pos_pricelists[0]["items"]), 2)
        self.assertEqual(len(pos_pricelists[1]["items"]), 1)
