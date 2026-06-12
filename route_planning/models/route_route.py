# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import math

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
ALL_DAY = 60 * 24  # 1440 minutes


class RouteRoute(models.Model):
    _name = "route.route"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Route"
    _order = "schedule_date desc"

    name = fields.Char(
        required=True, default=lambda self: self.env._("New"), copy=False, readonly=True
    )
    route_area_id = fields.Many2one(
        "route.area",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    time_start = fields.Float(
        compute="_compute_time_start",
        precompute=True,
        store=True,
        readonly=False,
        tracking=True,
    )
    waiting_time = fields.Float(
        compute="_compute_waiting_time",
        precompute=True,
        store=True,
        readonly=False,
        tracking=True,
        help="Average waiting time at each stop, expressed in minutes.",
    )
    start_location_id = fields.Many2one(
        comodel_name="res.partner",
        default=lambda self: self.env.company.partner_id,
        tracking=True,
    )
    user_id = fields.Many2one(
        "res.users",
        compute="_compute_user_id",
        precompute=True,
        store=True,
        readonly=False,
        tracking=True,
    )
    schedule_date = fields.Date(
        required=True, default=fields.Date.context_today, tracking=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("planned", "Planned"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        compute="_compute_state",
        store=True,
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        tracking=True,
    )
    checkpoint_ids = fields.One2many("route.checkpoint", "route_id")

    @api.depends("route_area_id")
    def _compute_time_start(self):
        for record in self:
            record.time_start = record.route_area_id.time_start

    @api.depends("route_area_id")
    def _compute_waiting_time(self):
        for record in self:
            record.waiting_time = record.route_area_id.waiting_time

    @api.depends("route_area_id")
    def _compute_user_id(self):
        for record in self:
            record.user_id = record.route_area_id.user_id

    @api.depends("checkpoint_ids", "checkpoint_ids.state")
    def _compute_state(self):
        for record in self:
            if not record.checkpoint_ids:
                record.state = "draft"
            elif all(cp.state in ["done", "incident"] for cp in record.checkpoint_ids):
                record.state = "done"
            elif any(cp.state in ["done", "incident"] for cp in record.checkpoint_ids):
                record.state = "in_progress"
            elif any(cp.state == "planned" for cp in record.checkpoint_ids):
                record.state = "planned"
            else:
                record.state = "draft"

    @api.constrains("time_start")
    def _check_time_start(self):
        for record in self:
            if record.time_start < 0 or record.time_start >= 24:
                raise UserError(
                    self.env._("The time start must be between 0 and 24 hours.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Override to set sequence and add user as follower"""
        for vals in vals_list:
            if vals.get("name", self.env._("New")) == self.env._("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("route.route")
        records = super().create(vals_list)
        for route in records:
            route.message_subscribe(partner_ids=[route.user_id.partner_id.id])
        return records

    def write(self, vals):
        checkpoints_by_route = {}
        if "checkpoint_ids" in vals:
            for route in self:
                checkpoints_by_route[route] = route.checkpoint_ids
        res = super().write(vals)
        # Subscribe the new user to the checkpoints
        if "user_id" in vals:
            partners = self.user_id.partner_id
            for checkpoint in self.checkpoint_ids:
                checkpoint.message_subscribe(partner_ids=partners.ids)
        # Reschedule checkpoints if needed
        if "checkpoint_ids" in vals:
            checkpoints_to_update_ids = []
            for command in vals["checkpoint_ids"]:
                if command[0] == 1:
                    checkpoints_to_update_ids.append(command[1])
            for route in self.filtered(lambda r: r.state in ["planned", "in_progress"]):
                current_checkpoints = (
                    checkpoints_by_route.get(route) or self.env["route.checkpoint"]
                )
                new_checkpoints = route.checkpoint_ids - current_checkpoints
                route._reschedule_checkpoints(
                    new_checkpoints, checkpoints_to_update_ids
                )
        return res

    def _reschedule_checkpoints(self, new_checkpoints, checkpoints_to_update_ids):
        Checkpoint = self.env["route.checkpoint"]
        common_domain = [("route_id", "=", self.id)]
        first_checkpoint = Checkpoint.search(
            common_domain + [("id", "in", checkpoints_to_update_ids)],
            order="sequence",
            limit=1,
        )
        before_checkpoint = Checkpoint.search(
            common_domain
            + [
                ("sequence", "<", first_checkpoint.sequence),
            ],
            order="sequence desc",
            limit=1,
        )
        checkpoints_to_reschedule = Checkpoint.search(
            common_domain
            + [
                ("id", "!=", first_checkpoint.id),
                ("state", "not in", ["done", "incident"]),
                ("sequence", ">", first_checkpoint.sequence),
            ]
        )
        first_sequence = 1
        if not before_checkpoint:
            starting_location = (
                self.start_location_id.partner_latitude,
                self.start_location_id.partner_longitude,
            )
            time_start = self.time_start
        else:
            starting_location = (
                before_checkpoint.latitude,
                before_checkpoint.longitude,
            )
            time_start = before_checkpoint.schedule_time
            first_sequence = before_checkpoint.sequence + 1
        # reschedule the first checkpoint to start from there
        self._action_optimize_route(
            time_start, starting_location, first_checkpoint, first_sequence
        )
        starting_location = (
            first_checkpoint.latitude,
            first_checkpoint.longitude,
        )
        # reschedule the rest of checkpoints
        if checkpoints_to_reschedule:
            self._action_optimize_route(
                first_checkpoint.schedule_time,
                starting_location,
                checkpoints_to_reschedule,
                first_sequence=first_checkpoint.sequence + 1,
            )
        if new_checkpoints:
            new_checkpoints.action_planned()

    @api.ondelete(at_uninstall=False)
    def _unlink_except_in_draft(self):
        if any(record.state != "draft" for record in self):
            raise UserError(
                self.env._("You cannot delete routes that are not in draft state.")
            )

    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        res = super().message_subscribe(partner_ids, subtype_ids)
        for checkpoint in self.checkpoint_ids:
            checkpoint.message_subscribe(partner_ids=partner_ids)
        return res

    def action_draft(self):
        self.checkpoint_ids.action_draft()

    def action_planned(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(self.env._("Only draft routes can be planned."))
        start_location = self.start_location_id
        if not start_location.partner_latitude or not start_location.partner_longitude:
            raise UserError(
                self.env._(
                    "The partner: %(partner)s must have latitude and longitude "
                    "to optimize the route.",
                    partner=start_location.display_name,
                )
            )
        starting_location = (
            start_location.partner_latitude,
            start_location.partner_longitude,
        )
        self._attach_checkpoint_with_incident()
        self._action_optimize_route(
            self.time_start, starting_location, self.checkpoint_ids
        )
        self.checkpoint_ids.action_planned()

    def _attach_checkpoint_with_incident(self):
        domain = self._prepare_domain_checkpoint_with_incident()
        checkpoints = self.env["route.checkpoint"].search(domain)
        for checkpoint in checkpoints:
            checkpoint.copy(checkpoint._prepare_vals_to_copy_incident(self))

    def _prepare_domain_checkpoint_with_incident(self):
        return [
            ("state", "=", "incident"),
            ("route_id.route_area_id", "=", self.route_area_id.id),
            ("incident_type_id.rescheduled", "=", True),
            ("checkpoint_ids", "=", False),
        ]

    def action_view_map(self):
        self.ensure_one()
        # TODO: How to show the start and end points
        # if no checkpoints exist for this,
        # or should we create fictitious records
        return {
            "name": self.env._("Route Map"),
            "type": "ir.actions.act_window",
            "res_model": "route.checkpoint",
            "view_mode": "leaflet_map",
            "domain": [("route_id", "=", self.id)],
        }

    def action_open_google_maps(self):
        maps_url = self._generate_google_maps_url()
        return {
            "type": "ir.actions.act_url",
            "url": maps_url,
            "target": "new",
        }

    def _generate_google_maps_url(self):
        """Generate Google Maps URL with waypoints in optimized order"""
        base_url = "https://www.google.com/maps/dir/"
        start_lat = self.start_location_id.partner_latitude
        start_lng = self.start_location_id.partner_longitude
        ordered_checkpoints = self.checkpoint_ids.sorted("sequence")
        waypoints = []
        # Add start location
        waypoints.append(f"{start_lat},{start_lng}")
        # Add checkpoints in order
        for checkpoint in ordered_checkpoints:
            if checkpoint.latitude and checkpoint.longitude:
                waypoints.append(f"{checkpoint.latitude},{checkpoint.longitude}")
        waypoints.append(f"{start_lat},{start_lng}")
        waypoints_str = "/".join(waypoints)
        params = [
            "travelmode=driving",  # Driving mode
            "optimize=false",  # Do not optimize (already optimized)
        ]
        full_url = f"{base_url}{waypoints_str}?{' & '.join(params)}"
        return full_url

    def _action_optimize_route(
        self, time_start, starting_location, checkpoints, first_sequence=1
    ):
        """Optimize the route based on partner locations using VRP in OR-Tools.
        :time_start: start time as float in hours
        :param starting_location: tuple of (latitude, longitude) for the start point
        :param checkpoints: recordset of route.checkpoint to optimize
        """
        # Get partner positions
        # Add starting location as first point
        locations = [starting_location]
        # The time windows is available all day (00:00 - 24:00)
        time_start *= 60  # Convert to minutes
        time_windows = [[(time_start, ALL_DAY)]]
        id_map = {0: None}
        for i, checkpoint in enumerate(checkpoints, start=1):
            latitude = checkpoint.latitude
            longitude = checkpoint.longitude
            partner = checkpoint.partner_id
            if partner and (not latitude or not longitude):
                # Try geo localize
                try:
                    with self.env.cr.savepoint():
                        partner.geo_localize()
                        latitude = partner.partner_latitude
                        longitude = partner.partner_longitude
                        checkpoint.write({"latitude": latitude, "longitude": longitude})
                except Exception:
                    _logger.warning("Failed to geo localize partner %s", partner.name)
            if not (latitude and longitude):
                _logger.warning("No coordinates found for %s", checkpoint.display_name)
                continue
            locations.append((latitude, longitude))
            id_map[i] = checkpoint
            # Get partner visit windows
            time_window_list = [
                (max(s.time_from * 60, time_start), s.time_to * 60)
                for s in partner.route_visitwindow_ids
                if s.day_of_week == str(self.schedule_date.weekday())
            ]
            # If partner has not delivery schedule means that is available for all day
            if not time_window_list:
                time_window_list = [(time_start, ALL_DAY)]
            time_windows.append(time_window_list)
        if len(locations) < 2:
            raise UserError(
                self.env._(
                    "Not enough addresses with coordinates for optimisation. "
                    "Please check that partners have latitude and longitude."
                )
            )
        # Resolver with VRP en OR-Tools
        self._solve_vrp(locations, id_map, time_windows, first_sequence)
        _logger.info(f"Route optimized with method VRP for route {self.name}.")

    def _compute_distance_matrix(self, locations):
        """Construct the matrix of distances between the points using Euclidean
        distance."""

        def compute_distance(loc1, loc2):
            return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

        return [
            [compute_distance(loc1, loc2) for loc2 in locations] for loc1 in locations
        ]

    def _solve_vrp(self, locations, id_map, time_windows, first_sequence=1):
        """Solve the Vehicle Routing Problem (VRP) with OR-Tools."""
        distance_matrix = self._compute_distance_matrix(locations)
        num_locations = len(distance_matrix)
        num_vehicles = 1  # Only one vehicle for all checkpoints
        depot = 0  # The start and stop point.
        max_waiting_time = 30  # Minutes
        time_dimension_name = "Time"
        max_travel_time = ALL_DAY  # Maximum travel time per vehicle in minutes

        manager = pywrapcp.RoutingIndexManager(num_locations, num_vehicles, depot)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            # Convert to meters
            return int(distance_matrix[from_node][to_node] * 1000)

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # Add time dimension
        routing.AddDimension(
            transit_callback_index,
            max_waiting_time,
            max_travel_time,
            False,  # Don't force start cumul to zero.
            time_dimension_name,
        )
        time_dimension = routing.GetMutableDimension(time_dimension_name)
        # Assign multiple time windows
        for i in range(num_locations):
            index = manager.NodeToIndex(i)
            earliest_window = min(
                time_windows[i], key=lambda w: w[0]
            )  # Seleccionar la ventana más temprana
            time_dimension.CumulVar(index).SetRange(
                int(earliest_window[0]), int(earliest_window[1])
            )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        # Search timeout
        search_parameters.time_limit.seconds = 10
        solution = routing.SolveWithParameters(search_parameters)
        if not solution:
            _logger.warning("An optimal solution for the route could not be found.")
            for checkpoint in id_map.values():
                # It could be None if the location is the starting point
                if not checkpoint:
                    continue
                checkpoint.write(
                    {
                        "sequence": 0,
                        "schedule_time": 0,
                    }
                )
            return
        # extract route from OR-Tools
        checkpoint_ids = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            # Ignore the start point
            if node in id_map and id_map[node]:
                time_var = time_dimension.CumulVar(node)
                time_minutes = solution.Value(time_var) / 60
                checkpoint = id_map[node]
                if self.waiting_time:
                    time_minutes += self.waiting_time
                checkpoint.write({"schedule_time": time_minutes})
                checkpoint_ids.append(checkpoint.id)
            index = solution.Value(routing.NextVar(index))
        checkpoints = self.env["route.checkpoint"].search(
            [("id", "in", checkpoint_ids)], order="schedule_time"
        )
        for seq, checkpoint in enumerate(checkpoints, start=first_sequence):
            checkpoint.write({"sequence": seq})
        return solution
