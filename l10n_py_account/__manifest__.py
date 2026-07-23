{
    "name": "Paraguay - Accounting Extensions",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Accounting extensions for Paraguay localization",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "post_init_hook": "post_init_hook",
    "depends": [
        "account",
        "l10n_py",
        "l10n_py_base",
        "l10n_latam_invoice_document",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Data
        "data/l10n_latam_document_type_data.xml",
        "data/account_authorization_sequence.xml",
        # Views
        "views/account_authorization_views.xml",
        "views/account_journal_views.xml",
        "views/account_move_views.xml",
    ],
    "demo": [
        "demo/res_company_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/account_authorization_demo.xml",
    ],
    "external_dependencies": {
        "python": [
            "num2words",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
