# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPosDeposit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.deposit_product = cls.env.ref("pos_container_deposit.demo_deposit_product")
        cls.product = cls.env.ref("pos_container_deposit.demo_product")
        cls.product_template = cls.product.product_tmpl_id

    def test_product_behavior(self):
        """
        Test that product search, write, copy behaves as expected with deposit products
        """
        self.assertIn(
            self.product,
            self.env["product.product"].search(
                [
                    ("deposit_product_id", "=", self.deposit_product.id),
                ]
            ),
        )
        self.assertIn(
            self.product_template,
            self.env["product.template"].search(
                [
                    ("deposit_product_id", "=", self.deposit_product.id),
                ]
            ),
        )
        self.product_template.deposit_product_id = False
        self.assertFalse(self.product.deposit_product_id)
        self.product.deposit_product_id = self.deposit_product
        self.assertEqual(self.product_template.deposit_product_id, self.deposit_product)
        product2 = self.product.copy({})
        self.assertEqual(product2.deposit_product_id, self.deposit_product)
        self.assertEqual(self.product_template.deposit_product_id, self.deposit_product)
        template2 = self.product_template.copy()
        self.assertEqual(template2.deposit_product_id, self.deposit_product)

    def test_pos_session(self):
        """
        Be sure the extra field and domain are included
        """
        params = self.env["pos.session"]._loader_params_product_product()
        self.assertIn("deposit_product_id", params["search_params"]["fields"])
