# Copyright 2025 ForgeFlow (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class StockBuffer(models.Model):
    _inherit = "stock.buffer"

    def _search_stock_moves_incoming(self, outside_dlt=False):
        # WARNING: Overriding standard method.
        domain = self._search_stock_moves_incoming_domain(outside_dlt=outside_dlt)
        moves = self.env["stock.move"].search(domain)
        moves = moves.filtered(
            lambda move: (
                not move.location_id.is_sublocation_of(self.location_id)
                and (
                    move.location_dest_id.is_sublocation_of(self.location_id)
                    or (
                        move.location_final_id
                        and move.location_final_id.is_sublocation_of(self.location_id)
                        and not any(m in moves for m in move.move_dest_ids)
                    )
                )
            )
        )
        return moves
