# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_uom", "product_uom_qty", "product_packaging_id")
    def _compute_pricelist_item_id(self):
        self = self.with_context(packaging=self.product_packaging_id)
        return super()._compute_pricelist_item_id()
