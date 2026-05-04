{
    "name": "Paraguay - Base Localization",
    "version": "16.0.1.2.0",
    "category": "Localization",
    "summary": "Base localization data for Paraguay",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "depends": [
        "base",
        "base_address_extended",
        "l10n_latam_base",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Views (address view must load before res_country_data references it)
        "views/res_partner_address_view.xml",
        "views/l10n_py_neighborhood_views.xml",
        # Data
        "data/l10n_latam_identification_type_data.xml",
        "data/res_country_data.xml",
        "data/res_country_state_data.xml",
        "data/res_city_data.xml",
        "data/l10n_py_neighborhood_data.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
