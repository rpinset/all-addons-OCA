# Copyright 2025 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class LocationContentTransfer(Component):
    _inherit = "shopfloor.location.content.transfer"

    def _create_moves_from_location(self, location):
        """Allow the reservation of expired lots if enabled on the menu."""
        moves = super()._create_moves_from_location(location)
        if self.work.menu.ignore_expiration_date:
            # Consumed by product_expiry_assign to bypass the product_expiry
            # constraint preventing the reservation of expired lots.
            moves = moves.with_context(ignore_expiration_date=True)
        return moves
