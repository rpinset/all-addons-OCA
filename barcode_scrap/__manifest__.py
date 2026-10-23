{
    "name": "Barcode Scrap",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "summary": "Scrap damaged or lost goods from the Barcode app",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_scanner",
        "stock",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_scrap/static/src/scss/scrap.scss",
            "barcode_scrap/static/src/xml/scrap_templates.xml",
            "barcode_scrap/static/src/js/screens/scrap_location_screen.esm.js",
            "barcode_scrap/static/src/js/screens/scrap_product_selector_screen.esm.js",
            "barcode_scrap/static/src/js/screens/scrap_screen.esm.js",
            "barcode_scrap/static/src/js/tiles/scrap_menu_tiles.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_scrap/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
