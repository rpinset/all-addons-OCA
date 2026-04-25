# Copyright 2024 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopfloor Vendor Packaging",
    "summary": "Manage shopfloor behavior for vendor packaging",
    "version": "18.0.1.1.0",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["jbaudoux", "TDu", "mmequignon"],
    "license": "AGPL-3",
    "application": False,
    "data": [
        "views/shopfloor_menu.xml",
    ],
    "depends": ["shopfloor", "product_packaging_level_vendor"],
    "auto_install": True,
}
