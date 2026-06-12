# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Route Planning",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/route-planning",
    "depends": ["mail", "web_view_leaflet_map"],
    "external_dependencies": {"python": ["ortools"]},
    "data": [
        "security/route_planning_security.xml",
        "security/ir.model.access.csv",
        "data/mail_message_subtype_data.xml",
        "data/route_sequence.xml",
        "wizards/route_create_incident_views.xml",
        "views/res_partner_views.xml",
        "views/route_area_views.xml",
        "views/route_visitwindow_template_views.xml",
        "views/route_route_views.xml",
        "views/route_checkpoint_views.xml",
        "views/route_incident_type_views.xml",
        "views/route_planning_menus.xml",
    ],
    "demo": [
        "demo/route_area_demo.xml",
        "demo/route_incident.type_demo.xml",
        "demo/route_visitwindow_template_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/route_route_demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "route_planning/static/src/components/map-component/**/*"
        ],
    },
    "installable": True,
    "auto_install": False,
    "maintainers": ["carlos-lopez-tecnativa"],
}
