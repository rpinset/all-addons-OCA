# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestMrpSubcontractingStockOwnerRestriction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.manufacture_route = cls.env.ref("mrp.route_warehouse0_manufacture")
        cls.owner = cls.env["res.partner"].create({"name": "Test Owner"})
        cls.finished_product = cls.env["product.product"].create(
            {"name": "test product", "type": "product"}
        )
        cls.component = cls.env["product.product"].create(
            {"name": "test component", "type": "product"}
        )
        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_id": cls.finished_product.id,
                "product_tmpl_id": cls.finished_product.product_tmpl_id.id,
                "product_uom_id": cls.finished_product.uom_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        cls.picking_type = cls.env["stock.picking.type"].search(
            [
                ("code", "=", "mrp_operation"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )
        cls.env["mrp.bom.line"].create(
            {"bom_id": cls.bom.id, "product_id": cls.component.id, "product_qty": 1}
        )
        cls.finished_product.route_ids = [Command.set(cls.manufacture_route.ids)]
        quant_vals = {
            "product_id": cls.component.id,
            "location_id": cls.picking_type.default_location_src_id.id,
            "quantity": 10.00,
        }
        cls.env["stock.quant"].create(quant_vals)
        cls.mo = cls.env["mrp.production"].create(
            {
                "product_id": cls.finished_product.id,
                "bom_id": cls.bom.id,
                "product_qty": 1,
            }
        )
        cls.mo.action_confirm()

    def test_mrp_stock_owner_restriction_change_owner(self):
        self.picking_type.owner_restriction = "standard_behavior"
        self.assertTrue(self.mo.move_line_raw_ids)
        self.mo.owner_id = self.owner
        self.assertTrue(self.mo.move_line_raw_ids)
        self.mo.owner_id = False
        self.picking_type.owner_restriction = "picking_partner"
        self.mo.owner_id = self.owner
        self.assertFalse(self.mo.move_line_raw_ids)
