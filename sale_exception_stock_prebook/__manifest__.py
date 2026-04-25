# Copyright 2025 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Exception Stock Prebook",
    "summary": "Glue Addon to no release reservation if sale order has exceptions",
    "version": "16.0.1.1.0",
    "author": "MT Software, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/sale-prebook",
    "depends": [
        "sale_stock_prebook",
        "sale_exception",
    ],
    "maintainers": ["mt-software-de"],
    "auto_install": True,
}
