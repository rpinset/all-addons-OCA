# Copyright 2023 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Bulgaria - Cities and Locations",
    "summary": (
        "Complete database of Bulgarian cities, municipalities, and "
        "administrative-territorial units with EKATTE codes."
    ),
    "version": "18.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Localization",
    "license": "LGPL-3",
    "author": "Odoo Community Association (OCA), Rosen Vladimirov",
    "maintainers": ["rosenvladimirov"],
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": [
        "base_address_extended",
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/res_city_types.xml",
        "data/res_country_data.xml",
        "views/res_city_view.xml",
    ],
    "demo": [],
    "post_init_hook": "post_init_hook",
    "images": [
        "static/description/banner.png",
    ],
    "tags": ["localization", "bulgaria", "cities", "ekatte", "geographic"],
    "countries": ["BG"],
    "odoo_version": "18.0",
    "python_version": ">=3.11",
}
