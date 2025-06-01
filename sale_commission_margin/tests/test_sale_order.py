# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].create(
            {
                "name": "Product",
                "detailed_type": "consu",
                "list_price": 100,
                "standard_price": 50,
            }
        )

        self.commission = self.env["commission"].create(
            {
                "name": "10% Commission",
                "commission_type": "fixed",
                "amount_base_type": "gross_amount",
                "invoice_state": "open",
                "fix_qty": 10,
            }
        )

        self.agent = self.env["res.partner"].create(
            {
                "name": "Agent",
                "agent": True,
                "agent_type": "agent",
                "commission_id": self.commission.id,
                "settlement": "monthly",
            }
        )

    def test_sale_order_with_commission(self):
        """
        Data:
            Price: 100
            Cost: 50
            Commission: 10%

        Result:
            Sale Order Total: 100
            Sale Order Commission: 10
            Sale Order Margin: 40"""

        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_2").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                        },
                    )
                ],
            }
        )
        sale_agent = self.env["sale.order.line.agent"].create(
            {
                "object_id": sale_order.order_line[0].id,
                "commission_id": self.commission.id,
                "agent_id": self.agent.id,
            }
        )
        sale_order.order_line[0].agent_ids = [(4, sale_agent.id)]

        self.assertEqual(sale_order.amount_untaxed, 100.0)
        self.assertEqual(sale_order.commission_total, 10.0)
        self.assertEqual(sale_order.margin, 40.0)
        self.assertEqual(sale_order.margin_percent, 0.4)
