from odoo.tests import TransactionCase

from odoo.addons.openupgrade_framework import openupgrade_test


@openupgrade_test
class TestProductMigration(TransactionCase):
    def test_pricelist(self):
        partner = self.env.ref("base.user_demo").partner_id
        company = self.env["res.company"].search(
            [
                ("name", "=", "Product migration test company"),
            ]
        )
        pricelist_main = self.env["product.pricelist"].search(
            [
                ("name", "=", "Pricelist for main company"),
            ]
        )
        pricelist = self.env["product.pricelist"].search(
            [
                ("name", "=", "Pricelist for demo company"),
            ]
        )
        self.assertTrue(company)
        self.assertTrue(pricelist)
        self.assertEqual(partner.property_product_pricelist, pricelist_main)
        self.assertEqual(
            partner.with_company(company).property_product_pricelist, pricelist
        )
