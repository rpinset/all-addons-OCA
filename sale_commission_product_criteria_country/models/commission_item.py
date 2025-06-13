# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CommissionItem(models.Model):
    _inherit = "commission.item"

    country_id = fields.Many2one(
        string="Customer Country",
        comodel_name="res.country",
        ondelete="restrict",
    )
