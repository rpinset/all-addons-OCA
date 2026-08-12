# Copyright 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestStockQuantManualAssign(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env["product.product"].create(
            {"name": "Product 4 test", "type": "consu", "is_storable": True}
        )
        cls.location_src = cls.env.ref("stock.stock_location_locations_virtual")
        cls.location_dst = cls.env.ref("stock.stock_location_customers")
        cls.picking_type_out = cls.env["ir.model.data"]._xmlid_to_res_id(
            "stock.picking_type_out"
        )
        cls.env["stock.picking.type"].browse(
            cls.picking_type_out
        ).reservation_method = "manual"
        cls.location1 = cls._create_location("Location 1")
        cls.location2 = cls._create_location("Location 2")
        cls.location3 = cls._create_location("Location 3")
        cls.picking_type = cls.env.ref("stock.picking_type_out")
        cls.quant1 = cls._create_quant(cls.product, 100.0, cls.location1)
        cls.quant2 = cls._create_quant(cls.product, 100.0, cls.location2)
        cls.quant3 = cls._create_quant(cls.product, 100.0, cls.location3)
        cls.move = cls.env["stock.move"].create(
            {
                "name": cls.product.name,
                "product_id": cls.product.id,
                "product_uom_qty": 400.0,
                "product_uom": cls.product.uom_id.id,
                "location_id": cls.location_src.id,
                "location_dest_id": cls.location_dst.id,
                "picking_type_id": cls.picking_type.id,
            }
        )
        cls.move._action_confirm()

    @classmethod
    def _create_location(cls, name):
        return cls.env["stock.location"].create(
            {"name": name, "usage": "internal", "location_id": cls.location_src.id}
        )

    @classmethod
    def _create_quant(cls, product, qty, location):
        return (
            cls.env["stock.quant"]
            .sudo()
            .create(
                {"product_id": product.id, "quantity": qty, "location_id": location.id}
            )
        )

    @classmethod
    def _create_wizard(cls):
        return (
            cls.env["assign.manual.quants"]
            .with_context(active_id=cls.move.id)
            .create({})
        )

    @classmethod
    def _process_basic_manual_assign_steps(cls, wizard):
        wizard.quants_lines[0].write({"selected": True})
        wizard.quants_lines[0]._onchange_selected()
        wizard.quants_lines[1].write({"selected": True, "qty": 50.0})

    def test_quant_assign_wizard(self):
        wizard = self._create_wizard()
        self.assertEqual(
            len(wizard.quants_lines.ids),
            3,
            "Three quants created, three quants got by default",
        )
        self.assertEqual(
            len(wizard.quants_lines.filtered("selected").ids),
            0,
            "None of the quants must have been selected",
        )
        self.assertEqual(wizard.lines_qty, 0.0, "None selected must give 0")
        self.assertEqual(
            sum(line.qty for line in wizard.quants_lines),
            self.move.quantity,
        )
        self.assertEqual(wizard.move_qty, self.move.product_uom_qty)

    def test_quant_assign_wizard_constraint(self):
        wizard = self._create_wizard()
        self.assertEqual(
            len(wizard.quants_lines.ids),
            3,
            "Three quants created, three quants got by default",
        )
        self.assertEqual(
            len(wizard.quants_lines.filtered("selected").ids),
            0,
            "None of the quants must have been selected",
        )
        self.assertEqual(wizard.lines_qty, 0.0, "None selected must give 0")
        with self.assertRaises(ValidationError):
            wizard.write(
                {
                    "quants_lines": [
                        (1, wizard.quants_lines[:1].id, {"selected": True, "qty": 500})
                    ]
                }
            )

    def test_quant_manual_assign(self):
        wizard = self._create_wizard()
        self.assertEqual(
            len(wizard.quants_lines.ids),
            3,
            "Three quants created, three quants got by default",
        )
        self._process_basic_manual_assign_steps(wizard)
        self.assertEqual(wizard.lines_qty, 150.0)
        self.assertEqual(wizard.move_qty, 250.0)
        wizard.assign_quants()
        self.assertAlmostEqual(
            len(self.move.move_line_ids),
            2,
            "There are 2 quants selected",
        )
        self.assertEqual(sum(self.move.move_line_ids.mapped("quantity")), 150.0)

    def test_quant_assign_wizard_after_availability_check(self):
        self.move._action_assign()
        wizard = self._create_wizard()
        self.assertEqual(
            len(wizard.quants_lines.ids),
            3,
            "Three quants created, three quants got by default",
        )
        self.assertEqual(
            len(wizard.quants_lines.filtered("selected").ids),
            3,
            "All the quants must have been selected",
        )
        self.assertEqual(wizard.lines_qty, 300.0)
        self.assertEqual(wizard.move_qty, 100.0)
        self.assertEqual(
            len(wizard.quants_lines.filtered("selected")), len(self.move.move_line_ids)
        )
        self.assertEqual(
            sum(line.qty for line in wizard.quants_lines),
            self.move.quantity,
        )

    def test_quant_assign_get_discrepancies(self):
        self.move._action_assign()
        # There should be no move lines to unlink and no quant lines to assign
        # if there is no discrepancy between move lines and quant lines
        wizard = self._create_wizard()
        self.assertEqual(
            len(wizard.quants_lines.ids),
            3,
            "Three quants created, three quants got by default",
        )
        move_lines_to_unlink, quant_lines_to_assign = wizard._get_discrepancies()
        self.assertFalse(move_lines_to_unlink)
        self.assertFalse(quant_lines_to_assign)
        # There should be a move line to unlink
        # and a quant line to assisgn (due to qty discrepancy)
        wizard.quants_lines[2].write({"selected": True, "qty": 50.0})
        move_lines_to_unlink, quant_lines_to_assign = wizard._get_discrepancies()
        self.assertEqual(move_lines_to_unlink, self.move.move_line_ids[2])
        self.assertEqual(quant_lines_to_assign, wizard.quants_lines[2])
