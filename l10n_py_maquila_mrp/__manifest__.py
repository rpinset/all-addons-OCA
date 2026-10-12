# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Paraguay - Maquila MRP",
    "summary": "BOM coefficients, VAN calculation, and waste management for Maquila",
    "version": "19.0.1.0.0",
    "category": "Localization",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "AGPL-3",
    "depends": [
        "l10n_py_maquila_base",
        "account",
        "mail",
        "mrp",
        "mrp_account",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/maquila_mrp_security.xml",
        "views/mrp_bom_views.xml",
        "views/mrp_production_views.xml",
        "views/maquila_waste_views.xml",
        "views/maquila_program_views.xml",
        "wizard/maquila_van_wizard_views.xml",
        "views/maquila_mrp_menu.xml",
    ],
    "demo": [
        "demo/maquila_mrp_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
