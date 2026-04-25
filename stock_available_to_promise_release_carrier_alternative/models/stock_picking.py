# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _apply_alternative_carrier(self):
        self.ensure_one()
        carrier = self._get_preferred_carrier()
        if not carrier:
            return False
        if carrier == self.carrier_id:
            return False
        # Set a context key to not trigger a carrier change on the
        # procurement group
        self.with_context(skip_align_group_carrier=True).carrier_id = carrier
        return True

    def _get_preferred_carrier(self):
        self.ensure_one()
        picking_carrier = self.carrier_id
        # we consider current carrier as well allowing to configure better
        # carriers as alternative or less restrictive carrier as fallback
        possible_carriers = picking_carrier | picking_carrier.alternative_carrier_ids
        for carrier in possible_carriers.sorted("sequence"):
            if carrier._match_picking(self):
                return carrier
