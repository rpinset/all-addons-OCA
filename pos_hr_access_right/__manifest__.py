# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale HR- Extra Access Right",
    "version": "16.0.1.0.1",
    "category": "Point Of Sale",
    "summary": "Point of Sale HR - Extra Access Right for certain actions",
    "author": "Binhex ,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "depends": ["pos_hr", "pos_access_right"],
    "data": [],
    "assets": {
        "point_of_sale.assets": [
            "pos_hr_access_right/static/src/js/*.js",
        ]
    },
    "maintainers": ["adasatorres"],
    "installable": True,
}
