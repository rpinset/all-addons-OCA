# Copyright 2021 Camptocamp SA
# Copyright 2024 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    last_inventory_date = fields.Datetime(
        "Last Inventory Date",
        help="Indicates the last inventory date for the location, "
        "including inventory done on parents location.",
    )
