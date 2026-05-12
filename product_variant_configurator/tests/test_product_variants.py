# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestProductVariant(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmpl_model = cls.env["product.template"].with_context(
            check_variant_creation=True
        )
        cls.categ_model = cls.env["product.category"]
        cls.categ1 = cls.categ_model.create({"name": "No create variants category"})
        cls.categ2 = cls.categ_model.create(
            {"name": "Create variants category", "no_create_variants": False}
        )
        cls.attribute = cls.env["product.attribute"].create({"name": "Test Attribute"})
        cls.value1 = cls.env["product.attribute.value"].create(
            {"name": "Value 1", "attribute_id": cls.attribute.id}
        )
        cls.value2 = cls.env["product.attribute.value"].create(
            {"name": "Value 2", "attribute_id": cls.attribute.id}
        )

    def test_no_create_variants(self):
        tmpl = self.tmpl_model.create(
            {
                "name": "No create variants template",
                "no_create_variants": "yes",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.set([self.value1.id, self.value2.id])
                            ],
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(tmpl.product_variant_ids), 0)
        tmpl = self.tmpl_model.create(
            {"name": "No variants template", "no_create_variants": "yes"}
        )
        # Odoo by default when there are not attributes will create a product
        self.assertEqual(len(tmpl.product_variant_ids), 1)

    def test_no_create_variants_category(self):
        self.assertTrue(self.categ1.no_create_variants)
        tmpl = self.tmpl_model.create(
            {
                "name": "Category option template",
                "categ_id": self.categ1.id,
                "no_create_variants": "empty",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.set([self.value1.id, self.value2.id])
                            ],
                        },
                    )
                ],
            }
        )
        self.assertTrue(tmpl.no_create_variants == "empty")
        self.assertEqual(len(tmpl.product_variant_ids), 0)
        tmpl = self.tmpl_model.create(
            {
                "name": "No variants template",
                "categ_id": self.categ1.id,
                "no_create_variants": "empty",
            }
        )
        self.assertTrue(tmpl.no_create_variants == "empty")
        self.assertEqual(len(tmpl.product_variant_ids), 1)

    def test_create_variants(self):
        tmpl = self.tmpl_model.create(
            {
                "name": "Create variants template",
                "no_create_variants": "no",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.set([self.value1.id, self.value2.id])
                            ],
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(tmpl.product_variant_ids), 2)
        tmpl = self.tmpl_model.create(
            {"name": "No variants template", "no_create_variants": "no"}
        )
        self.assertEqual(len(tmpl.product_variant_ids), 1)

    def test_create_variants_category(self):
        self.assertFalse(self.categ2.no_create_variants)
        tmpl = self.tmpl_model.create(
            {
                "name": "Category option template",
                "categ_id": self.categ2.id,
                "no_create_variants": "empty",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.set([self.value1.id, self.value2.id])
                            ],
                        },
                    )
                ],
            }
        )
        self.assertTrue(tmpl.no_create_variants == "empty")
        self.assertEqual(len(tmpl.product_variant_ids), 2)
        tmpl = self.tmpl_model.create(
            {
                "name": "No variants template",
                "categ_id": self.categ2.id,
                "no_create_variants": "empty",
            }
        )
        self.assertTrue(tmpl.no_create_variants == "empty")
        self.assertEqual(len(tmpl.product_variant_ids), 1)

    def test_category_change(self):
        self.assertTrue(self.categ1.no_create_variants)
        tmpl = self.tmpl_model.create(
            {
                "name": "Category option template",
                "categ_id": self.categ1.id,
                "no_create_variants": "empty",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [
                                Command.set([self.value1.id, self.value2.id])
                            ],
                        },
                    )
                ],
            }
        )
        self.assertTrue(tmpl.no_create_variants == "empty")
        self.assertEqual(len(tmpl.product_variant_ids), 0)
        self.categ1.no_create_variants = False
        self.assertEqual(len(tmpl.product_variant_ids), 2)
