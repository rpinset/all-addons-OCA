# Copyright (C) 2025 - Today: Odoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_template_field_from_variant_field(self, fname, default=False):
        """Sets the value of the given field based on the template variant values

        Equals to product_variant_ids[fname] if it's a single variant product.
        Otherwise, sets the value specified in ``default``.
        It's used to compute fields like barcode, weight, volume..

        :param str fname: name of the field to compute
            (field name must be identical between product.product & product.template models)
        :param default: default value to set when there are multiple or no variants
        on the template
        :return: None
        """
        for template in self:
            variant_count = len(template.product_variant_ids)
            if variant_count == 1:
                template[fname] = template.product_variant_ids[fname]
            elif variant_count == 0 and self.env.context.get("active_test", True):
                # If the product has no active variants, retry without the active_test
                template_ctx = template.with_context(active_test=False)
                template_ctx._compute_template_field_from_variant_field(
                    fname, default=default
                )
            else:
                template[fname] = default

    def _set_product_variant_field(self, fname):
        """Propagate the value of the given field from the templates to their unique variant.

        Only if it's a single variant product.
        It's used to set fields like barcode, weight, volume..

        :param str fname: name of the field whose value should be propagated to the variant.
            (field name must be identical between product.product & product.template models)
        """
        for template in self:
            count = len(template.product_variant_ids)
            if count == 1:
                template.product_variant_ids[fname] = template[fname]
            elif count == 0:
                archived_variants = self.with_context(
                    active_test=False
                ).product_variant_ids
                if len(archived_variants) == 1:
                    archived_variants[fname] = template[fname]
