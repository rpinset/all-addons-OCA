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

    def _get_rule_from_record_route_area(self, location_src_id, location_dest_id):
        rule = self.rule_id
        return rule.route_id.rule_ids.filtered(
            lambda r: r.location_src_id == location_src_id
            and r.location_dest_id == location_dest_id
            and r.procure_method == rule.procure_method
        )

    def _get_stock_move_vals_from_record_route_area(self, location_final):
        """This method will be extended by other modules to apply the appropriate
        changes of the linked picking moves.
        """
        self.ensure_one()
        vals = {}
        if not location_final:
            return vals
        rule = self.rule_id
        if self.location_final_id:
            rules = self._get_rule_from_record_route_area(
                rule.location_src_id, location_final
            )
            rules = rules.filtered(lambda x: x.action != "push")
        else:
            rules = self._get_rule_from_record_route_area(
                location_final, rule.location_dest_id
            )
        new_rule = rules[:1]
        if new_rule:
            vals["rule_id"] = new_rule.id
            vals["location_id"] = new_rule.location_src_id.id
            if new_rule.location_dest_from_rule or not self._get_route_area():
                # Although the _compute_location_dest_id() method in stock.move uses
                # this data, it does not have the appropriate "depends" field, and
                # we do not want to add it; therefore, we must change it manually
                vals["location_dest_id"] = new_rule.location_dest_id.id
            if self.location_final_id:
                vals["location_final_id"] = location_final.id
        return vals
