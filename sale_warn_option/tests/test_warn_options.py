# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.tests.common import TransactionCase


class TestWarnOptions(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.partner_sale_warn_warning = cls.env["warn.option"].create(
            {
                "name": "warning",
                "allowed_warning_usage": "partner_sale_warn",
                "allowed_warning_type": "warning",
            }
        )
        cls.partner_sale_warn_blocking = cls.env["warn.option"].create(
            {
                "name": "block",
                "allowed_warning_usage": "partner_sale_warn",
                "allowed_warning_type": "block",
            }
        )
        cls.product = cls.env["product.template"].create(
            {
                "name": "Test Product",
            }
        )
        cls.product_sale_line_warn_warning = cls.env["warn.option"].create(
            {
                "name": "warning",
                "allowed_warning_usage": "product_sale_warn",
                "allowed_warning_type": "warning",
            }
        )
        cls.product_sale_line_warn_blocking = cls.env["warn.option"].create(
            {
                "name": "block",
                "allowed_warning_usage": "product_sale_warn",
                "allowed_warning_type": "block",
            }
        )

    def test_partner_warn_options(self):
        """Test Warn Options on Partner Form"""
        partner_f = self.env["res.partner"].new(
            {
                "sale_warn": "warning",
                "sale_warn_option": self.partner_sale_warn_warning.id,
            }
        )
        partner_f._onchange_sale_warn_option()
        self.assertEqual(partner_f.sale_warn_msg, "warning")
        partner_f.sale_warn = "block"
        partner_f.sale_warn_option = self.partner_sale_warn_blocking.id
        partner_f._onchange_sale_warn_option()
        self.assertEqual(partner_f.sale_warn_msg, "block")

    def test_product_warn_options(self):
        """Test Warn Options on Product Form"""
        product_f = self.env["product.template"].new(
            {
                "sale_line_warn": "warning",
                "sale_line_warn_option": self.product_sale_line_warn_warning.id,
            }
        )
        product_f._onchange_sale_line_warn_option()
        self.assertEqual(product_f.sale_line_warn_msg, "warning")
        product_f.sale_line_warn = "block"
        product_f.sale_line_warn_option = self.product_sale_line_warn_blocking.id
        product_f._onchange_sale_line_warn_option()
        self.assertEqual(product_f.sale_line_warn_msg, "block")
