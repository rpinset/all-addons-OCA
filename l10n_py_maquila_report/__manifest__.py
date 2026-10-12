# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Paraguay - Maquila Reports",
    "summary": "CNIME reports, dashboard, SIFEN extension, and SIMEX for Maquila",
    "version": "18.0.1.0.0",
    "category": "Localization",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "AGPL-3",
    "depends": [
        "l10n_py_maquila_base",
        "l10n_py_maquila_ops",
        "l10n_py_maquila_mrp",
        "l10n_py_edi_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/maquila_report_security.xml",
        "views/maquila_cnime_report_views.xml",
        "views/maquila_dashboard.xml",
        "views/maquila_program_views.xml",
        "views/maquila_report_menu.xml",
    ],
    "demo": [
        "demo/maquila_report_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
