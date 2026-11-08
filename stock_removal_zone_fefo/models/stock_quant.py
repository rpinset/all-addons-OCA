# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_removal_strategy_order(self, removal_strategy):
        if removal_strategy == "zone_fefo":
            # Standard FEFO, with the zone entry date as first tie-breaker.
            return "removal_date, zone_in_date, in_date, id"
        return super()._get_removal_strategy_order(removal_strategy)
