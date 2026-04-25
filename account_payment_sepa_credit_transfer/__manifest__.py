# Copyright 2010-2020 Akretion (www.akretion.com)
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2016-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Account Payment SEPA Credit Transfer",
    "summary": "Create SEPA XML files for Credit Transfers",
    "version": "18.0.3.0.1",
    "license": "AGPL-3",
    "author": "Akretion, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "category": "Banking addons",
    "depends": ["account_payment_sepa_base"],
    "conflicts": ["account_sepa", "account_banking_sepa_credit_transfer"],
    "data": ["data/account_payment_method.xml"],
    "installable": True,
}
