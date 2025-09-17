# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.product_contract.tests.test_sale_order import (
    TestSaleOrder as TestContractSaleOrder,
)


class TestSaleOrder(TestContractSaleOrder):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.transmit_method_post = cls.env.ref("account_invoice_transmit_method.post")

    def test_0(self):
        self.sale.transmit_method_id = self.transmit_method_post
        self.sale.action_confirm()
        self.assertEqual(
            self.order_line1.contract_id.transmit_method_id, self.transmit_method_post
        )
