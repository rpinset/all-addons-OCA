# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning Delivery Integration",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": [
        "route_planning_sale_stock",
        "stock_delivery",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "wizard/choose_delivery_carrier_views.xml",
    ],
    "demo": ["demo/delivery_carrier_demo.xml"],
    "installable": True,
    "auto_install": True,
    "maintainers": ["carlos-lopez-tecnativa"],
}
