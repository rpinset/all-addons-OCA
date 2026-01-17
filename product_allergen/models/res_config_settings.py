# Copyright 2025 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_allergens_on_product_labels = fields.Boolean(
        string="Show Allergens on Product Labels",
        config_parameter="product_allergen.show_allergens_on_product_labels",
        help="Display allergen icons at the bottom of product labels",
    )
