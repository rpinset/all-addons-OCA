# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_route_area(self):
        if self.sale_line_id.order_id and self.sale_line_id.order_id.route_area_id:
            return self.sale_line_id.order_id.route_area_id
        return super()._get_route_area()

    def _set_locations_from_record_route_area(self):
        # We define the appropriate data associated with the sol
        res = super()._set_locations_from_record_route_area()
        for item in self.filtered(lambda x: x.sale_line_id):
            vals = item._get_stock_move_vals_from_record_route_area(
                item.sale_line_id._get_location_final()
            )
            if vals:
                item.write(vals)
        return res
