# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    route_visitwindow_template_id = fields.Many2one(
        "route.visitwindow.template",
        string="Visit Window Template",
        help="Template to pre-fill visit windows for this partner, "
        "this field will be cleared after applying the template.",
    )
    route_visitwindow_ids = fields.One2many("route.partner.visitwindow", "partner_id")
    route_area_id = fields.Many2one(
        "route.area",
        company_dependent=True,
        compute="_compute_route_area_id",
        store=True,
        readonly=False,
    )

    @api.depends("zip", "state_id", "country_id")
    def _compute_route_area_id(self):
        RouteArea = self.env["route.area"]
        domain = [("auto_assign", "=", True), ("company_id", "=", self.env.company.id)]
        all_areas = RouteArea.search(domain).sorted(
            key=lambda area: area._get_specificity_score(), reverse=True
        )
        for partner in self:
            area_found = self.env["route.area"]
            for area in all_areas:
                if area._match_address(partner):
                    area_found = area
                    break
            partner.route_area_id = area_found

    @api.onchange("route_visitwindow_template_id")
    def _onchange_route_visitwindow_template_id(self):
        # Fill visit windows based on the template
        if self.route_visitwindow_template_id:
            template = self.route_visitwindow_template_id
            self.route_visitwindow_ids = [Command.clear()] + [
                Command.create(
                    {
                        "day_of_week": line.day_of_week,
                        "time_from": line.time_from,
                        "time_to": line.time_to,
                    }
                )
                for line in template.line_ids
            ]
            self.route_visitwindow_template_id = False

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ["route_area_id"]


class RoutePartnerVisitwindow(models.Model):
    _name = "route.partner.visitwindow"
    _inherit = "route.visitwindow.mixin"
    _description = "Partner Visit Window"

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
        ondelete="cascade",
        help="Partner for this visit window",
    )

    _sql_constraints = [
        (
            "partner_day_unique",
            "unique(partner_id, day_of_week)",
            "A visit window for the same day of the week "
            "already exists for this partner.",
        ),
    ]
