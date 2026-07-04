# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.route_planning.tests.common import RouteCommon


class TestRoutePlanningSaleStock(RouteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.area_north.warehouse_id = cls.warehouse
        cls.area_south.warehouse_id = cls.warehouse
        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "is_storable": True}
        )
        # Create quants for products to ensure stock availability
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product_a.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "quantity": 10.0,
            }
        )
        # Create sale order
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner_1
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product_a
        cls.order = order_form.save()

    def test_sale_order_with_route_area(self):
        self.order.action_confirm()
        self.assertEqual(self.order.state, "sale")
        picking = self.order.picking_ids
        self.assertEqual(picking.route_area_id, self.area_north)
        self.assertEqual(picking.location_dest_id, self.area_north.location_id)
        picking.button_validate()
        self.assertEqual(picking.state, "done")
        next_picking = picking._get_next_transfers()
        self.assertTrue(next_picking)
        self.assertEqual(next_picking.route_area_id, self.area_north)
        self.assertEqual(next_picking.location_id, self.area_north.location_id)
        checkpoint = self.env["route.checkpoint"].search(
            [("picking_id", "=", next_picking.id)]
        )
        checkpoint.route_id.action_planned()
        checkpoint.action_done()
        self.assertEqual(next_picking.state, "done")
        self.assertEqual(checkpoint.state, "done")

    def test_sale_order_without_route_area(self):
        self.partner_1.route_area_id = False
        self.order.route_area_id = False
        self.order.action_confirm()
        self.assertEqual(self.order.state, "sale")
        picking = self.order.picking_ids
        self.assertFalse(picking.route_area_id)
        self.assertNotEqual(picking.location_dest_id, self.area_north.location_id)
        picking.button_validate()
        self.assertEqual(picking.state, "done")
        next_picking = picking._get_next_transfers()
        self.assertFalse(next_picking)
