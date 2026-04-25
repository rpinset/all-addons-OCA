# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Reservation Rules",
    "summary": "Configure reservation rules by location",
    "version": "18.0.1.2.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "category": "Stock Management",
    "depends": [
        "stock",
        "stock_location_is_sublocation",
        "stock_route_location_source",
        "product_packaging_level",
    ],
    "demo": [
        "data/demo/product_demo.xml",
        "data/demo/stock_location_demo.xml",
        "data/demo/stock_reserve_rule_demo.xml",
        "data/demo/stock_picking_demo.xml",
    ],
    "data": [
        "views/stock_reserve_rule_views.xml",
        "security/ir.model.access.csv",
        "security/stock_reserve_rule_security.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "license": "AGPL-3",
}
