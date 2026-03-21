# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Street numbers and extensions",
    "summary": "Allows to customize partner street number parsing and formatting",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "base_address_extended",
        "base_setup",
        "web",
    ],
    "data": [
        "data/res_country.xml",
        "security/partner_street_number_security.xml",
        "security/ir.model.access.csv",
        "views/res_country.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
        "views/templates.xml",
        "wizards/partner_street_number_wizard.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/partner_street_number/static/src/css/partner_street_number.css",
        ],
    },
}
