{
    "name": "Barcode Scanner",
    "version": "18.0.1.0.0",
    "category": "Hidden",
    "summary": "Base scanning framework: client action, registries, scanner "
    "input and hooks",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/barcode-interface",
    "maintainers": ["szalatyzuzanna"],
    "license": "AGPL-3",
    "depends": [
        "web",
    ],
    "data": [
        "views/action.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "barcode_scanner/static/src/scss/barcode_scanner.scss",
            "barcode_scanner/static/src/xml/barcode_scanner_templates.xml",
            "barcode_scanner/static/src/js/registries.esm.js",
            "barcode_scanner/static/src/js/barcode_parser.esm.js",
            "barcode_scanner/static/src/js/utils/scan_match.esm.js",
            "barcode_scanner/static/src/js/barcode.esm.js",
            "barcode_scanner/static/src/js/api.esm.js",
            "barcode_scanner/static/src/js/router.esm.js",
            "barcode_scanner/static/src/js/store.esm.js",
            "barcode_scanner/static/src/js/app.esm.js",
            "barcode_scanner/static/src/js/services/feedback_service.esm.js",
            "barcode_scanner/static/src/js/hooks/use_barcode.esm.js",
            "barcode_scanner/static/src/js/hooks/use_barcode_handler.esm.js",
            "barcode_scanner/static/src/js/hooks/use_barcode_dispatcher.esm.js",
            "barcode_scanner/static/src/js/hooks/use_inventory.esm.js",
            "barcode_scanner/static/src/js/screens/main_screen.esm.js",
        ],
        "web.assets_unit_tests": [
            "barcode_scanner/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
