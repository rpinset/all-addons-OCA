# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class ProductPackagingLevel(models.Model):
    _inherit = "product.packaging.level"

    is_vendor_packaging = fields.Boolean(
        string="Vendor Packaging",
        default=False,
        help="Check this box if the packaging type is vendor specific.",
    )
