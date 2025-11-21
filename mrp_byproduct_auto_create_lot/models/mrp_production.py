from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _set_auto_lot(self):
        """Create and assign lots to by-products in the production order"""
        for production in self:
            lines = production.mapped("move_byproduct_ids.move_line_ids").filtered(
                lambda x: (
                    not x.lot_id
                    and not x.lot_name
                    and x.product_id.tracking != "none"
                    and x.product_id.auto_create_lot
                )
            )
            for move in lines:
                move.lot_name = move._get_lot_sequence()

    def _get_lot_sequence(self):
        self.ensure_one()
        return self.env["ir.sequence"].next_by_code("stock.lot.serial")

    def _action_done(self):
        self._set_auto_lot()
        return super()._action_done()

    def button_mark_done(self):
        self._set_auto_lot()
        return super().button_mark_done()
