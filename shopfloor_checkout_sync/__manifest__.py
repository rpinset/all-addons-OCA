# Copyright 2020 Camptocamp (https://www.camptocamp.com)
{
    "name": "Shopfloor - Checkout Sync",
    "summary": "Glue module",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "category": "Warehouse Management",
    "version": "18.0.1.1.0",
    "license": "AGPL-3",
    "maintainers": ["jbaudoux", "mmequignon", "TDu"],
    "depends": [
        "shopfloor",
        # OCA/stock-logistics-workflow
        "stock_checkout_sync",
    ],
    "auto_install": True,
    "installable": True,
}
