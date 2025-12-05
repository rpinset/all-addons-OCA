# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestMrpSaleInfo(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        route_manufacture_1 = cls.env.ref("mrp.route_warehouse0_manufacture")
        route_manufacture_2 = cls.env.ref("stock.route_warehouse0_mto")
        route_manufacture_2.active = True
        cls.product = cls.env["product.product"].create(
            [
                {
                    "name": "Test mrp_sale_info product",
                    "type": "consu",
                    "route_ids": [
                        (4, route_manufacture_1.id),
                        (4, route_manufacture_2.id),
                    ],
                }
            ]
        )
        cls.product_to_use = cls.env["product.product"].create(
            {"name": "Material", "type": "consu"}
        )
        cls.bom = cls.env["mrp.bom"].create(
            [
                {
                    "product_tmpl_id": cls.product.product_tmpl_id.id,
                    "operation_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Test operation",
                                "workcenter_id": cls.env.ref("mrp.mrp_workcenter_3").id,
                            },
                        )
                    ],
                    "bom_line_ids": [
                        (
                            0,
                            0,
                            {"product_id": cls.product_to_use.id, "product_qty": 1.0},
                        ),
                    ],
                }
            ]
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test client"})
        cls.sale_order = cls.env["sale.order"].create(
            [
                {
                    "partner_id": cls.partner.id,
                    "client_order_ref": "SO1",
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": cls.product.id,
                                "product_uom_qty": 1,
                                "price_unit": 1,
                            },
                        ),
                    ],
                }
            ]
        )

    def test_mrp_sale_info(self):
        prev_productions = self.env["mrp.production"].search([])
        self.sale_order.action_confirm()
        production = self.env["mrp.production"].search([]) - prev_productions
        self.assertEqual(production.sale_id, self.sale_order)
        self.assertEqual(production.partner_id, self.partner)
        self.assertEqual(production.client_order_ref, self.sale_order.client_order_ref)
        self.assertEqual(production.sale_line_id, self.sale_order.order_line)

    def test_mrp_workorder(self):
        prev_workorders = self.env["mrp.workorder"].search([])
        self.sale_order.action_confirm()
        workorder = (
            self.env["mrp.production"].search([]).workorder_ids - prev_workorders
        )
        self.assertEqual(workorder.sale_id, self.sale_order)
        self.assertEqual(workorder.partner_id, self.partner)
        self.assertEqual(workorder.client_order_ref, self.sale_order.client_order_ref)

    def test_orderpoint(self):
        """Test if orderpoint MO generation still works well"""
        prev_productions = self.env["mrp.production"].search([])
        warehouse = self.env["stock.warehouse"].search([], limit=1)
        orderpoint = self.env["stock.warehouse.orderpoint"].create(
            {
                "name": "replenish product",
                "location_id": warehouse.lot_stock_id.id,
                "product_id": self.product.id,
                "product_min_qty": 10,
                "product_max_qty": 100,
            }
        )
        orderpoint._procure_orderpoint_confirm(
            company_id=orderpoint.company_id, raise_user_error=False
        )
        production = self.env["mrp.production"].search([]) - prev_productions
        self.assertEqual(len(production), 1)
