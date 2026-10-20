{
    "name": "Barcode GS1",
    "version": "18.0.1.0.0",
    "category": "Hidden",
    "summary": "GS1 barcode parsing (GS1-128, application identifiers)",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "barcode_scanner",
        "barcodes_gs1_nomenclature",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_gs1/static/src/js/gs1_nomenclature.esm.js",
            "barcode_gs1/static/src/js/gs1_parser.esm.js",
            "barcode_gs1/static/src/js/gs1_startup.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_gs1/static/tests/**/*",
        ],
    },
    "installable": True,
    "auto_install": False,
}
