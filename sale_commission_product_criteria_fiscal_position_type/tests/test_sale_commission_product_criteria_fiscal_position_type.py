# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleCommissionProductCriteriaFiscalPositionType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.agent = cls.env.ref("sale_commission_product_criteria.demo_agent_rules")
        cls.partner_b2c = cls.env["res.partner"].create(
            {
                "name": "Test B2C",
                "fiscal_position_type": "b2c",
                "agent_ids": [(4, cls.agent.id)],
            }
        )
        cls.partner_b2b = cls.env["res.partner"].create(
            {
                "name": "Test B2B",
                "fiscal_position_type": "b2b",
                "agent_ids": [(4, cls.agent.id)],
            }
        )
        cls.partner_no_type = cls.env["res.partner"].create(
            {
                "name": "Test B2B",
                "fiscal_position_type": "",
                "agent_ids": [(4, cls.agent.id)],
            }
        )
        cls.product = cls.env.ref("product.product_product_4")
        cls.product_2 = cls.env.ref("product.product_product_1")
        cls.commission = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules"
        )
        cls.com_item_1 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_1"
        )
        cls.com_item_1.fiscal_position_type = False
        cls.com_item_1_amount = 10
        cls.com_item_2 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_2"
        )
        cls.com_item_2.fiscal_position_type = "b2b"
        cls.com_item_2_amount = 20
        cls.com_item_3 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_3"
        )
        cls.com_item_3.fiscal_position_type = "b2c"
        cls.com_item_4 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_4"
        )
        cls.com_item_4.fiscal_position_type = "b2c"
        cls.com_item_4_amount = 150
        cls.com_item_5_amount = 5
        cls.com_item_5 = cls.env["commission.item"].create(
            {
                "commission_id": cls.commission.id,
                "applied_on": "0_product_variant",
                "commission_type": "fixed",
                "fixed_amount": cls.com_item_5_amount,
                "product_id": cls.product_2.id,
                "fiscal_position_type": False,
            }
        )
        cls.com_item_6_amount = 6
        cls.com_item_6 = cls.env["commission.item"].create(
            {
                "commission_id": cls.commission.id,
                "applied_on": "0_product_variant",
                "commission_type": "fixed",
                "fixed_amount": cls.com_item_6_amount,
                "product_id": cls.product_2.id,
                "fiscal_position_type": "b2b",
            }
        )
        cls.com_item_7 = cls.com_item_5.copy()

    def _create_sale_order(self, product, partner):
        return self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "product_uom_qty": 1.0,
                            "product_uom": product.uom_id.id,
                            "price_unit": 1000,
                        },
                    )
                ],
            }
        )

    def _create_account_invoice(self, product, partner):
        return self.env["account.move"].create(
            {
                "partner_id": partner.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "quantity": 1.0,
                            "product_uom_id": product.uom_id.id,
                            "price_unit": 1000,
                        },
                    )
                ],
            }
        )

    def test_sale_order(self):
        so1 = self._create_sale_order(self.product, self.partner_b2c)
        so1.recompute_lines_agents()
        self.assertEqual(so1.order_line.agent_ids.amount, self.com_item_4_amount)

        so2 = self._create_sale_order(self.product, self.partner_b2b)
        so2.recompute_lines_agents()
        self.assertEqual(so2.order_line.agent_ids.amount, self.com_item_2_amount)

        so3 = self._create_sale_order(self.product, self.partner_no_type)
        so3.recompute_lines_agents()
        self.assertEqual(so3.order_line.agent_ids.amount, self.com_item_1_amount)

    def test_invoice(self):
        in1 = self._create_account_invoice(self.product, self.partner_b2c)
        in1.recompute_lines_agents()
        self.assertEqual(in1.invoice_line_ids.agent_ids.amount, self.com_item_4_amount)

        in2 = self._create_account_invoice(self.product, self.partner_b2b)
        in2.recompute_lines_agents()
        self.assertEqual(in2.invoice_line_ids.agent_ids.amount, self.com_item_2_amount)

        in3 = self._create_account_invoice(self.product, self.partner_no_type)
        in3.recompute_lines_agents()
        self.assertEqual(in3.invoice_line_ids.agent_ids.amount, self.com_item_1_amount)

    def test_commission_order(self):
        # Test that commissions with fiscal position types are applied before
        in1 = self._create_account_invoice(self.product_2, self.partner_b2b)
        in1.recompute_lines_agents()
        self.assertEqual(in1.invoice_line_ids.agent_ids.amount, self.com_item_6_amount)
