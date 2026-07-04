# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning Stock Integration",
    "version": "18.0.1.1.1",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": ["route_planning", "stock"],
    "data": [
        "data/route_incident_type_data.xml",
        "security/ir.model.access.csv",
        "views/route_area_views.xml",
        "views/route_checkpoint_views.xml",
        "views/route_route_views.xml",
        "views/stock_picking_views.xml",
    ],
    "demo": [
        "demo/route_area_demo.xml",
        "demo/route_route_demo.xml",
        "demo/stock_picking_demo.xml",
    ],
    "installable": True,
    "auto_install": True,
    "maintainers": ["carlos-lopez-tecnativa"],
}
