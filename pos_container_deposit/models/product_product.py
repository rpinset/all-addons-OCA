# Copyright 2021 Sunflower IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    deposit_product_id = fields.Many2one(
        "product.product",
        "Deposit",
        domain=[("is_deposit", "!=", False)],
        help="If this product is packaged in a container for which you charge deposit, "
        "add a product here that stands for the deposit",
    )
