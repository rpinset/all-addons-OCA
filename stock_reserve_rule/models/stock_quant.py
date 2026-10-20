# Copyright 2025 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.osv import expression


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _get_gather_domain(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
    ):
        domain = super()._get_gather_domain(
            product_id,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )
        if excluded_quant_ids := self.env.context.get("exclude_quant_ids"):
            domain = expression.AND([[("id", "not in", excluded_quant_ids)], domain])
        return domain
