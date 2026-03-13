# Copyright 2010-2020 Akretion (www.akretion.com)
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2016-2022 Tecnativa - Pedro M. Baeza
# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Account Banking International Credit Transfer",
    "summary": "Create PAIN XML files for International Credit Transfers",
    "version": "17.0.1.0.0",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "Akretion, Tecnativa, Odoo Community Association (OCA), Camptocamp SA",
    "website": "https://github.com/OCA/bank-payment",
    "category": "Banking addons",
    "depends": ["account_banking_pain_base"],
    "data": [
        "data/account_payment_method.xml",
        "views/res_partner_bank_views.xml",
    ],
    "installable": True,
}
