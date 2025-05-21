# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestSaleQuotationBuilder(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env["product.product"]
        cls.SaleTemplate = cls.env["sale.order.template"]
        cls.product_1 = cls.Product.create(
            {
                "name": "Test product 1",
                "type": "service",
                "list_price": 100,
                "taxes_id": [(6, 0, [])],
            }
        )
        cls.product_2 = cls.Product.create(
            {
                "name": "Test product 2",
                "type": "service",
                "list_price": 150,
                "taxes_id": [(6, 0, [])],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.sale_template_1 = cls.SaleTemplate.create(
            {
                "name": "Template 1",
                "website_description": "<p>Template description</p>",
                "sale_order_template_line_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_1.id,
                            "website_description": "<p>Product 1 description</p>",
                        }
                    )
                ],
                "sale_order_template_option_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_2.id,
                            "website_description": "<p>Product 2 description</p>",
                        }
                    )
                ],
            }
        )

    def test_sale_template_from_product(self):
        """Test that the sale template is created from the products and that the
        website description are set correctly.
        """
        sale_template_form = Form(self.env["sale.order.template"])
        self.product_1.quotation_only_description = "<p>Product 1 description</p>"
        self.product_2.quotation_only_description = "<p>Product 2 description</p>"
        sale_template_form.name = "Template 1"
        with sale_template_form.sale_order_template_line_ids.new() as line_form:
            line_form.product_id = self.product_1
        with sale_template_form.sale_order_template_option_ids.new() as line_form:
            line_form.product_id = self.product_2
        with sale_template_form.sale_order_template_line_ids.new() as line_note:
            line_note.display_type = "line_note"
            line_note.name = "This is a note"
        sale_template = sale_template_form.save()
        template_line_note = sale_template.sale_order_template_line_ids.filtered(
            lambda line: line.display_type == "line_note"
        )
        template_line_1 = sale_template.sale_order_template_line_ids.filtered(
            lambda line: line.product_id == self.product_1
        )
        template_line_2 = sale_template.sale_order_template_option_ids.filtered(
            lambda line: line.product_id == self.product_2
        )
        self.assertEqual(
            template_line_1.website_description, "<p>Product 1 description</p>"
        )
        self.assertEqual(
            template_line_2.website_description, "<p>Product 2 description</p>"
        )
        self.assertFalse(template_line_note.website_description)

    def test_sale_from_template(self):
        """Test that the sale order is created from the template and that the
        website description are set correctly.
        """
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = self.partner
        sale_form.sale_order_template_id = self.sale_template_1
        order = sale_form.save()
        sale_line_contract_1 = order.order_line.filtered(
            lambda line: line.product_id == self.product_1
        )
        sale_line_contract_2 = order.sale_order_option_ids.filtered(
            lambda line: line.product_id == self.product_2
        )
        self.assertEqual(order.website_description, "<p>Template description</p>")
        self.assertEqual(
            sale_line_contract_1.website_description, "<p>Product 1 description</p>"
        )
        self.assertEqual(
            sale_line_contract_2.website_description, "<p>Product 2 description</p>"
        )
        action = self.sale_template_1.action_open_template()
        self.assertEqual(
            action["url"],
            "/@/sale_quotation_builder/template/%d" % self.sale_template_1.id,
        )
