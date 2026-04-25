# Copyright 2025 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_line_description = fields.Text(
        related="sale_line_id.name",
        string="Sale line description",
        readonly=True,
        store=False,
    )
