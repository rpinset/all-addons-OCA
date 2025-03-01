# Copyright 2023 ACSONE SA/NV
# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    product_cat_code_unique_restriction = fields.Selection(
        [
            ("system", "Whole System"),
            ("direct", "Parent-Children"),
            ("hierarchy", "Category Hierarchy"),
        ],
        string="Product Category Code Uniqueness Restriction",
        config_parameter="product_code_unique.product_code_unique_restriction",
        help=(
            "If no option is selected, no restriction applies.\n"
            "If you select:\n"
            "- Whole Sytem: Product Category Codes cannot be duplicated within the "
            " whole system\n"
            "- Parent-Children: Parent and Children Product Category Codes of the"
            " same category cannot be duplicated.\n"
            "- Category Hierarchy: Product Category Codes cannot be duplicated "
            "within the same category hierarchy.\n"
        ),
    )

    @api.constrains("product_cat_code_unique_restriction")
    def _check_product_cat_code_unique_restriction(self):
        restriction = self.product_cat_code_unique_restriction or "no"
        self.env["product.category"].search([])._code_restriction(restriction)
