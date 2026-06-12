# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RouteVisitwindowTemplate(models.Model):
    _name = "route.visitwindow.template"
    _description = "Visit Window Template"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    line_ids = fields.One2many(
        comodel_name="route.visitwindow.template.line",
        inverse_name="template_id",
        copy=True,
    )


class RouteVisitwindowTemplateLine(models.Model):
    _name = "route.visitwindow.template.line"
    _inherit = "route.visitwindow.mixin"
    _description = "Visit Window Template Line"
    _order = "day_of_week, time_from"

    template_id = fields.Many2one(
        comodel_name="route.visitwindow.template", required=True, ondelete="cascade"
    )

    _sql_constraints = [
        (
            "template_day_unique",
            "unique(template_id, day_of_week)",
            "A visit window for the same day of the week "
            "already exists in this template.",
        ),
    ]
