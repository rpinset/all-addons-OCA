# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Project Task Multilang",
    "summary": (
        "Add multilingual support for project task fields in Bulgarian localization"
    ),
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "author": "Odoo Community Association (OCA), Rosen Vladimirov",
    "maintainer": "Rosen Vladimirov",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "category": "Localization",
    "depends": [
        "project",
        "partner_multilang",
    ],
    "data": [
        # View файлове ще бъдат добавени когато са готови
    ],
    "demo": [],
    "assets": {},
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "external_dependencies": {
        "python": [],
    },
    "development_status": "Production/Stable",
    "maintainers": ["rosenvladimirov"],
    "support": "https://github.com/OCA/l10n-bulgaria/issues",
    "countries": ["BG"],
}
