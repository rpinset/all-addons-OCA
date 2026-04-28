# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_bulk = fields.Boolean(
        compute="_compute_is_bulk",
        readonly=False,
        store=True,
        help="Check this box if this product is sold without"
        " any manufactured packaging. It is usually the case"
        " for product whose unit of measure is a unit of weight"
        " or volume, but it can be also the case for products"
        " priced per unit but sold in bulk (such as cookies, bread, etc.)",
    )

    @api.depends("uom_id.category_id.measure_type")
    def _compute_is_bulk(self):
        for product in self:
            product.is_bulk = product.uom_id.category_id.measure_type in [
                "weight",
                "volume",
            ]
