# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Paraguay - Maquila Base",
    "summary": "Base module for Paraguay Maquila regime (Ley 7547/2025)",
    "version": "18.0.1.0.0",
    "category": "Localization",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "AGPL-3",
    "depends": [
        "l10n_py_base",
        "agreement",
        "mail",
        "product",
        "analytic",
    ],
    "data": [
        "security/maquila_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/maquila_program_views.xml",
        "views/maquila_menu.xml",
    ],
    "demo": [
        "demo/maquila_program_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
