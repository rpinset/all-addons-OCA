# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


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
        # Unset 'with_expiration' key if 'ignore_expiration_date' is set
        # NOTE: 'with_expiration' key is used in overrides of
        # _update_reserved_quantity and _get_available_quantity methods
        # in product_expiry module to later generate a domain skipping expired
        # quants during reservation in stock module.
        if self.env.company.product_ignore_expiration_date or self.env.context.get(
            "ignore_expiration_date"
        ):
            self = self.with_context(with_expiration=False)
        return super()._get_gather_domain(
            product_id,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )
