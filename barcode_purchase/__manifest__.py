{
    "name": "Barcode Purchase",
    "version": "18.0.1.0.0",
    "category": "Inventory/Purchase",
    "summary": "Create purchase orders by barcode: scan products against a "
    "vendor and confirm the order from the scanner",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_scanner",
        "purchase_stock",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_purchase/static/src/scss/purchase.scss",
            "barcode_purchase/static/src/xml/purchase_templates.xml",
            "barcode_purchase/static/src/js/utils/avatar.esm.js",
            "barcode_purchase/static/src/js/screens/supplier_selector_screen.esm.js",
            "barcode_purchase/static/src/js/screens/buyer_selector_screen.esm.js",
            "barcode_purchase/static/src/js/screens/location_selector_screen.esm.js",
            "barcode_purchase/static/src/js/screens/product_selector_screen.esm.js",
            "barcode_purchase/static/src/js/screens/purchase_screen.esm.js",
            "barcode_purchase/static/src/js/tiles/purchase_menu_tiles.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_purchase/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
