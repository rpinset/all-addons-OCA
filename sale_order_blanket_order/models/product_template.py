# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_blanket_order_overlap = fields.Boolean(
        help="If enabled, blanket orders for this product can have overlapping validity"
        "periods. By default, overlap is not allowed, ensuring only one active blanket "
        "order applies at a time.",
    )
