# Copyright 2025 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
{
    "name": "Stock Available to Promise Release - Delivery",
    "summary": "Glue module between release mechanism and delivery.",
    "version": "18.0.1.0.1",
    "category": "Operations/Inventory/Delivery",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "stock_delivery",
        "stock_available_to_promise_release",
    ],
}
