# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    crowdfunding_default_fee_percentage = fields.Float(
        "Default fee percentage",
        help="The percentage of money pledged for a "
        "challenge your organization uses to pay for overhead",
    )
    crowdfunding_product_id = fields.Many2one(
        "product.product",
        string="Product",
        help="This product is used to create invoices and vendor bills.",
        default=lambda self: self.env.ref(
            "crowdfunding.product_crowdfunding", raise_if_not_found=False
        ),
    )
