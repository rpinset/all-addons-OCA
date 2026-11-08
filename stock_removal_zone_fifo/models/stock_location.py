# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.model
    def _zone_removal_strategies(self):
        # Extended by the modules adding another zone-based strategy.
        return ["zone_fifo"]

    @api.model
    def _is_same_zone(self, source_zone, destination_zone):
        """Tell whether both zones are the same one. An empty destination zone is
        the exception: it is True unless zone_in_date_update_out_of_zone is set."""
        if source_zone == destination_zone:
            return True
        if not destination_zone:
            # zone_in_date_update_out_of_zone is when destination has no zone !

            # Entering a zone, even from non-zone location, must always update.
            # Otherwise, this would cause a bug:
            # Zone A -> no zone -> Zone B would bypass the zone_in_date update.
            return not self.env.company.zone_in_date_update_out_of_zone
        return False

    def _get_zone_location(self):
        """Nearest ancestor, self included, whose removal strategy defines a
        zone. Empty when no ancestor carries one."""
        self.ensure_one()
        methods = self._zone_removal_strategies()
        location = self.sudo()
        while location:
            if location.removal_strategy_id.method in methods:
                return location
            location = location.location_id
        return self.browse()
