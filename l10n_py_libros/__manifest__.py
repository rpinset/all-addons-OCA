{
    "name": "Paraguay - Libros DNIT (RG 90/2021)",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Registro de comprobantes Ventas/Compras/Ingresos/Egresos (DNIT)",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "depends": [
        "account",
        "l10n_py_base",
        "l10n_py_account",
        "l10n_py_edi_base",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/l10n_py_libros_security.xml",
        # Data
        "data/l10n_latam_identification_type_data.xml",
        "data/l10n_py_libro_document_type_map_data.xml",
        # Views
        "views/l10n_py_libro_line_views.xml",
        "views/l10n_py_libro_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "wizard/l10n_py_libro_generate_wizard_views.xml",
        "views/l10n_py_libro_menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
