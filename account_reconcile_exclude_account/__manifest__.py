# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Exclude accounts during reconciliation",
    "version": "14.0.1.0.0",
    "author": "PyTech, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/account-reconcile",
    "category": "Invoicing Management",
    "summary": "Allow to exclude journal items of specific accounts during reconciliation",
    "depends": [
        "account_reconciliation_widget",
    ],
    "data": [
        "views/account_journal_views.xml",
    ],
    "maintainers": [
        "SirPyTech",
    ],
}
