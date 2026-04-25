# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Quant Available Quantity",
    "summary": "Shows Available Quantity in the stock quant views",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/OCA/stock-logistics-availability",
    "author": "Sygel, Odoo Community Association (OCA)",
    "maintainers": ["tisho99"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_quant_views.xml",
    ],
}
