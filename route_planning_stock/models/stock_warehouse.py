from odoo import models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _create_or_update_route(self):
        res = super()._create_or_update_route()
        RouteArea = self.env["route.area"]
        for warehouse in self:
            area = RouteArea.search([("warehouse_id", "=", warehouse.id)], limit=1)
            if area:
                area._create_or_update_stock_records()
        return res

    def _find_or_create_custom_rule(self, rules):
        """Find or create stock rules based on the provided rules list.
        Each rule in the list should be a dictionary
        returned by _prepare_stock_rule_values method.
        :param rules: List of dictionaries with stock rule values.
        """
        StockRule = self.env["stock.rule"].sudo()
        for rule_val in rules:
            existing_rule = StockRule.with_context(active_test=False).search(
                [
                    ("picking_type_id", "=", rule_val["picking_type_id"]),
                    ("location_src_id", "=", rule_val["location_src_id"]),
                    ("location_dest_id", "=", rule_val["location_dest_id"]),
                    ("route_id", "=", rule_val["route_id"]),
                    ("action", "=", rule_val["action"]),
                ]
            )
            if not existing_rule:
                StockRule.create(rule_val)
            else:
                existing_rule.write(rule_val)

    def _prepare_stock_rule_values(
        self, route, routing, procure_method, location_dest_from_rule=False
    ):
        """Prepare the values to create or update a stock rule.
        :param route: stock.route record to which the rule will be linked.
        :param routing: The namedtuple
            containing from_loc, dest_loc, picking_type, and action.
        :param procure_method: 'make_to_stock' or 'make_to_order'.
        :param location_dest_from_rule: True or False.
        """
        return {
            "location_dest_from_rule": location_dest_from_rule,
            "name": self._format_rulename(
                routing.from_loc, routing.dest_loc, self.code
            ),
            "location_src_id": routing.from_loc.id,
            "location_dest_id": routing.dest_loc.id,
            "action": routing.action,
            "auto": "manual",
            "picking_type_id": routing.picking_type.id,
            "procure_method": procure_method,
            "warehouse_id": self.id,
            "company_id": self.company_id.id,
            "route_id": route.id,
            "propagate_carrier": True,
            "active": True,
        }
