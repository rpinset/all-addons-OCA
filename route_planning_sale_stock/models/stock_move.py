# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_route_area(self):
        if self.sale_line_id.order_id and self.sale_line_id.order_id.route_area_id:
            return self.sale_line_id.order_id.route_area_id
        return super()._get_route_area()
