# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockLocation(models.Model):
    _inherit = "stock.location"

    def _get_zone_location(self):
        # no fallback on the ancestor carrying the removal strategy: an empty
        # zone_location_id already means this location is in no zone
        return self.zone_location_id
