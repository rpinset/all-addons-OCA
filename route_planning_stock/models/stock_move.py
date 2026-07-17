# Copyright 2025 Tecnativa - Carlos Lopez
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_route_area(self):
        if self.move_orig_ids and any(
            p.route_area_id for p in self.move_orig_ids.picking_id
        ):
            return self.move_orig_ids.picking_id.route_area_id
        return self.env["route.area"]

    def _get_new_picking_values(self):
        values = super()._get_new_picking_values()
        route_area = self._get_route_area()
        if route_area:
            values["route_area_id"] = route_area.id
        return values

    def _assign_picking_post_process(self, new=False):
        res = super()._assign_picking_post_process(new=new)
        if new:
            route_area_pickings = self.picking_id.filtered(lambda x: x.route_area_id)
            if route_area_pickings:
                route_area_pickings._find_auto_route()
        return res

    def _set_locations_from_record_route_area(self):
        """This method will be extended by other modules to apply the appropriate
        changes to the location of the linked picking moves.
        This method is called from a picking when the route area changes.
        """
        return
