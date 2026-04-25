# Copyright 2025 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Account Statement Import Mt940",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["account_statement_import_file"],
    "data": ["wizard/account_statement_import.xml"],
    "external_dependencies": {"python": ["mt-940"]},
    "demo": [],
    "images": ["static/description/banner.png"],
    "maintainers": ["rosenvladimirov"],
}
