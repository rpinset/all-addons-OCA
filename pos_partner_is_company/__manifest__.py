# Copyright 2021 initOS Gmbh
# Copyright 2019 Roberto Fichera
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "POS Partner - Is Company",
    "summary": "POS Support of 'Is Company' partner field",
    "version": "16.0.2.0.0",
    "category": "Point Of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale.assets": [
            "pos_partner_is_company/static/src/xml/**/*.xml",
            "pos_partner_is_company/static/src/js/**/*.esm.js",
        ],
    },
}
