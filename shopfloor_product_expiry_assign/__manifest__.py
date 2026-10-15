# Copyright 2025 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Shopfloor - Ignore expiration date",
    "summary": "Allow reserving expired lots from Shopfloor scenarios",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["jbaudoux", "simahawk", "sebalix", "TDu"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "shopfloor",
        # OCA/stock-logistics-reservation
        "product_expiry_assign",
    ],
    "data": [
        "views/shopfloor_menu.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
