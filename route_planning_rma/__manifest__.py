# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning RMA Integration",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": [
        "route_planning_stock",
        "rma",
    ],
    "data": [
        "views/rma_views.xml",
        "wizard/stock_picking_return_views.xml",
        "wizard/rma_rma_wizard_views.xml",
    ],
    "installable": True,
    "auto_install": True,
    "maintainers": ["victoralmau"],
}
