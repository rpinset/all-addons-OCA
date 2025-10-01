# Copyright 2025 Factor Libre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # remove rounding from volume and weight
    # this is needed to avoid rounding errors when converting between units
    # and is safe since we display the net weight in the product's
    # net weight UOM. In the same time, we need to keep the net weight
    # we ensure that no information is lost by storing the volume and weight
    # without rounding.
    net_weight = fields.Float(digits=False)

    product_net_weight = fields.Float(
        "Net Weight",
        digits="Stock Weight",
        help="The net weight in the product's weight UOM, container excluded.",
        compute="_compute_product_net_weight",
        inverse="_inverse_product_net_weight",
    )

    @api.depends("net_weight", "product_tmpl_id.weight_uom_id")
    def _compute_product_net_weight(self):
        """Compute net weight in product UOM from system UOM."""
        odoo_weight_uom = (
            self.product_tmpl_id._get_weight_uom_id_from_ir_config_parameter()
        )
        for product in self:
            if product.net_weight and product.weight_uom_id:
                product.product_net_weight = odoo_weight_uom._compute_quantity(
                    qty=product.net_weight,
                    to_unit=product.weight_uom_id,
                    round=False,  # avoid losing information
                )
            else:
                product.product_net_weight = 0.0

    def _inverse_product_net_weight(self):
        """Set net weight in system UOM from product UOM."""
        odoo_weight_uom = (
            self.product_tmpl_id._get_weight_uom_id_from_ir_config_parameter()
        )
        for product in self:
            if product.product_net_weight and product.weight_uom_id:
                product.net_weight = product.weight_uom_id._compute_quantity(
                    qty=product.product_net_weight,
                    to_unit=odoo_weight_uom,
                    round=False,  # avoid losing information
                )
            else:
                product.net_weight = 0.0
