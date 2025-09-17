# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.contract.tests.test_contract import TestContractBase


@tagged("-at_install", "post_install")
class TestContractSaleMandate(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_bank = cls.env["res.partner.bank"].create(
            {
                "acc_number": "1234",
                "partner_id": cls.partner.id,
            }
        )
        cls.mandate = cls.env["account.banking.mandate"].create(
            {
                "partner_id": cls.partner.id,
                "partner_bank_id": cls.partner_bank.id,
                "signature_date": "2017-01-01",
            }
        )
        cls.product1 = cls.env.ref("product.product_product_1")
        cls.contract_template1 = cls.env["contract.template"].create(
            {"name": "Template 1"}
        )
        cls.sale = cls.env.ref("sale.sale_order_2")
        cls.product1.with_company(cls.sale.company_id.id).write(
            {
                "is_contract": True,
                "recurrence_number": 12,
                "recurrence_interval": "monthly",
                "recurring_rule_type": "monthlylastday",
                "recurring_invoicing_type": "post-paid",
                "property_contract_template_id": cls.contract_template1.id,
            }
        )
        cls.sale.mandate_id = cls.mandate
        cls.order_line1 = cls.sale.order_line.filtered(
            lambda line: line.product_id == cls.product1
        )

    def test_01(self):
        """
        Data:
            - A sale order with a mandate
        Test case:
            - Confirm the sale order
        Expected result:
            - The mandate of the sale order is copied on the generated
              contract
        """
        self.order_line1._compute_product_contract_data()
        self.sale.action_confirm()
        contracts = self.sale.order_line.mapped("contract_id")
        self.assertEqual(len(contracts), 1)
        # Set mandate_required on the contract
        contracts[0].payment_mode_id.payment_method_id.mandate_required = True
        self.assertEqual(contracts[0].mandate_id, self.mandate)
