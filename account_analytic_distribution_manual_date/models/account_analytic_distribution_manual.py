# Copyright 2024 (APSL - Nagarro) Bernat Obrador
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountAnalyticDistributionManual(models.Model):
    _inherit = "account.analytic.distribution.manual"
    _sql_constraints = [
        (
            "check_start_end_date",
            "CHECK (start_date IS NULL OR end_date IS NULL OR end_date >= start_date)",
            "The end date must be greater than or equal to the start date.",
        ),
    ]

    start_date = fields.Date()
    end_date = fields.Date()
