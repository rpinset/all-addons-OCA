# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning Sale Stock Integration",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": [
        "route_planning_stock",
        "sale_stock",
    ],
    "data": ["views/sale_order_views.xml"],
    "installable": True,
    "auto_install": True,
    "maintainers": ["carlos-lopez-tecnativa"],
    "pre_init_hook": "pre_init_hook",
}
