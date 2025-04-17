# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _filter_auto_releaseable_locations(self, locations):
        return (
            super()
            ._filter_auto_releaseable_locations(locations)
            .filtered(lambda l: not l.exclude_from_immediately_usable_qty)
        )
