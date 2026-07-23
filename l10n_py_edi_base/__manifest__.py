{
    "name": "Paraguay - Electronic Invoicing Base",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "summary": "Base module for Electronic Invoicing in Paraguay",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "depends": [
        "account",
        "l10n_py_base",
        "l10n_py_account",
        "product",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/l10n_py_edi_security.xml",
        # Data
        "data/l10n_py_edi_document_types.xml",
        "data/ir_cron_data.xml",
        # Views
        "views/res_company_views.xml",
        "views/account_move_views.xml",
        "views/product_template_views.xml",
        "views/l10n_py_edi_log_views.xml",
        "views/l10n_py_associated_document_views.xml",
        "views/l10n_py_number_inutilization_views.xml",
        "views/l10n_py_transport_views.xml",
        # Wizards
        "wizard/account_move_send_edi_views.xml",
        "wizard/l10n_py_edi_cancel_wizard_views.xml",
        # Reports
        "report/kude_report_template.xml",
        "report/kude_report.xml",
        # Menus
        "views/l10n_py_edi_menu.xml",
        "views/edi_connector_views.xml",
    ],
    "external_dependencies": {
        "python": [
            "qrcode",
            "requests",
            "cryptography",
            "pykude",
        ],
    },
    "demo": [
        "demo/res_company_edi_demo.xml",
        "demo/account_move_nce_demo.xml",
        "demo/account_move_nde_demo.xml",
        "demo/account_move_nre_demo.xml",
        "demo/account_move_afe_demo.xml",
        "demo/l10n_py_associated_document_demo.xml",
        "demo/l10n_py_number_inutilization_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
