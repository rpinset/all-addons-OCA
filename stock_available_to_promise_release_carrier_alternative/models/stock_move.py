# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models
from odoo.tools import groupby


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_processible_quantity(self):
        self.ensure_one()
        # use available promised qty to estimate the shipping weight
        return self.ordered_available_to_promise_uom_qty

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        # Take the carrier_id from the group only when we have a related line
        # (i.e. we are in an OUT). It reflects the code of the super method in
        # "delivery" which takes the carrier of the related SO through SO line
        if self.sale_line_id:
            if group_carrier := self.group_id.carrier_id:
                vals["carrier_id"] = group_carrier.id
        return vals

    def _before_release(self):
        # Apply alternative carrier before updating the date
        self = self._apply_alternative_carrier()
        return super()._before_release()

    def _apply_alternative_carrier(self):
        for picking, moves_list in groupby(self, key=lambda move: move.picking_id):
            if not picking.carrier_id.alternative_carrier_ids:
                continue
            # Don't apply alternative carrier when there is already a released move
            if any(
                not move.need_release and move.state != "cancel"
                for move in picking.move_ids
            ):
                continue
            # For computing the best carrier, we need the released moves
            # to be isolated in a dedicated picking.
            # This is for instance required to have the picking estimated
            # shipping weight only for the released moves
            moves = self.browse().union(*moves_list)
            with self.env.cr.savepoint() as savepoint:
                all_need_release_moves = picking.move_ids.filtered("need_release")
                if moves != all_need_release_moves:
                    moves._unreleased_to_backorder(split_order=True)
                    picking = moves.picking_id
                # If a better carrier is found, assign it, otherwise rollback
                carrier_changed = picking._apply_alternative_carrier()
                if not carrier_changed:
                    savepoint.rollback()
        return self
