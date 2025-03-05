# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models

from .stock_picking_type import REPORT_STICKER_POSITIONS


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_product_stickers = fields.Selection(
        selection=REPORT_STICKER_POSITIONS,
        compute="_compute_show_product_stickers",
        store=True,
        readonly=False,
        help="Show Product Stickers on pickings of this type.",
    )
    sticker_ids = fields.Many2many(
        comodel_name="product.sticker",
        string="Stickers",
        compute="_compute_sticker_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends("picking_type_id")
    def _compute_show_product_stickers(self):
        for picking in self:
            picking.show_product_stickers = (
                picking.picking_type_id.show_product_stickers
            )

    @api.depends("show_product_stickers", "move_line_ids.product_id")
    def _compute_sticker_ids(self):
        self.sticker_ids = False
        for picking in self:
            if not picking.show_product_stickers:
                continue
            picking.sticker_ids = picking.move_line_ids.product_id.get_product_stickers(
                extra_domain=[
                    "|",
                    ("available_model_ids.model", "in", [self._name]),
                    ("available_model_ids", "=", False),
                ]
            )
