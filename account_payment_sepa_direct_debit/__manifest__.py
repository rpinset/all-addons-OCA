# Copyright 2013-2020 Akretion (www.akretion.com)
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Payment SEPA Direct Debit",
    "summary": "Create SEPA files for Direct Debit",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion, Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/bank-payment-alternative",
    "category": "Banking addons",
    "depends": ["account_payment_sepa_base", "account_payment_mandate"],
    "excludes": ["account_banking_sepa_direct_debit"],
    "assets": {
        "web.report_assets_common": [
            "/account_payment_sepa_direct_debit/static/src/css/report.css"
        ],
    },
    "data": [
        "data/report_paperformat.xml",
        "reports/sepa_direct_debit_mandate.xml",
        "views/report_sepa_direct_debit_mandate.xml",
        "views/account_banking_mandate.xml",
        "views/res_company.xml",
        "views/res_config_settings.xml",
        "views/account_payment_method_line.xml",
        "views/account_payment_lot.xml",
        "data/mandate_expire_cron.xml",
        "data/account_payment_method.xml",
    ],
    "demo": ["demo/sepa_direct_debit_demo.xml"],
    "installable": True,
}
