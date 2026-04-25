# Copyright 2023 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from .test_checkout_base import CheckoutCommonCase


class CheckoutAutoPostCase(CheckoutCommonCase):
    def test_auto_posting(self):
        self.menu.sudo().auto_post_line = True
        picking = self._create_picking(
            lines=[(self.product_a, 10), (self.product_b, 20), (self.product_c, 30)]
        )
        self._fill_stock_for_moves(picking.move_ids)
        picking.action_assign()
        selected_move_line_a = picking.move_line_ids.filtered(
            lambda x: x.product_id == self.product_a
        )
        selected_move_line_a.qty_picked = 7
        selected_move_line_b = picking.move_line_ids.filtered(
            lambda x: x.product_id == self.product_b
        )
        selected_move_line_b.qty_picked = 9
        selected_move_line_c = picking.move_line_ids.filtered(
            lambda x: x.product_id == self.product_c
        )

        # User has selected 7 units out of 10 for product_a,
        # and 9 units out of 20 for product_b.
        # We would expect a split picking to be created
        # with those two lines and qtys done.
        self.service.dispatch(
            "scan_package_action",
            params={
                "picking_id": picking.id,
                "selected_line_ids": [selected_move_line_a.id, selected_move_line_b.id],
                "barcode": self.package_type.barcode,
            },
        )

        # Check that two new lines for products a and b are in a split picking,
        # and the line for product c remained in the original picking.
        self.assertNotEqual(picking, selected_move_line_a.picking_id)
        self.assertEqual(
            selected_move_line_a.picking_id, selected_move_line_b.picking_id
        )
        self.assertEqual(picking, selected_move_line_c.picking_id)

        # The lines in the new picking must have the expected picked qty,
        # and the split picking must be marked as "done".
        self.assertEqual(selected_move_line_a.qty_picked, 7)
        self.assertEqual(selected_move_line_b.qty_picked, 9)
        self.assertEqual(selected_move_line_a.picking_id.state, "done")

        # In the original picking, we should have three lines:
        # - the original line for product c, unchanged;
        # - two lines (products a and b) with the non-split qtys.
        line_a_in_original_picking = picking.move_line_ids.filtered(
            lambda x: x.product_id == selected_move_line_a.product_id
        )
        line_b_in_original_picking = picking.move_line_ids.filtered(
            lambda x: x.product_id == selected_move_line_b.product_id
        )
        self.assertEqual(line_a_in_original_picking.quantity, 3)
        self.assertEqual(line_b_in_original_picking.quantity, 11)
        self.assertEqual(selected_move_line_c.quantity, 30)

        self.assertEqual(line_a_in_original_picking.qty_picked, 0)
        self.assertEqual(line_b_in_original_picking.qty_picked, 0)
        self.assertEqual(selected_move_line_c.qty_picked, 0)
        self.assertFalse(selected_move_line_c.picked)
