# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _prepare_batch_vals(self, rmas):
        self.ensure_one()
        if not rmas:
            return {}
        first_rma = rmas[0]
        return {
            "partner_id": first_rma.partner_id.id,
            "user_id": first_rma.user_id.id or self.env.user.id,
            "team_id": first_rma.team_id.id if first_rma.team_id else False,
            "tag_ids": [Command.set(first_rma.tag_ids.ids)]
            if first_rma.tag_ids
            else [],
            "state": "confirmed",
        }

    def action_create_returns(self):
        res = super().action_create_returns()
        moves = self.product_return_moves.move_id
        rmas = self.env["rma"].search([("move_id", "in", moves.ids)])
        if len(rmas) <= 1:
            return res
        rmas.batch_id = self.env["rma.batch"].create(self._prepare_batch_vals(rmas))
        return res
