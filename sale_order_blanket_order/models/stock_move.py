# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    call_off_sale_line_id = fields.Many2one(
        "sale.order.line", "Call Off Sale Line", index="btree_not_null"
    )

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super()._prepare_merge_moves_distinct_fields()
        distinct_fields.append("call_off_sale_line_id")
        return distinct_fields

    def _split_for_dest_moves(self, dest_moves):
        """Split the qty feeding the given destination moves into a new move.

        Return an empty recordset if the move cannot be split because its
        operation has started or its whole qty feeds the given destination moves.
        """
        self.ensure_one()
        if any(self.move_line_ids.mapped("picked")):
            return self.browse()
        vals_list = self._split(sum(dest_moves.mapped("product_qty")))
        if not vals_list:
            return self.browse()
        for vals in vals_list:
            vals["picking_id"] = False
            vals["move_dest_ids"] = [Command.set(dest_moves.ids)]
        new_move = self.create(vals_list)
        self.move_dest_ids = [Command.unlink(move.id) for move in dest_moves]
        # The qty of the move has been decreased without changing its reservation
        self._release_exceeding_reserved_qty()
        return new_move

    def _release_exceeding_reserved_qty(self):
        """Release reserved qty exceeding the move demand while keeping existing
        move line reservations.
        """
        self.ensure_one()
        uom = self.product_id.uom_id
        exceeding_qty = (
            sum(self.move_line_ids.mapped("quantity_product_uom")) - self.product_qty
        )
        for move_line in self.move_line_ids.sorted("id", reverse=True):
            if uom.compare(exceeding_qty, 0) <= 0:
                break
            if uom.compare(move_line.quantity_product_uom, exceeding_qty) <= 0:
                exceeding_qty -= move_line.quantity_product_uom
                move_line.unlink()
                continue
            move_line.quantity = uom._compute_quantity(
                move_line.quantity_product_uom - exceeding_qty,
                move_line.product_uom_id,
                rounding_method="HALF-UP",
            )
            exceeding_qty = 0
        self._recompute_state()
