# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    qty_done_total = fields.Float(
        compute="_compute_qty_progress",
        string="Done",
        store=False,
    )
    qty_remaining = fields.Float(
        compute="_compute_qty_progress",
        string="Remaining Quantity",
        store=False,
    )
    is_fully_picked = fields.Boolean(
        compute="_compute_qty_progress",
        string="Fully Picked",
        store=False,
    )

    def _reset_qty_progress(self):
        for move in self:
            move.qty_done_total = 0
            move.qty_remaining = 0
            move.is_fully_picked = False

    @api.depends("move_line_ids.qty_picked", "picking_id.state")
    def _compute_qty_progress(self):
        if self.env.context.get("install_mode"):
            self._reset_qty_progress()
            return
        ready_moves = self.filtered(lambda m: m.picking_id.state == "assigned")
        if not ready_moves:
            self._reset_qty_progress()
            return
        data = self.env["stock.move.line"]._read_group(
            [("move_id", "in", ready_moves.ids)],
            ["move_id"],
            ["qty_picked:sum"],
        )
        sums = {move.id: qty_picked for move, qty_picked in data}
        for move in self:
            done = sums.get(move.id, 0.0)
            move.qty_done_total = done
            move.qty_remaining = move.product_uom_qty - done
            move.is_fully_picked = move.qty_remaining <= 0
