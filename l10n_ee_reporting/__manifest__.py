# Copyright 2020-2022 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Estonia - Reporting",
    "summary": "Estonian reporting localization",
    "version": "14.0.1.2.1",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-estonia",
    "author": "CorporateHub, Odoo Community Association (OCA)",
    "maintainers": ["alexey-pelykh"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_ee_accounting", "mis_builder"],
    "data": [
        "data/income_statement.xml",
        "data/balance_sheet.xml",
        "data/kmd_2017.xml",
        "security/ir.model.access.csv",
        "security/l10n_ee_reporting_security.xml",
        "views/l10n_ee_reporting.xml",
        "views/l10n_ee_reporting_kmd_inf.xml",
        "views/l10n_ee_reporting_vies_declaration.xml",
    ],
    "post_init_hook": "post_init_hook",
}
