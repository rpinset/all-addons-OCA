# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EndpointEndpoint(models.Model):
    _inherit = "endpoint.endpoint"

    product_assortment_id = fields.Many2one(
        comodel_name="ir.filters",
        domain=[("is_assortment", "=", True)],
    )
    include_prices = fields.Boolean()
    lang_id = fields.Many2one(
        comodel_name="res.lang",
    )
