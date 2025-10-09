# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import common


class TestProductAttachmentLink(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {"name": "Test Attribute", "create_variant": "always"}
        )
        cls.value1 = cls.env["product.attribute.value"].create(
            {"name": "Value 1", "attribute_id": cls.attribute.id}
        )
        cls.value2 = cls.env["product.attribute.value"].create(
            {"name": "Value 2", "attribute_id": cls.attribute.id}
        )
        cls.product = cls.env["product.template"].create(
            {
                "name": "Test Template",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute.id,
                            "value_ids": [(6, 0, [cls.value1.id, cls.value2.id])],
                        },
                    )
                ],
            }
        )
        cls.variant_1 = cls.product.product_variant_ids[0]
        cls.variant_2 = cls.product.product_variant_ids[1]
        cls.attachment_model = cls.env["ir.attachment"]

    @classmethod
    def create_attachment(cls, product, name=False):
        name = name if name else "Test file %s" % product.name
        return cls.attachment_model.create(
            {
                "name": name,
                "res_model": product._name,
                "res_id": product.id,
                "datas": base64.b64encode(b"\xff data"),
            }
        )

    def test_product_template_attachments(self):
        template_attachment = self.create_attachment(self.product)
        variant_1_attachment = self.create_attachment(self.variant_1)
        variant_2_attachment = self.create_attachment(self.variant_2)
        action = self.variant_1.action_see_product_template_attachments()
        self.assertIn(
            template_attachment.id, self.attachment_model.search(action["domain"]).ids
        )
        self.assertNotIn(
            variant_1_attachment.id, self.attachment_model.search(action["domain"]).ids
        )
        self.assertNotIn(
            variant_2_attachment.id, self.attachment_model.search(action["domain"]).ids
        )

    def test_product_variant_attachments(self):
        template_attachment = self.create_attachment(self.product)
        variant_1_attachment = self.create_attachment(self.variant_1)
        variant_2_attachment = self.create_attachment(self.variant_2)
        action = self.product.action_see_product_variant_attachments()
        self.assertNotIn(
            template_attachment.id, self.attachment_model.search(action["domain"]).ids
        )
        self.assertIn(
            variant_1_attachment.id, self.attachment_model.search(action["domain"]).ids
        )
        self.assertIn(
            variant_2_attachment.id, self.attachment_model.search(action["domain"]).ids
        )
