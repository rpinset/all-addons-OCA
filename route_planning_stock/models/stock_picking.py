# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    route_area_id = fields.Many2one(
        comodel_name="route.area",
        inverse="_inverse_route_area_id",
        string="Route Area",
        copy=False,
        help="Route area for this picking, used to create routes.",
    )
    route_checkpoint_ids = fields.One2many(
        comodel_name="route.checkpoint",
        inverse_name="picking_id",
        string="Route Checkpoints",
        copy=False,
    )
    has_route_planning = fields.Boolean(compute="_compute_has_route_planning")

    @api.depends("route_checkpoint_ids")
    def _compute_has_route_planning(self):
        for picking in self:
            picking.has_route_planning = bool(picking.route_checkpoint_ids)

    def _inverse_route_area_id(self):
        """When changing the route area (for example, using the wizard), we will update
        the route_area_id for pending pickings and moves
        """
        for item in self.filtered("move_ids"):
            item.move_ids._set_locations_from_record_route_area()
            # Change location_dest_id to be consistent
            item.location_dest_id = item.move_ids[0].location_dest_id
            # We removed the linked checkpoint because there may not be a defined
            # route area, or the route area may have changed and need to be added
            # to another route.
            item.route_checkpoint_ids.unlink()
            # We'll try to create a new one (it will only be created if necessary,
            # for example, if a route area is defined)
            item._find_auto_route()

    def action_cancel(self):
        checkpoints = self.route_checkpoint_ids.filtered(
            lambda x: x.state not in ("done", "incident")
        )
        current_checkpoint = fields.first(checkpoints)
        if current_checkpoint:
            if current_checkpoint.state != "draft":
                raise UserError(
                    self.env._(
                        "This picking cannot be cancelled "
                        "because it is associated with a route: %(route)s. "
                        "If you want to cancel it, first remove it from the route.",
                        route=current_checkpoint.route_id.display_name,
                    )
                )
            incident_picking_cancel = self.env.ref(
                "route_planning_stock.route_incident_cancel"
            )
            current_checkpoint._action_create_incident(
                incident_picking_cancel, self.env._("Cancelled from picking")
            )
        return super().action_cancel()

    def _action_done(self):
        checkpoint_map = {}
        for picking in self:
            checkpoints = picking.route_checkpoint_ids.filtered(
                lambda x: x.state not in ("done", "incident")
            )
            current_checkpoint = fields.first(checkpoints)
            checkpoint_map[picking.id] = current_checkpoint
            if current_checkpoint and current_checkpoint.route_id.state == "draft":
                raise UserError(
                    self.env._(
                        "This picking cannot be validated yet "
                        "because it is associated with route: %(route)s. "
                        "Which has not been planned yet. "
                        "If you want to validate it, please plan the route first.",
                        route=current_checkpoint.route_id.display_name,
                    )
                )
        res = super()._action_done()
        for picking in self:
            current_checkpoint = checkpoint_map.get(picking.id)
            if current_checkpoint:
                current_checkpoint.action_done()
        return res

    def action_view_route_planning(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "route_planning.action_route_route"
        )
        action.update(
            {
                "res_id": self.route_checkpoint_ids.route_id.id,
                "views": [(False, "form")],
            }
        )
        return action

    def _can_add_to_route(self):
        """Check if the picking can be added to a route"""
        self.ensure_one()
        location = (
            self.location_dest_id
            if self.picking_type_code == "incoming"
            else self.location_id
        )
        return (
            self.route_area_id
            and self.partner_id
            and location == self.route_area_id.location_id
            and self.state not in ["draft", "done", "cancel"]
        )

    def _find_auto_route(self):
        """Assign picking to a route or create a new one"""
        self.ensure_one()
        Route = self.env["route.route"]
        Checkpoint = self.env["route.checkpoint"]
        if not self._can_add_to_route():
            return
        # Look for existing route for today in this area
        route = Route.search(
            self._get_possible_route_domain(),
            limit=1,
        )
        if not route:
            route = Route.create(self._prepare_route_vals())
        # Create checkpoint for this picking's partner
        checkpoint = self.route_checkpoint_ids.filtered(lambda x: x.route_id == route)
        if not checkpoint:
            if (
                not self.partner_id.partner_latitude
                or not self.partner_id.partner_longitude
            ):
                # Try geo localize
                try:
                    with self.env.cr.savepoint():
                        self.partner_id.geo_localize()
                except Exception:
                    _logger.warning(
                        "Failed to geo localize partner %s", self.partner_id.name
                    )
            Checkpoint.create(self._prepare_route_checkpoint_vals(route))
            picking_msg = self.env._(
                "This picking is associated with the route: %s", route._get_html_link()
            )
            self.message_post(body=picking_msg)

    def _get_possible_route_domain(self):
        self.ensure_one()
        company = self.company_id or self.env.company
        start_location = (
            self.picking_type_id.warehouse_id.partner_id or company.partner_id
        )
        route_date = self._get_schedule_date_for_route()
        domain = [
            ("state", "=", "draft"),
            ("company_id", "=", company.id),
            ("route_area_id", "=", self.route_area_id.id),
            ("start_location_id", "=", start_location.id),
            ("schedule_date", "=", route_date.date()),
        ]
        return domain

    def _get_schedule_date_for_route(self):
        """Get the schedule date to use for route assignment."""
        now = fields.Datetime.now()
        max_date = max(self.scheduled_date or now, self.date_deadline or now)
        return fields.Datetime.context_timestamp(self, max_date)

    def _prepare_route_vals(self):
        company = self.company_id or self.env.company
        start_location = (
            self.picking_type_id.warehouse_id.partner_id or company.partner_id
        )
        route_date = self._get_schedule_date_for_route()
        return {
            "route_area_id": self.route_area_id.id,
            "start_location_id": start_location.id,
            "schedule_date": route_date.date(),
        }

    def _prepare_route_checkpoint_vals(self, route):
        return {
            "route_id": route.id,
            "partner_id": self.partner_id.id,
            "picking_id": self.id,
        }
