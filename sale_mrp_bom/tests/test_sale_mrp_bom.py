# Copyright 2020 Akretion Renato Lima <renato.lima@akretion.com.br>
# Copyright 2024 Binhex Rolando Pérez <r.perez@binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from .common import TestSaleMrpBomCommon


class TestSaleMrpLink(TestSaleMrpBomCommon):
    def prepare_boms(self):
        # Create BOMs
        bom_a_v1 = self.create_bom(self.product_a.product_tmpl_id)
        self.create_bom_line(bom_a_v1, self.component_a, 1)
        bom_a_v2 = self.create_bom(self.product_a.product_tmpl_id)
        self.create_bom_line(bom_a_v2, self.component_a, 2)

        bom_b_v1 = self.create_bom(self.product_b.product_tmpl_id)
        self.create_bom_line(bom_b_v1, self.component_b, 1)
        bom_b_v2 = self.create_bom(self.product_b.product_tmpl_id)
        self.create_bom_line(bom_b_v2, self.component_b, 2)

        bom_a, bom_b = bom_a_v2, bom_b_v2
        self.boms = {
            self.product_a.id: bom_a,
            self.product_b.id: bom_b,
        }
        return bom_a, bom_b

    def prepare_so(self):
        bom_a_v2, bom_b_v2 = self.prepare_boms()

        # Create Sale Order
        so = self.create_sale_order("SO1")
        self.create_sale_order_line(so, self.product_a, 1, 10.0, bom_a_v2)
        self.create_sale_order_line(so, self.product_b, 1, 10.0, bom_b_v2)
        so.action_confirm()
        return so, bom_a_v2, bom_b_v2

    def test_define_bom_in_sale_line(self):
        """Check manufactured order is created with BOM defined in Sale."""
        so, bom_a, bom_b = self.prepare_so()

        # Check manufacture order
        mos = self.env["mrp.production"].search([("origin", "=", so.name)])
        for mo in mos:
            self.assertEqual(mo.bom_id, self.boms.get(mo.product_id.id))

    def test_pick_a_pack_confirm(self):
        so, bom_a, bom_b = self.prepare_so()
        picking, boms = so.picking_ids[0], (bom_a, bom_b)

        for i, line in enumerate(picking.move_lines):
            values = line._prepare_procurement_values()
            self.assertEqual(values["bom_id"], boms[i])

    def test_mismatch_product_variant_ids(self):
        so, bom_a, bom_b = self.prepare_so()
        line_a = so.order_line[0]
        self.assertEqual(line_a.bom_id, bom_a)
        with self.assertRaises(ValidationError):
            line_a.bom_id = bom_b

    def test_accept_bom_with_no_variant(self):
        # make variants for template of product A
        product_tmpl_a = self.product_a.product_tmpl_id
        prod_attr_color = self.product_attr_color
        product_attr_val_red, product_attr_val_green = (
            self.product_attr_val_red,
            self.product_attr_val_green,
        )
        product_tmpl_a.attribute_line_ids = [
            (
                0,
                0,
                {
                    "attribute_id": prod_attr_color.id,
                    "value_ids": [
                        (6, 0, [product_attr_val_red.id, product_attr_val_green.id])
                    ],
                },
            )
        ]
        product_a = product_tmpl_a.product_variant_ids[0]
        bom_no_variant = self.create_bom(product_tmpl_a)
        so = self.create_sale_order("SO2")
        self.create_sale_order_line(so, product_a, 2, 25, bom_no_variant)
        line_a = so.order_line[0]
        line_a.bom_id = bom_no_variant
