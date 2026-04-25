# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Stock Available to Promise Release - Carrier Alternative",
    "summary": "Advanced selection of preferred shipping methods",
    "version": "18.0.1.0.1",
    "category": "Operations/Inventory/Delivery",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "delivery_carrier_picking_valid",
        "stock_available_to_promise_release_delivery",
        "delivery_procurement_group_carrier",
    ],
    "data": [
        "views/delivery_carrier.xml",
    ],
}
