# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestCompanyDefaultPartnerPricelist(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_pricelist = self.env.ref("product.list0")
        self.pricelist_1 = self.env["product.pricelist"].create(
            {"name": "Test pricelist 1"}
        )
        self.pricelist_2 = self.env["product.pricelist"].create(
            {"name": "Test pricelist 2"}
        )
        self.pricelist_3 = self.env["product.pricelist"].create(
            {"name": "Test pricelist 3"}
        )
        self.partner = self.env["res.partner"].create({"name": "Test customer"})

    def test_company_default_partner_pricelist(self):
        """Test Company Default Partner Pricelist"""
        # By default, the pricelist of the partner is the first valid pricelist
        self.assertEqual(self.partner.property_product_pricelist, self.base_pricelist)
        # When the default is changed for the active company, the pricelist of
        # the partner is the one assigned to the current company
        self.env.company.default_property_product_pricelist_id = self.pricelist_2
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.property_product_pricelist, self.pricelist_2)

        self.env.company.default_property_product_pricelist_id = self.pricelist_3
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.property_product_pricelist, self.pricelist_3)

        self.env.company.default_property_product_pricelist_id = False
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.property_product_pricelist, self.base_pricelist)

        # Finally, when modified explicitly, the pricelist is the one
        # set by the user
        self.partner.property_product_pricelist = self.pricelist_1
        self.assertEqual(self.partner.property_product_pricelist, self.pricelist_1)

    def test_company_pricelist_create(self):
        self.env["ir.property"].sudo().search(
            [("name", "=", "property_product_pricelist")]
        ).unlink()
        company = self.env["res.company"].create(
            [
                {
                    "name": "Test Company",
                    "default_property_product_pricelist_id": self.base_pricelist.id,
                }
            ]
        )
        properties = (
            self.env["ir.property"]
            .sudo()
            .search(
                [
                    ("company_id", "=", company.id),
                    (
                        "value_reference",
                        "=",
                        "product.pricelist,%s" % self.base_pricelist.id,
                    ),
                ]
            )
        )
        self.assertEqual(len(properties), 1, "Properties count must be equal to 1")
        self.assertEqual(
            properties[0].name,
            "property_product_pricelist",
            "Properties name must be equal to 'property_product_pricelist'",
        )
