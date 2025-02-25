# Copyright 2022-23 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields
from odoo.tests.common import TransactionCase


class TestComponentOperation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env = api.Environment(cls.cr, cls.user_admin.id, {})
        cls.ProcurementGroup = cls.env["procurement.group"]
        cls.MrpProduction = cls.env["mrp.production"]
        cls.env.user.company_id.manufacturing_lead = 0

        cls.picking_type = cls.env["stock.picking.type"].search(
            [
                ("code", "=", "mrp_operation"),
                ("sequence_id.company_id", "=", cls.env.user.company_id.id),
            ],
            limit=1,
        )
        cls.product1 = cls.env["product.product"].create(
            {
                "name": "TEST Parent",
                "route_ids": [
                    (6, 0, [cls.env.ref("mrp.route_warehouse0_manufacture").id])
                ],
                "type": "product",
            }
        )
        cls.product2 = cls.env["product.product"].create(
            {"name": "TEST Child", "type": "product"}
        )
        cls.product3 = cls.env["product.product"].create(
            {"name": "TEST Child Serial", "type": "product", "tracking": "serial"}
        )
        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_id": cls.product1.id,
                "product_tmpl_id": cls.product1.product_tmpl_id.id,
                "produce_delay": 0,
                "type": "normal",
                "bom_line_ids": [
                    (0, 0, {"product_id": cls.product2.id, "product_qty": 2}),
                    (0, 0, {"product_id": cls.product3.id, "product_qty": 1}),
                ],
            }
        )
        cls.stock_picking_type = cls.env.ref("stock.picking_type_out")
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.user.company_id.id)], limit=1
        )
        cls.warehouse.manufacture_steps = "pbm"
        cls.ressuply_loc1 = cls.warehouse.lot_stock_id
        cls.manufacture_location = cls.warehouse.pbm_loc_id
        cls.destination_location = cls.env.ref("stock.stock_location_output")
        stock_location_locations_virtual = cls.env["stock.location"].create(
            {"name": "Virtual Locations", "usage": "view", "posz": 1}
        )
        cls.scrapped_location = cls.env["stock.location"].create(
            {
                "name": "Scrapped",
                "location_id": stock_location_locations_virtual.id,
                "scrap_location": True,
                "usage": "inventory",
            }
        )
        cls.source_route = cls.env["stock.route"].create(
            {
                "name": "Source Route",
                "mo_component_selectable": True,
                "sequence": 10,
            }
        )

        cls.destination_route = cls.env["stock.route"].create(
            {
                "name": "Destination Route",
                "mo_component_selectable": True,
                "sequence": 10,
            }
        )

        cls.env["stock.rule"].create(
            {
                "name": "Transfer",
                "route_id": cls.source_route.id,
                "location_src_id": cls.ressuply_loc1.id,
                "location_dest_id": cls.manufacture_location.id,
                "action": "pull",
                "picking_type_id": cls.warehouse.int_type_id.id,
                "procure_method": "make_to_stock",
                "warehouse_id": cls.warehouse.id,
            }
        )

        cls.env["stock.rule"].create(
            {
                "name": "Transfer 2",
                "route_id": cls.destination_route.id,
                "location_src_id": cls.manufacture_location.id,
                "location_dest_id": cls.destination_location.id,
                "action": "pull",
                "picking_type_id": cls.warehouse.int_type_id.id,
                "procure_method": "make_to_stock",
                "warehouse_id": cls.warehouse.id,
                "propagate_warehouse_id": cls.warehouse.id,
            }
        )

        cls.operation_scrap_replace = cls.env["mrp.component.operation"].create(
            {
                "name": "Operation Scrap and Replace",
                "incoming_operation": "replace",
                "outgoing_operation": "scrap",
                "manufacture_location_id": cls.manufacture_location.id,
                "source_route_id": cls.source_route.id,
                "scrap_location_id": cls.scrapped_location.id,
            }
        )

        cls.operation_no = cls.env["mrp.component.operation"].create(
            {
                "name": "Operation Scrap and Replace",
                "incoming_operation": "no",
                "outgoing_operation": "no",
                "manufacture_location_id": cls.manufacture_location.id,
            }
        )

        cls.operation_move_replace = cls.env["mrp.component.operation"].create(
            {
                "name": "Operation Move",
                "incoming_operation": "replace",
                "outgoing_operation": "move",
                "manufacture_location_id": cls.manufacture_location.id,
                "source_route_id": cls.source_route.id,
                "destination_location_id": cls.destination_location.id,
                "destination_route_id": cls.destination_route.id,
            }
        )

    @classmethod
    def _do_picking(cls, picking):
        picking.action_assign()
        date = fields.Datetime.now()
        picking.action_confirm()
        picking.move_ids.picked = True
        picking._action_done()
        for move in picking.move_ids:
            move.date = date

    def test_01_scrap_and_replace(self):
        nb_product_todo = 5
        serials_p2 = []
        for i in range(nb_product_todo):
            serials_p2.append(
                self.env["stock.lot"].create(
                    {
                        "name": f"lot_consumed_2_{i}",
                        "product_id": self.product3.id,
                        "company_id": self.env.company.id,
                    }
                )
            )
            self.env["stock.quant"]._update_available_quantity(
                self.product3, self.ressuply_loc1, 1, lot_id=serials_p2[-1]
            )
        self.env["stock.quant"]._update_available_quantity(
            self.product2, self.ressuply_loc1, 10
        )
        mo = self.MrpProduction.create(
            {
                "bom_id": self.bom.id,
                "product_id": self.product1.id,
                "product_qty": 2,
                "product_uom_id": self.product1.uom_id.id,
                "date_deadline": "2023-01-01 15:00:00",
                "date_start": "2023-01-01 15:00:00",
            }
        )
        mo.action_confirm()
        picking = mo.move_raw_ids.move_orig_ids.picking_id
        picking.move_ids.write({"picked": True})
        picking.button_validate()
        mo.action_assign()
        move_product_2 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product2
        )
        raw_move_product_3 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product3
        )
        self.assertEqual(move_product_2.move_line_ids.quantity_product_uom, 4)
        self.assertEqual(len(raw_move_product_3.move_line_ids), 2)
        lot = raw_move_product_3.move_line_ids[0].lot_id
        wizard = self.env["mrp.component.operate"].create(
            {
                "product_id": self.product3.id,
                "lot_id": lot.id,
                "operation_id": self.operation_scrap_replace.id,
                "mo_id": mo.id,
            }
        )
        self.assertEqual(wizard.product_qty, 1)
        old_pickings = mo.picking_ids
        wizard.action_operate_component()
        new_pickings = mo.picking_ids - old_pickings
        self.assertEqual(mo.scrap_ids.product_id, self.product3)
        self.assertEqual(mo.scrap_ids.lot_id, lot)
        self.assertEqual(mo.scrap_ids.state, "done")
        self.assertEqual(len(raw_move_product_3.move_line_ids), 1)
        self._do_picking(new_pickings)
        self.assertEqual(new_pickings.state, "done")
        self.assertEqual(
            len(raw_move_product_3.move_line_ids),
            2,
            "Two lines, the operated one and the other one. (2 units required)",
        )
        self.assertEqual(len(raw_move_product_3.move_orig_ids[-1].move_line_ids), 1)

    def test_02_move_and_replace(self):
        nb_product_todo = 5
        serials_p2 = []
        for i in range(nb_product_todo):
            serials_p2.append(
                self.env["stock.lot"].create(
                    {
                        "name": f"lot_consumed_2_{i}",
                        "product_id": self.product3.id,
                        "company_id": self.env.company.id,
                    }
                )
            )
            self.env["stock.quant"]._update_available_quantity(
                self.product3, self.ressuply_loc1, 1, lot_id=serials_p2[-1]
            )
        self.env["stock.quant"]._update_available_quantity(
            self.product2, self.ressuply_loc1, 10
        )
        mo = self.MrpProduction.create(
            {
                "bom_id": self.bom.id,
                "product_id": self.product1.id,
                "product_qty": 1,
                "product_uom_id": self.product1.uom_id.id,
                "date_deadline": "2023-01-01 15:00:00",
                "date_start": "2023-01-01 15:00:00",
            }
        )
        mo.action_confirm()
        picking = mo.move_raw_ids.move_orig_ids.picking_id
        picking.move_ids.write({"picked": True})
        picking.button_validate()
        mo.action_assign()
        self.assertEqual(len(mo.move_raw_ids), 2)
        move_product_2 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product2
        )
        raw_move_product_3 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product3
        )
        self.assertEqual(move_product_2.move_line_ids.quantity_product_uom, 2)
        self.assertEqual(len(raw_move_product_3.move_line_ids), 1)
        lot = raw_move_product_3.move_line_ids[0].lot_id
        wizard = self.env["mrp.component.operate"].create(
            {
                "product_id": self.product3.id,
                "lot_id": lot.id,
                "operation_id": self.operation_move_replace.id,
                "mo_id": mo.id,
            }
        )
        self.assertEqual(wizard.product_qty, 1)
        old_pickings = mo.picking_ids
        self.assertEqual(len(old_pickings), 1)
        wizard.action_operate_component()
        self.assertEqual(len(mo.picking_ids), 3)
        new_pickings = mo.picking_ids - old_pickings
        moves_for_replacement = new_pickings.mapped("move_ids")
        self.assertEqual(len(moves_for_replacement), 2)
        for move in moves_for_replacement:
            self.assertEqual(
                move.product_id,
                self.product3,
            )
        replacement_first_move = moves_for_replacement.filtered(
            lambda m: m.location_dest_id == self.destination_location
        )
        self.assertTrue(replacement_first_move)
        replacement_second_move = moves_for_replacement.filtered(
            lambda m: m.location_dest_id == self.manufacture_location
        )
        self.assertTrue(replacement_second_move)
        self.assertEqual(
            len(raw_move_product_3.move_line_ids),
            0,
            "Reservation for product3 should have been cleared",
        )
        self.assertEqual(raw_move_product_3.move_orig_ids[-1], replacement_second_move)
        self._do_picking(replacement_first_move.picking_id)
        self.assertEqual(replacement_first_move.state, "done")
        self.assertEqual(replacement_first_move.move_line_ids.lot_id, lot)
        self.assertEqual(
            len(raw_move_product_3.move_line_ids),
            0,
            "raw move for product 3 still not reserved.",
        )
        self._do_picking(replacement_second_move.picking_id)
        self.assertEqual(replacement_second_move.state, "done")
        self.assertEqual(replacement_first_move.product_id, self.product3)
        mo.action_assign()
        self.assertEqual(len(raw_move_product_3.move_line_ids), 1)

    def test_03_nothing_and_nothing(self):
        nb_product_todo = 5
        serials_p2 = []
        for i in range(nb_product_todo):
            serials_p2.append(
                self.env["stock.lot"].create(
                    {
                        "name": f"lot_consumed_2_{i}",
                        "product_id": self.product3.id,
                        "company_id": self.env.company.id,
                    }
                )
            )
            self.env["stock.quant"]._update_available_quantity(
                self.product3, self.ressuply_loc1, 1, lot_id=serials_p2[-1]
            )
        self.env["stock.quant"]._update_available_quantity(
            self.product2, self.ressuply_loc1, 10
        )
        mo = self.MrpProduction.create(
            {
                "bom_id": self.bom.id,
                "product_id": self.product1.id,
                "product_qty": 2,
                "product_uom_id": self.product1.uom_id.id,
                "date_deadline": "2023-01-01 15:00:00",
                "date_start": "2023-01-01 15:00:00",
            }
        )
        mo.action_confirm()
        picking = mo.move_raw_ids.move_orig_ids.picking_id
        picking.move_ids.write({"picked": True})
        picking.button_validate()
        mo.action_assign()
        move_product_2 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product2
        )
        raw_move_product_3 = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product3
        )
        self.assertEqual(move_product_2.move_line_ids.quantity_product_uom, 4)
        self.assertEqual(len(raw_move_product_3.move_line_ids), 2)
        wizard = self.env["mrp.component.operate"].create(
            {
                "product_id": self.product3.id,
                "lot_id": raw_move_product_3.move_line_ids[0].lot_id.id,
                "operation_id": self.operation_no.id,
                "mo_id": mo.id,
            }
        )
        self.assertEqual(wizard.product_qty, 1)
        self.assertEqual(wizard.product_id, self.product3)
        wizard.action_operate_component()
        self.assertEqual(move_product_2.move_line_ids.quantity_product_uom, 4)
        self.assertEqual(len(mo.move_raw_ids[1].move_line_ids), 2)
