# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestStockRepairOrder(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.repair_model = cls.env["repair.order"]
        cls.repair_line_model = cls.env["stock.move"]
        cls.product_model = cls.env["product.product"]
        cls.stock_location_model = cls.env["stock.location"]
        cls.warehouse_model = cls.env["stock.warehouse"]
        cls.company = cls.env.ref("base.main_company")
        cls.warehouse = cls.warehouse_model.create(
            {
                "name": "Test Warehouse",
                "code": "TW",
                "company_id": cls.company.id,
            }
        )

        cls.product1 = cls.product_model.create(
            {
                "name": "Product 1",
                "type": "product",
                "company_id": cls.company.id,
            }
        )
        cls.product2 = cls.product_model.create(
            {
                "name": "Product 2",
                "type": "product",
                "company_id": cls.company.id,
            }
        )
        cls.repair_location = cls.stock_location_model.create(
            {
                "name": "Repair Location",
                "usage": "internal",
                "location_id": cls.warehouse.view_location_id.id,
                "company_id": cls.company.id,
            }
        )
        cls.production_location = cls.stock_location_model.create(
            {
                "name": "Production Location",
                "usage": "production",
                "company_id": cls.company.id,
            }
        )
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product1.id,
                "location_id": cls.repair_location.id,
                "quantity": 10,
            }
        )
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product2.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "quantity": 10,
            }
        )

    def _crate_repair_order(self):
        return self.repair_model.create(
            {
                "product_id": self.product1.id,
                "product_uom": self.product1.uom_id.id,
                "location_id": self.repair_location.id,
                "company_id": self.company.id,
                "picking_type_id": self.warehouse.repair_type_id.id,
            }
        )

    def test_1step_repair_order_flow(self):
        self.warehouse.write(
            {
                "repair_steps": "1_step",
                "repair_location_id": self.repair_location.id,
            }
        )
        repair_order = self._crate_repair_order()
        self.repair_line_model.create(
            {
                "name": "Repair Line 1",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "add",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.repair_location.id,
                "location_dest_id": self.production_location.id,
            }
        )
        repair_order._action_repair_confirm()
        self.assertEqual(repair_order.state, "confirmed")

    def test_2steps_repair_order_flow(self):
        self.warehouse.write(
            {
                "repair_steps": "2_steps",
                "repair_location_id": self.repair_location.id,
            }
        )
        self.product2.write(
            {"route_ids": [(6, 0, [self.warehouse.repair_route_id.id])]}
        )
        repair_order = self._crate_repair_order()
        self.repair_line_model.create(
            {
                "name": "Repair Line 2",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "add",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.repair_location.id,
                "location_dest_id": self.production_location.id,
            }
        )
        repair_order._action_repair_confirm()
        repair_order._compute_picking_ids()
        self.assertEqual(repair_order.state, "confirmed")
        pick = repair_order.picking_ids
        self.assertEqual(len(pick), 1)
        self.assertEqual(pick.picking_type_id, self.warehouse.add_c_type_id)

    def test_3steps_repair_order_flow(self):
        self.warehouse.write(
            {
                "repair_steps": "3_steps",
                "repair_location_id": self.repair_location.id,
            }
        )
        self.product2.write(
            {"route_ids": [(6, 0, [self.warehouse.repair_route_id.id])]}
        )
        repair_order = self._crate_repair_order()
        self.repair_line_model.create(
            {
                "name": "Repair Line 3",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "add",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.repair_location.id,
                "location_dest_id": self.production_location.id,
            }
        )
        self.repair_line_model.create(
            {
                "name": "Repair Line 4",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "recycle",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.production_location.id,
                "location_dest_id": self.repair_location.id,
            }
        )
        repair_order._action_repair_confirm()
        repair_order._compute_picking_ids()
        self.assertEqual(repair_order.state, "confirmed")
        pickings = repair_order.picking_ids
        self.assertEqual(len(pickings), 2)
        pick = pickings.filtered(
            lambda p: p.picking_type_id == self.warehouse.add_c_type_id
        )
        self.assertTrue(pick)
        self.assertEqual(len(pick.move_ids.move_dest_ids), 1)
        self.assertEqual(pick.state, "assigned")
        self.assertEqual(pick.move_ids.move_dest_ids.repair_id, repair_order)
        recycle = pickings.filtered(
            lambda p: p.picking_type_id == self.warehouse.recycle_c_type_id
        )
        self.assertTrue(recycle)
        self.assertEqual(len(recycle.move_ids.move_orig_ids), 1)
        self.assertEqual(recycle.state, "waiting")
        self.assertEqual(recycle.move_ids.move_orig_ids.repair_id, repair_order)
        repair_order.action_repair_cancel()
        self.assertEqual(repair_order.state, "cancel")
        for picking in repair_order.picking_ids:
            self.assertEqual(picking.state, "cancel")

    def test_update_related_pickings(self):
        self.warehouse.write(
            {
                "repair_steps": "3_steps",
                "repair_location_id": self.repair_location.id,
            }
        )
        self.product2.write(
            {"route_ids": [(6, 0, [self.warehouse.repair_route_id.id])]}
        )
        repair_order = self._crate_repair_order()
        self.repair_line_model.create(
            {
                "name": "Repair Line 3",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "add",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.repair_location.id,
                "location_dest_id": self.production_location.id,
            }
        )
        repair_order._action_repair_confirm()
        repair_order._compute_picking_ids()
        self.assertEqual(repair_order.state, "confirmed")
        self.assertTrue(repair_order.picking_ids)
        self.assertEqual(len(repair_order.picking_ids), 1)
        self.assertEqual(len(repair_order.picking_ids.move_ids_without_package), 1)
        self.assertEqual(
            repair_order.picking_ids.move_ids_without_package.product_uom_qty, 1
        )
        self.repair_line_model.create(
            {
                "name": "Repair Line Add",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "add",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.repair_location.id,
                "location_dest_id": self.production_location.id,
            }
        )
        self.assertEqual(len(repair_order.picking_ids), 1)
        self.assertEqual(len(repair_order.picking_ids.move_ids_without_package), 1)
        self.assertEqual(
            repair_order.picking_ids.move_ids_without_package.product_uom_qty, 2
        )
        self.repair_line_model.create(
            {
                "name": "Repair Line Recycle",
                "repair_id": repair_order.id,
                "product_id": self.product2.id,
                "repair_line_type": "recycle",
                "product_uom_qty": 1,
                "product_uom": self.product2.uom_id.id,
                "price_unit": 1,
                "location_id": self.production_location.id,
                "location_dest_id": self.repair_location.id,
            }
        )
        repair_order._compute_picking_ids()
        self.assertEqual(len(repair_order.picking_ids), 2)
