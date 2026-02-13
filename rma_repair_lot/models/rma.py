# Copyright 2024 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RMA(models.Model):
    _inherit = "rma"

    def _get_repair_order_default_vals(self):
        vals = super()._get_repair_order_default_vals()
        if self.lot_id:
            vals["default_lot_id"] = self.lot_id.id
        return vals
