# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_processible_quantity(self):
        self.ensure_one()
        # use available promised qty to estimate the shipping weight
        return self.ordered_available_to_promise_uom_qty
