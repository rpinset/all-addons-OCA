{
    "name": "OCA Website Theme",
    "version": "18.0.1.0.0",
    "category": "Theme",
    "summary": "OCA Website Theme",
    "author": "Akretion, Odoo Community Association (OCA)",
    "company": "Akretion",
    "maintainer": "Akretion",
    "website": "https://github.com/OCA/oca-custom",
    "depends": [
        "website",
    ],
    "data": [
        "data/images.xml",
    ],
    "images": [
        "static/description/favicon.png",
        "static/description/theme_screenshot.png",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "oca_website/static/src/scss/primary_variables.scss",
        ],
        "web.assets_frontend": [
            "oca_website/static/src/scss/layout/website_theme.scss",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
}
