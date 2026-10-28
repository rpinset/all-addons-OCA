{
    "name": "Barcode Stock Partner Delivery Zone",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "summary": "Filter and group the warehouse app's operations by delivery zone",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_stock",
        "partner_delivery_zone",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_stock_partner_delivery_zone/static/src/xml/delivery_zone_templates.xml",
            "barcode_stock_partner_delivery_zone/static/src/js/picking_list_delivery_zone.esm.js",
            "barcode_stock_partner_delivery_zone/static/src/js/picking_info_delivery_zone.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_stock_partner_delivery_zone/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": True,
}
