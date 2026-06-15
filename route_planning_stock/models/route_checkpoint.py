# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class RouteCheckpoint(models.Model):
    _inherit = "route.checkpoint"

    picking_id = fields.Many2one("stock.picking", copy=False, tracking=True)
    picking_domain = fields.Binary(compute="_compute_picking_domain")
    move_ids_without_package = fields.Many2many(
        "stock.move", compute="_compute_move_ids_without_package"
    )

    @api.depends("partner_id", "route_id", "route_id.route_area_id")
    def _compute_picking_domain(self):
        for checkpoint in self:
            checkpoint.picking_domain = [
                ("partner_id", "=", checkpoint.partner_id.id),
                ("route_area_id", "=", checkpoint.route_id.route_area_id.id),
                ("state", "not in", ["draft", "done", "cancel"]),
            ]

    @api.depends("picking_id")
    def _compute_move_ids_without_package(self):
        for checkpoint in self:
            checkpoint.move_ids_without_package = (
                checkpoint.picking_id.move_ids_without_package
            )

    def _prepare_vals_to_copy_incident(self, new_route):
        vals = super()._prepare_vals_to_copy_incident(new_route)
        vals.update({"picking_id": self.picking_id.id})
        return vals

    def action_back_to_planned(self):
        for checkpoint in self.filtered("picking_id"):
            if checkpoint.picking_id.state == "done":
                raise UserError(
                    self.env._(
                        "You cannot move back to planned a checkpoint "
                        "with a done picking."
                    )
                )
        return super().action_back_to_planned()

    def action_done(self):
        res = super().action_done()
        # Try to mark picking as done
        for checkpoint in self.filtered("picking_id"):
            picking = checkpoint.picking_id
            if picking.state not in ["done", "cancel"]:
                picking.move_ids.picked = True
                cancel_backorder = picking.picking_type_id.create_backorder == "never"
                picking.sudo().with_context(
                    cancel_backorder=cancel_backorder
                )._action_done()
                # Try to assign backorders to the same route area
                for backorder in picking.backorder_ids:
                    backorder.route_area_id = picking.route_area_id
                    backorder._find_auto_route()
        return res

    def action_view_picking(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.action_picking_tree_outgoing"
        )
        action.update(
            {
                "res_id": self.picking_id.id,
                "views": [(False, "form")],
            }
        )
        return action
