# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    include_recurrence_in_price = fields.Boolean(
        help="The amounts of the Sale Order Line will be multiplied"
        "by the number of times the line will be invoiced."
    )
