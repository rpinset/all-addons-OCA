# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.sale_order_blanket_order_stock_prebook_release.hooks import (
    post_init_hook,
)

from .common import SaleOrderBlanketOrderStockPrebookReleaseCase


class TestPostInitHook(SaleOrderBlanketOrderStockPrebookReleaseCase):
    def test_hook_skips_draft_and_sets_priority_for_confirmed(self):
        """post_init_hook must compute blanket_move_date_priority only for confirmed
        blanket orders (sale/done state) and propagate it to their moves."""
        # Draft order must be skipped
        self.assertFalse(self.blanket_so.blanket_move_date_priority)
        post_init_hook(self.env.cr, self.env.registry)
        self.assertFalse(self.blanket_so.blanket_move_date_priority)

        # Confirm the order and reset priority to simulate pre-hook state
        self.blanket_so.action_confirm()
        self.blanket_so.write({"blanket_move_date_priority": False})
        non_final_moves = self.blanket_so.order_line.move_ids.filtered(
            lambda m: m.state not in ("done", "cancel", "assigned")
        )
        non_final_moves.write({"date_priority": False})

        post_init_hook(self.env.cr, self.env.registry)

        expected = self.blanket_so.blanket_move_date_priority
        self.assertTrue(expected)
        for move in non_final_moves:
            self.assertEqual(move.date_priority, expected)
