# Copyright 2015-2021 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Supplier invoices on HR expenses",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/hr-expense",
    "depends": ["hr_expense"],
    "data": [
        "views/account_move_views.xml",
        "views/hr_expense_views.xml",
    ],
    "installable": True,
}
