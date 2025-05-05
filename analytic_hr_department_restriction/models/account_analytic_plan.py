# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticPlan(models.Model):
    _inherit = "account.analytic.plan"

    department_id = fields.Many2one(
        comodel_name="hr.department",
        string="Department",
        domain="['|',('company_id', '=?', company_id),('company_id', '=', False)]",
    )
