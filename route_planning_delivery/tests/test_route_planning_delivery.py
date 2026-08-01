# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tools import mute_logger

from odoo.addons.route_planning.tests.common import RouteCommon


class TestRoutePlanningDelivery(RouteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Product = cls.env["product.product"]
        cls.warehouse = cls.env.ref("stock.warehouse0")
        # Archive all pricelists to avoid conflicts with the test
        cls.env["product.pricelist"].search([]).action_archive()
        cls.area_north.warehouse_id = cls.warehouse
        cls.area_south.warehouse_id = cls.warehouse
        cls.product_a = Product.create({"name": "Product A", "is_storable": True})
        carrier_product = Product.create(
            {
                "name": "Test shipping product",
                "type": "service",
                "list_price": 10.0,
                "taxes_id": [Command.clear()],
                "supplier_taxes_id": [Command.clear()],
            }
        )
        # Create quants for products to ensure stock availability
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product_a.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "quantity": 10.0,
            }
        )
        cls.carrier = cls.env["delivery.carrier"].create(
            {"name": "Test carrier", "product_id": carrier_product.id}
        )
        cls.carrier_route = cls.env["delivery.carrier"].create(
            {
                "name": "Test carrier route",
                "product_id": carrier_product.id,
                "delivery_type": "route_planning",
                "integration_level": "rate",
            }
        )
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner_1
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product_a
        cls.order = order_form.save()

    def _add_shipping_to_order(self, sale_order, carrier, route_area=None):
        action = sale_order.action_open_delivery_wizard()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        wizard_form.carrier_id = carrier
        if route_area:
            wizard_form.route_area_id = route_area
        wizard = wizard_form.save()
        wizard._get_delivery_rate()
        wizard.button_confirm()

    def test_delivery_carrier_constrains(self):
        # test onchange delivery_type to route_planning
        self.assertEqual(self.carrier.delivery_type, "fixed")
        self.carrier.integration_level = "rate_and_ship"
        with Form(self.carrier) as carrier_form:
            carrier_form.delivery_type = "route_planning"
        self.assertEqual(self.carrier.integration_level, "rate")
        # test constrains delivery_type to route_planning and invalid integration_level
        with self.assertRaisesRegex(
            ValidationError, r"please change the integration level to ' Get rate'"
        ):
            self.carrier_route.integration_level = "rate_and_ship"

    def test_sale_order_with_carrier_and_route_area(self):
        self._add_shipping_to_order(
            self.order, self.carrier_route, route_area=self.area_north
        )
        self.assertEqual(self.order.carrier_id, self.carrier_route)
        self.assertEqual(self.order.route_area_id, self.area_north)
        delivery_line = self.order.order_line.filtered("is_delivery")
        self.assertEqual(delivery_line.product_id, self.carrier_route.product_id)
        self.assertEqual(delivery_line.price_unit, 10)
        self.order.action_confirm()
        picking = self.order.picking_ids
        self.assertEqual(picking.route_area_id, self.area_north)
        self.assertEqual(picking.carrier_id, self.carrier_route)
        self.assertEqual(picking.location_dest_id, self.area_north.location_id)
        self.assertFalse(picking.has_route_planning)
        picking.button_validate()
        next_picking = picking._get_next_transfers()
        self.assertEqual(next_picking.route_area_id, self.area_north)
        self.assertEqual(next_picking.carrier_id, self.carrier_route)
        self.assertEqual(next_picking.location_id, self.area_north.location_id)
        self.assertTrue(next_picking.has_route_planning)
        next_picking.route_checkpoint_ids.route_id.action_planned()
        next_picking.button_validate()
        # test that the picking cannot be sent to shipper
        with self.assertRaisesRegex(ValidationError, r"cannot create shipments"):
            next_picking.send_to_shipper()

    def test_sale_order_choose_delivery_carrier_change(self):
        # asign the carrier and route area first
        # and remove the carrier later
        self._add_shipping_to_order(
            self.order, self.carrier_route, route_area=self.area_north
        )
        self.assertEqual(self.order.carrier_id, self.carrier_route)
        self.assertEqual(self.order.route_area_id, self.area_north)
        # remove delivery line
        delivery_line = self.order.order_line.filtered("is_delivery")
        delivery_line.unlink()
        self.assertFalse(self.order.carrier_id)
        self.assertFalse(self.order.route_area_id)
        # Set the carrier without route area, the route_area_id should be removed
        self._add_shipping_to_order(self.order, self.carrier)
        self.assertEqual(self.order.carrier_id, self.carrier)
        self.assertFalse(self.order.route_area_id)
        # Open wizard: auto-set route_area_id
        action = self.order.action_open_delivery_wizard()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        wizard_form.carrier_id = self.carrier_route
        self.assertEqual(wizard_form.route_area_id, self.area_north)
        wizard_form.carrier_id = self.carrier
        self.assertFalse(wizard_form.route_area_id)
        wizard = wizard_form.save()
        wizard.button_confirm()
        self.order.action_confirm()
        picking = self.order.picking_ids
        self.assertFalse(picking.route_area_id)
        self.assertNotEqual(picking.location_dest_id, self.area_north.location_id)
        self.assertFalse(picking.has_route_planning)
        picking.button_validate()
        next_picking = picking._get_next_transfers()
        self.assertFalse(next_picking)

    @mute_logger("odoo.models.unlink")
    def test_sale_order_confirm_choose_delivery_carrier(self):
        line_a = self.order.order_line
        self._add_shipping_to_order(
            self.order, self.carrier_route, route_area=self.area_north
        )
        self.assertEqual(self.order.carrier_id, self.carrier_route)
        self.assertEqual(self.order.route_area_id, self.area_north)
        self.order.action_confirm()
        move_a = line_a.move_ids
        picking = self.order.picking_ids
        self.assertEqual(picking.carrier_id, self.carrier_route)
        self.assertEqual(picking.route_area_id, self.area_north)
        self.assertEqual(move_a.location_dest_id, self.area_north.location_id)
        self.assertEqual(picking.location_dest_id, self.area_north.location_id)
        self.assertFalse(picking.has_route_planning)
        # Change carrier without route area
        self._add_shipping_to_order(self.order, self.carrier)
        self.assertEqual(picking.carrier_id, self.carrier)
        self.assertFalse(picking.route_area_id)
        self.assertNotEqual(move_a.location_dest_id, self.area_north.location_id)
        self.assertNotEqual(picking.location_dest_id, self.area_north.location_id)
        # Change carrier with route area
        self._add_shipping_to_order(
            self.order, self.carrier_route, route_area=self.area_north
        )
        self.assertEqual(picking.carrier_id, self.carrier_route)
        self.assertEqual(picking.route_area_id, self.area_north)
        self.assertEqual(move_a.location_dest_id, self.area_north.location_id)
        self.assertEqual(picking.location_dest_id, self.area_north.location_id)
