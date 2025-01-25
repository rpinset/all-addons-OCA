# Copyright 2024 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def _action_done(self):
        super()._action_done()
        for inventory in self:
            last_inventory_date = inventory.date
            done_locations = inventory.line_ids.location_id
            done_locations.write({"last_inventory_date": last_inventory_date})
