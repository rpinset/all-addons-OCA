# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class RouteCheckpoint(models.Model):
    _name = "route.checkpoint"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Route Checkpoint"
    _order = "route_id, sequence"

    sequence = fields.Integer(default=10, tracking=True, copy=False)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("planned", "Planned"),
            ("done", "Done"),
            ("incident", "Incident"),
        ],
        default="draft",
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        ondelete="restrict",
        tracking=True,
    )
    route_id = fields.Many2one(
        "route.route",
        ondelete="cascade",
        required=True,
        tracking=True,
    )
    route_state = fields.Selection(related="route_id.state", string="Route State")
    user_id = fields.Many2one(
        "res.users",
        related="route_id.user_id",
        store=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="route_id.company_id",
        store=True,
    )
    incident_type_id = fields.Many2one(
        "route.incident.type",
        tracking=True,
        copy=False,
        readonly=True,
        ondelete="restrict",
    )
    schedule_date = fields.Date(
        related="route_id.schedule_date",
        store=True,
    )
    schedule_time = fields.Float(
        copy=False,
        tracking=True,
    )
    date_done = fields.Datetime(copy=False, readonly=True)
    origin_checkpoint_id = fields.Many2one(
        "route.checkpoint",
        copy=False,
        readonly=True,
        help="Original checkpoint when this is created from an incident",
    )
    checkpoint_ids = fields.One2many(
        "route.checkpoint", "origin_checkpoint_id", string="Checkpoints"
    )
    note = fields.Text()
    latitude = fields.Float(
        compute="_compute_latitude", store=True, readonly=False, digits=(10, 7)
    )
    longitude = fields.Float(
        compute="_compute_longitude", store=True, readonly=False, digits=(10, 7)
    )
    # fields needed for map visualization
    date_localization = fields.Date(related="partner_id.date_localization")
    display_address = fields.Char(compute="_compute_display_address")

    @api.depends("partner_id")
    def _compute_latitude(self):
        for record in self:
            record.latitude = record.partner_id.partner_latitude

    @api.depends("partner_id")
    def _compute_longitude(self):
        for record in self:
            record.longitude = record.partner_id.partner_longitude

    @api.depends("partner_id", "route_id")
    def _compute_display_name(self):
        for record in self:
            name = f"{record.route_id.name or ''}"
            if record.partner_id:
                name += f" - {record.partner_id.name}"
            else:
                name += f" - ID {record.id}"
            record.display_name = name

    @api.depends("partner_id")
    def _compute_display_address(self):
        for record in self:
            record.display_address = record.partner_id._display_address(
                without_company=True
            )

    @api.constrains("latitude", "longitude")
    def _check_latitude_longitude(self):
        for record in self:
            if not record.latitude or not record.longitude:
                raise UserError(
                    self.env._(
                        "Checkpoint %s does not have valid coordinates.",
                        record.display_name,
                    )
                )

    def write(self, vals):
        if "sequence" in vals:
            for checkpoint in self:
                previous_checkpoints = checkpoint.search_count(
                    [
                        ("route_id", "=", checkpoint.route_id.id),
                        ("sequence", ">=", vals["sequence"]),
                        ("id", "not in", self.ids),
                        ("state", "in", ["done", "incident"]),
                    ]
                )
                if previous_checkpoints:
                    raise UserError(
                        self.env._(
                            "You cannot set the sequence of checkpoint: %s to %s "
                            "because there are previous checkpoints "
                            "marked as done or incident.",
                            checkpoint.display_name,
                            vals["sequence"],
                        )
                    )
        return super().write(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_in_draft(self):
        if any(record.state != "draft" for record in self):
            raise UserError(
                self.env._("You cannot delete checkpoints that are not in draft state.")
            )

    def action_draft(self):
        self.state = "draft"

    def action_planned(self):
        self.state = "planned"

    def action_back_to_planned(self):
        self.state = "planned"

    def _check_previous_checkpoints_done(self):
        previous_checkpoints = self.search_count(
            [
                ("route_id", "=", self.route_id.id),
                ("sequence", "<", self.sequence),
                ("state", "not in", ["done", "incident"]),
            ]
        )
        if previous_checkpoints:
            raise UserError(
                self.env._(
                    "You must mark previous checkpoints as done "
                    "before marking this one as done."
                )
            )

    def action_done(self):
        for checkpoint in self:
            checkpoint._check_previous_checkpoints_done()
        self.write({"state": "done", "date_done": fields.Datetime.now()})

    def action_view_origin_checkpoint(self):
        self.ensure_one()
        return self.origin_checkpoint_id._open_checkpoint()

    def action_open_checkpoint(self):
        self.ensure_one()
        return self._open_checkpoint()

    def _open_checkpoint(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "route_planning.action_route_checkpoint"
        )
        action.update(
            {
                "res_id": self.id,
                "views": [(False, "form")],
            }
        )
        return action

    def _action_create_incident(self, incident_type, note):
        self.write(
            {
                "state": "incident",
                "incident_type_id": incident_type.id,
                "note": note,
            }
        )

    def _prepare_vals_to_copy_incident(self, new_route):
        self.ensure_one()
        return {
            "route_id": new_route.id,
            "origin_checkpoint_id": self.id,
        }
