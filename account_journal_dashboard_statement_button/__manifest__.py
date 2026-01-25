# Copyright 2024 r.perez@binhex.cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Journal Dashboard Statement Button",
    "category": "Accounting",
    "summary": """This module enhances the Account Journal Dashboard by introducing a
        shortcut button in the Bank and Cash journals. The button provides a direct link
        to the Bank Statements view.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-statement-import",
    "depends": ["account"],
    "data": [
        "views/account_journal_views.xml",
    ],
}
