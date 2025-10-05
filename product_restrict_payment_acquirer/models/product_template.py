# Copyright Cetmix OU 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_payment_provider_ids = fields.Many2many(
        comodel_name="payment.provider",
        relation="product_payment_provider_rel",
        column1="product_id",
        column2="provider_id",
        copy=False,
        string="Allowed Payment Providers",
        domain=[("state", "in", ["enabled", "test"])],
    )
