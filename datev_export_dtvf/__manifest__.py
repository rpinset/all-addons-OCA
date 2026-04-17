# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Datev Export DTVF",
    "summary": "Export Data for DATEV (dtvf)",
    "version": "18.0.2.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-germany",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account",
        "date_range",
        "datev_export",
    ],
    "data": [
        "data/ir_cron.xml",
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "views/account_account.xml",
        "views/datev_export_dtvf.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
    ],
}
