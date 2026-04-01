# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Payment Method Base + Payment Mode Glue",
    "summary": "Glue module for base views",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment",
    "depends": [
        "account_payment_mode",
        "account_payment_method_base",
    ],
    "data": [
        "views/account_payment_method.xml",
    ],
    "installable": True,
}
