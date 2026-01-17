# Copyright 2025 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allergen_ids = fields.Many2many(
        comodel_name="allergen.allergen",
        string="Allergens",
        compute="_compute_allergen_ids",
        inverse="_inverse_allergen_ids",
        store=False,
        help="Allergens present in this product template. "
        "When the template has a single variant, changes are "
        "applied to that variant. When there are multiple variants,"
        " this shows the union of all variant allergens.",
    )

    @api.depends("product_variant_ids.allergen_ids")
    def _compute_allergen_ids(self):
        """Compute allergens from variants.

        Shows the union of allergens from all variants.
        """
        for template in self:
            if template.product_variant_ids:
                # Get all unique allergens from all variants
                all_allergens = template.product_variant_ids.mapped("allergen_ids")
                template.allergen_ids = all_allergens
            else:
                template.allergen_ids = False

    def _inverse_allergen_ids(self):
        """Apply allergen changes to variants.

        If the template has a single variant, apply changes to that variant.
        If there are multiple variants, this is a no-op as each variant should
        be edited individually.
        """
        single_variant_templates = self.filtered(
            lambda t: len(t.product_variant_ids) == 1
        )
        for template in single_variant_templates:
            template.product_variant_ids.allergen_ids = template.allergen_ids
