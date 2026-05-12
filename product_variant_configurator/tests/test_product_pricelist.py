# Copyright 2016 ACSONE SA/NV
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestProductPriceList(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ENVIRONMENTS
        cls.product_template = cls.env["product.template"].with_context(
            check_variant_creation=True
        )
        cls.product_pricelist = cls.env["product.pricelist"]
        cls.supplier_info = cls.env["product.supplierinfo"]
        cls.uom_unit = cls.env["uom.uom"].create(
            {"name": "Units", "relative_factor": "1.0"}
        )
        # Instances: Product attribute
        cls.physical = cls.env["product.category"].create({"name": "Goods"})

        cls.attribute1 = cls.env["product.attribute"].create(
            {"name": "Brand", "sequence": 10}
        )
        cls.value1 = cls.env["product.attribute.value"].create(
            {"name": "Adidas", "attribute_id": cls.attribute1.id}
        )
        cls.value2 = cls.env["product.attribute.value"].create(
            {"name": "Apple", "attribute_id": cls.attribute1.id}
        )

        cls.attribute2 = cls.env["product.attribute"].create(
            {"name": "Color", "sequence": 30}
        )
        cls.value3 = cls.env["product.attribute.value"].create(
            {"name": "White", "attribute_id": cls.attribute2.id}
        )
        cls.value4 = cls.env["product.attribute.value"].create(
            {"name": "Black", "attribute_id": cls.attribute2.id}
        )

        cls.ipad_template = cls.product_template.create(
            {
                "name": "Ipad",
                "no_create_variants": "no",
                "categ_id": cls.physical.id,
                "company_id": False,
                "list_price": 750,
                "standard_price": 500,
                "uom_id": cls.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attribute1.id,
                            "value_ids": [Command.set([cls.value1.id, cls.value2.id])],
                        },
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.attribute2.id,
                            "value_ids": [Command.set([cls.value3.id, cls.value4.id])],
                        },
                    ),
                ],
            }
        )

        cls.ipad_product = cls.ipad_template.product_variant_ids[0]
        cls.partner1 = cls.env["res.partner"].create({"name": "Partner1"})

        cls.iphone_template = cls.product_template.create(
            {
                "name": "Ipad Retina Display",
                "no_create_variants": "yes",
                "categ_id": cls.physical.id,
                "company_id": False,
                "list_price": 500,
                "standard_price": 300,
                "uom_id": cls.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attribute1.id,
                            "value_ids": [Command.set([cls.value1.id, cls.value2.id])],
                        },
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.attribute2.id,
                            "value_ids": [Command.set([cls.value3.id, cls.value4.id])],
                        },
                    ),
                ],
                "seller_ids": [
                    Command.create(
                        {
                            "partner_id": cls.partner1.id,
                            "delay": 3,
                            "min_qty": 1,
                            "price": 300,
                        },
                    ),
                    Command.create(
                        {
                            "partner_id": cls.partner1.id,
                            "delay": 3,
                            "min_qty": 4,
                            "price": 290,
                        },
                    ),
                ],
            }
        )

        cls.pricelist = cls.product_pricelist.create(
            {
                "name": "Pricelist 1",
                "company_id": False,
                "item_ids": [
                    Command.create(
                        {
                            "name": "Rule 20% on ipad product",
                            "product_id": cls.ipad_product.id,
                            "categ_id": cls.physical.id,
                            "min_quantity": 1,
                            "base": "list_price",
                            "applied_on": "0_product_variant",
                            "compute_price": "formula",
                            "price_discount": 20,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Rule 10% on ipad template ",
                            "product_tmpl_id": cls.ipad_template.id,
                            "applied_on": "1_product",
                            "min_quantity": 1,
                            "base": "list_price",
                            "compute_price": "formula",
                            "price_discount": 10,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Rule Min qty 4 10% discount iphone template",
                            "product_tmpl_id": cls.iphone_template.id,
                            "applied_on": "1_product",
                            "base": "list_price",
                            "min_quantity": 4,
                            "compute_price": "percentage",
                            "percent_price": 10,
                        },
                    ),
                ],
            }
        )

    def test_01_price_rule_get_multi(self):
        # Price for ipad product
        # Must be 600
        price = self.pricelist.with_context(
            uom=self.ipad_product.uom_id.id, date="2016-01-01"
        )._price_get(self.ipad_product, 1)[self.pricelist.id]
        self.assertEqual(price, 750 * 0.8)

    def test_02_price_rule_get_multi_template(self):
        # Price for iphone template with correct partner
        # Price must be 450
        price = self.pricelist.with_context(
            uom=self.iphone_template.uom_id.id, date="2016-01-01"
        ).template_price_get(self.iphone_template, 4, self.partner1.id)[
            self.pricelist.id
        ]
        self.assertEqual(price, 500 * 0.9)

    def test_03_price_rule_get_multi_template(self):
        # Price for ipad template
        # must be 500
        price = self.pricelist.with_context(
            uom=self.iphone_template.uom_id.id, date="2016-01-01"
        ).template_price_get(self.iphone_template, 1)[self.pricelist.id]
        self.assertEqual(price, 500)
