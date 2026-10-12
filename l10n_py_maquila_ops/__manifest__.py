# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Paraguay - Maquila Operations",
    "summary": "Temporary admission, export, guarantees and fiscal ops for Maquila",
    "version": "19.0.1.0.0",
    "category": "Localization",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "AGPL-3",
    "depends": [
        "l10n_py_maquila_base",
        "account",
        "stock",
        "purchase",
        "sale_stock",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/maquila_ops_security.xml",
        "data/account_fiscal_position_data.xml",
        "data/stock_location_data.xml",
        "data/ir_cron_data.xml",
        "views/maquila_admission_views.xml",
        "views/maquila_export_views.xml",
        "views/maquila_guarantee_views.xml",
        "views/maquila_program_views.xml",
        "views/purchase_order_views.xml",
        "views/sale_order_views.xml",
        "views/account_payment_views.xml",
        "wizard/maquila_tum_wizard_views.xml",
        "wizard/maquila_tax_credit_wizard_views.xml",
        "views/maquila_ops_menu.xml",
    ],
    "demo": [
        "demo/maquila_ops_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
