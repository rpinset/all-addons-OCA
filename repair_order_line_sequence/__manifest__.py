# Copyright Cetmix OU 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Repair Order Line Sequence",
    "summary": "Allow to change line order in repairs",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/repair",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Manufacturing/Repair",
    "depends": ["repair"],
    "data": [
        "views/repair_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
