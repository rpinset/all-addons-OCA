# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Stock Available to Promise Release - Weight Volume",
    "summary": "Computes available to promise weight and volume",
    "version": "18.0.1.0.0",
    "category": "Operations/Inventory/Delivery",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock_available_to_promise_release",
        "delivery_total_weight_from_packaging",
        "stock_picking_volume",
    ],
}
