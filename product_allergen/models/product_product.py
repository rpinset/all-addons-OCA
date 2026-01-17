# Copyright 2025 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    allergen_ids = fields.Many2many(
        comodel_name="allergen.allergen",
        string="Allergens",
        help="Allergens present in this product variant",
    )
