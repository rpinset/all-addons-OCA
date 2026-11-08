# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models
from odoo.fields import Domain


class StockForecasted(models.AbstractModel):
    _inherit = "stock.forecasted_product_product"

    def _product_sale_domain(self, product_template_ids, product_variant_ids):
        domain = super()._product_sale_domain(product_template_ids, product_variant_ids)
        return Domain(domain) & Domain("order_id.stock_is_reserved", "=", False)
