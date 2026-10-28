{
    "name": "Barcode GS1 Stock",
    "version": "18.0.1.0.0",
    "category": "Inventory/Logistics",
    "summary": "Use the measure on a GS1 label as the quantity picked",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_gs1",
        "barcode_stock",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_gs1_stock/static/src/js/gs1_stock_quantity.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_gs1_stock/static/tests/**/*",
        ],
    },
    "installable": True,
    "auto_install": True,
}
