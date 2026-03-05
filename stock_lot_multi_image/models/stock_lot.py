# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockLot(models.Model):
    _name = "stock.lot"
    _inherit = ["stock.lot", "base_multi_image.owner", "image.mixin"]

    image_1920 = fields.Image(
        compute="_compute_image_1920",
        store=True,
        max_width=1920,
        max_height=1920,
    )

    @api.depends("image_ids")
    def _compute_image_1920(self):
        """
        Compute main image of lots
        """
        for lot in self:
            lot.image_1920 = fields.first(
                lot.with_context(bin_size=False).image_ids
            ).image_1920
