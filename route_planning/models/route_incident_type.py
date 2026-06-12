# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RouteIncidentType(models.Model):
    _name = "route.incident.type"
    _description = "Route Incident Type"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    rescheduled = fields.Boolean(
        default=False,
        help="If checked, checkpoints with this incident type will be rescheduled",
    )
    company_id = fields.Many2one("res.company")
