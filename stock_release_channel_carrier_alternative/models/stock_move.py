# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _apply_alternative_carrier(self):
        # recompute the new channel when moves have been reassigned to a new
        # picking with a new carrier
        moves_had_channel = self.filtered(lambda m: m.picking_id.release_channel_id)
        previous_carriers = {
            p.id: p.carrier_id for p in moves_had_channel.picking_id if p.carrier_id
        }
        moves = super()._apply_alternative_carrier()
        moves_had_channel &= moves
        for picking in moves_had_channel.picking_id:
            if not picking.carrier_id:
                continue
            if (
                picking.id not in previous_carriers
                or picking.carrier_id != previous_carriers[picking.id]
            ):
                picking.release_channel_id = False
                picking.assign_release_channel()
        moves_missing_channel = moves_had_channel.filtered(
            lambda m: not m.picking_id.release_channel_id
        )
        # do not release moves that became orphan of a channel
        return moves - moves_missing_channel
