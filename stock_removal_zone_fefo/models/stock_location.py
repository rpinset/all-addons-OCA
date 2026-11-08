# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.model
    def _zone_removal_strategies(self):
        return super()._zone_removal_strategies() + ["zone_fefo"]
