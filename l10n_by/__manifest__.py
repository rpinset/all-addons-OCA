# Copyright 2026 Aliaksandr Zubik <alexzub@tut.by> (https://artcloud.by)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Belarus - Accounting",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Chart of Accounts and Taxes for Belarus",
    "author": "Aliaksandr Zubik, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-belarus",
    "license": "AGPL-3",
    "countries": ["by"],
    "depends": [
        "account",
    ],
    "data": [
        "data/account_tax_report_data.xml",
    ],
    "installable": True,
    "auto_install": False,
}
