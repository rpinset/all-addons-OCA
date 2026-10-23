{
    "name": "Barcode Stock Quality",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "summary": "Run a reception's quality control inspections from the Barcode "
    "app, with photo evidence",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_stock",
        "quality_control_stock_oca",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_stock_quality/static/src/scss/quality.scss",
            "barcode_stock_quality/static/src/xml/quality_templates.xml",
            "barcode_stock_quality/static/src/js/components/quality_tab.esm.js",
            "barcode_stock_quality/static/src/js/patches/picking_screen_patch.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_stock_quality/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
