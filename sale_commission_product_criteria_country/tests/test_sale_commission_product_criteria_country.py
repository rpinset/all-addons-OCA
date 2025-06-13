# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleCommissionProductCriteriaCountry(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.agent = cls.env.ref("sale_commission_product_criteria.demo_agent_rules")
        cls.spain = cls.env.ref("base.es")
        cls.france = cls.env.ref("base.fr")
        cls.partner_spain = cls.env["res.partner"].create(
            {
                "name": "Test Spain",
                "country_id": cls.spain.id,
                "agent_ids": [(4, cls.agent.id)],
            }
        )
        cls.partner_france = cls.env["res.partner"].create(
            {
                "name": "Test France",
                "country_id": cls.france.id,
                "agent_ids": [(4, cls.agent.id)],
            }
        )
        cls.partner_no_country = cls.env["res.partner"].create(
            {
                "name": "Test B2B",
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
        cls.com_item_1.country_id = False
        cls.com_item_1_amount = 10
        cls.com_item_2 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_2"
        )
        cls.com_item_2.country_id = cls.france.id
        cls.com_item_2_amount = 20
        cls.com_item_3 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_3"
        )
        cls.com_item_3.country_id = cls.spain.id
        cls.com_item_4 = cls.env.ref(
            "sale_commission_product_criteria.demo_commission_rules_item_4"
        )
        cls.com_item_4.country_id = cls.spain.id
        cls.com_item_4_amount = 150
        cls.com_item_5_amount = 5
        cls.com_item_5 = cls.env["commission.item"].create(
            {
                "commission_id": cls.commission.id,
                "applied_on": "0_product_variant",
                "commission_type": "fixed",
                "fixed_amount": cls.com_item_5_amount,
                "product_id": cls.product_2.id,
                "country_id": False,
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
                "country_id": cls.france.id,
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
        so1 = self._create_sale_order(self.product, self.partner_spain)
        so1.recompute_lines_agents()
        self.assertEqual(so1.order_line.agent_ids.amount, self.com_item_4_amount)

        so2 = self._create_sale_order(self.product, self.partner_france)
        so2.recompute_lines_agents()
        self.assertEqual(so2.order_line.agent_ids.amount, self.com_item_2_amount)

        so3 = self._create_sale_order(self.product, self.partner_no_country)
        so3.recompute_lines_agents()
        self.assertEqual(so3.order_line.agent_ids.amount, self.com_item_1_amount)

    def test_invoice(self):
        in1 = self._create_account_invoice(self.product, self.partner_spain)
        in1.recompute_lines_agents()
        self.assertEqual(in1.invoice_line_ids.agent_ids.amount, self.com_item_4_amount)

        in2 = self._create_account_invoice(self.product, self.partner_france)
        in2.recompute_lines_agents()
        self.assertEqual(in2.invoice_line_ids.agent_ids.amount, self.com_item_2_amount)

        in3 = self._create_account_invoice(self.product, self.partner_no_country)
        in3.recompute_lines_agents()
        self.assertEqual(in3.invoice_line_ids.agent_ids.amount, self.com_item_1_amount)

    def test_commission_order(self):
        # Test that commissions with countries are applied before
        in1 = self._create_account_invoice(self.product_2, self.partner_france)
        in1.recompute_lines_agents()
        self.assertEqual(in1.invoice_line_ids.agent_ids.amount, self.com_item_6_amount)
