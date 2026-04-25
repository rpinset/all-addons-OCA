# Copyright 2013-2016 Akretion - Alexis de Lattre
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2021 Tecnativa - Carlos Roca
# Copyright 2014-2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Payment SEPA Base",
    "summary": "Base module for SEPA file generation",
    "version": "18.0.3.0.0",
    "license": "AGPL-3",
    "author": "Akretion, Noviat, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "category": "Hidden",
    "depends": ["account_payment_batch_oca"],
    "excludes": ["account_banking_pain_base"],
    "external_dependencies": {"python": ["unidecode", "lxml"]},
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/account_payment_line.xml",
        "views/account_payment_lot.xml",
        "views/account_payment_order.xml",
        "views/account_payment_method_line.xml",
        "views/res_config_settings.xml",
        "views/account_payment_method.xml",
        "views/account_pain_regulatory_reporting.xml",
    ],
    "post_init_hook": "set_default_initiating_party",
    "installable": True,
}
