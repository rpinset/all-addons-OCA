# Copyright 2025 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import Command, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def write(self, vals):
        skip_update_carrier_routes = self.env.context.get("skip_update_carrier_routes")
        if vals.get("carrier_id") and not skip_update_carrier_routes:
            # Update stock rules on moves when carrier is changed on transfers
            # not yet released.
            # This is only needed for Odoo 17.0+, allowing to set routes on carriers.
            orig_carriers = {rec: rec.carrier_id for rec in self}
            res = super().write(vals)
            for picking in self:
                # Update routes only when carrier has changed
                if picking.carrier_id != orig_carriers[picking]:
                    picking._update_moves_with_carrier_routes(orig_carriers[picking])
            return res
        return super().write(vals)

    def _update_moves_with_carrier_routes(self, old_carrier):
        """Update stock rules on transfer's moves based on new carrier's routes."""
        self.ensure_one()
        # Skip if transfer is already released
        if not self.need_release:
            return self.env["stock.move"]
        # Set a context key to not trigger a carrier change on the
        # procurement group
        defaults = {
            "carrier_id": self.carrier_id.id,
            "name": self.env._(
                "%s - Alternative carrier %s", self.group_id.name, self.carrier_id.name
            ),
        }
        self.group_id = self.group_id.copy(default=defaults)
        moves_to_reroute = self.move_ids.filtered(
            lambda m: m.state not in ("done", "cancel")
        )
        moves_to_reroute.group_id = self.group_id
        # Manage the carrier route
        moves_to_reroute.route_ids -= old_carrier.route_ids.filtered("active")
        moves_to_reroute.route_ids += self.carrier_id.route_ids.filtered("active")
        rerouted_moves = self.env["stock.move"]
        if moves_to_reroute:
            for move in moves_to_reroute:
                rule = self.env["procurement.group"]._get_rule(
                    move.product_id,
                    move.location_dest_id,
                    {
                        "warehouse_id": move.warehouse_id,
                        "product_packaging_id": move.product_packaging_id,
                        "route_ids": move.route_ids,
                    },
                )
                if rule and move.rule_id != rule:
                    move.write(
                        {
                            "location_id": rule.location_src_id.id,
                            "rule_id": rule.id,
                            "route_ids": [Command.link(rule.route_id.id)],
                            "picking_type_id": rule.picking_type_id.id,
                            "procure_method": rule.procure_method,
                            "propagate_cancel": rule.propagate_cancel,
                        }
                    )
                    rerouted_moves |= move
            rerouted_moves._unreleased_to_backorder(split_order=True)
        if not self.move_ids:
            self.state = "cancel"
        return rerouted_moves
