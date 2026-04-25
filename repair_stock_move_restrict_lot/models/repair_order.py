from odoo import models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    def _prepare_repair_stock_move(self):
        vals = super()._prepare_repair_stock_move()
        if self.lot_id:
            vals["restrict_lot_id"] = self.lot_id.id
        return vals
