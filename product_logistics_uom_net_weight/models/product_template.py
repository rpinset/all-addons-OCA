# Copyright 2025 Factor Libre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_net_weight = fields.Float(
        "Net Weight in product UOM",
        compute="_compute_product_net_weight",
        inverse="_inverse_product_net_weight",
        digits="Stock Weight",
        store=True,
        help="The net weight in the product's weight UOM, container excluded.",
    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.product_net_weight",
    )
    def _compute_product_net_weight(self):
        """Compute net weight from variants."""
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.product_net_weight = (
                template.product_variant_ids.product_net_weight
            )
        for template in self - unique_variants:
            template.product_net_weight = 0.0

    def _inverse_product_net_weight(self):
        """Set net weight on variants."""
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.product_net_weight = (
                    template.product_net_weight
                )

    def _prepare_variant_values(self, combination):
        """Add product_net_weight to variant values."""
        res = super()._prepare_variant_values(combination)
        if self.product_net_weight:
            res.update(
                {
                    "product_net_weight": self.product_net_weight,
                }
            )
        return res
