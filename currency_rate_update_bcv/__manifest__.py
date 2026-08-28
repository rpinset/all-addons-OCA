# Copyright 2023 Luis Pinzón
# Copyright 2026 Anderson Armeya
# Copyright 2026 andyengit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Currency Rate Provider BCV",
    "summary": "Currency rate provider for BCV (Banco Central de Venezuela)",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Financial Management/Configuration",
    "countries": ["ve"],
    "author": "Luis Pinzón, Anderson Armeya, andyengit, "
    "Odoo Community Association (OCA)",
    "maintainers": ["lapinzon", "andyengit"],
    "website": "https://github.com/OCA/l10n-venezuela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["currency_rate_update"],
    "data": [
        "views/res_currency_rate_update_wizard_views.xml",
    ],
}
