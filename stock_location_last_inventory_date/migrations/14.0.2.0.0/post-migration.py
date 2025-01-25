# Copyright 2024 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.addons.stock_location_last_inventory_date.hooks import (
    set_initial_last_inventory_date,
)


def migrate(cr, version):
    set_initial_last_inventory_date(cr)
