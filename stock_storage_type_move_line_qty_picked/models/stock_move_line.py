# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_qty_picked(self):
        self.ensure_one()
        return self.qty_picked
