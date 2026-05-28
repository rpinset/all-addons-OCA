# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    rma_returnable_uom_qty = fields.Float(
        compute="_compute_rma_returnable_uom_qty",
        string="RMA Returnable Quantity",
        digits="Product Unit of Measure",
        help="Quantity of this delivery move still eligible to be returned through RMA",
    )

    @api.depends("rma_ids", "product_uom_qty", "picking_type_id.code")
    def _compute_rma_returnable_uom_qty(self):
        for move in self:
            if move.picking_type_id.code != "outgoing":
                move.rma_returnable_uom_qty = 0
                continue

            already_in_rma = sum(
                rma.product_uom._compute_quantity(rma.product_uom_qty, move.product_uom)
                for rma in move.rma_ids
                if rma.state != "cancelled"
            )
            move.rma_returnable_uom_qty = move.product_uom_qty - already_in_rma
