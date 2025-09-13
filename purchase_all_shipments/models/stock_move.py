# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_move_dest_ids(self):
        """Recursively get all destination moves"""
        res = self.filtered("move_dest_ids").mapped("move_dest_ids")
        if res.filtered("move_dest_ids"):
            res |= res.filtered("move_dest_ids")._get_move_dest_ids()
        return res
