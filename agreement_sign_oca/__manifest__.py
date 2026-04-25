# Copyright 2025  APSL-Nagarro - Miquel Alzanillas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Agreement Sign Oca",
    "version": "17.0.1.1.0",
    "category": "Agreement",
    "website": "https://github.com/OCA/sign",
    "author": "APSL Nagarro, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sign_oca", "agreement_legal"],
    "data": [
        "views/agreement_views.xml",
        "views/res_config_settings_view.xml",
        "views/sign_oca_request_views.xml",
        "data/data.xml",
    ],
    "demo": [
        "demo/sign_oca_template.xml",
    ],
    "installable": True,
    "maintainers": ["miquelalzanillas"],
}
