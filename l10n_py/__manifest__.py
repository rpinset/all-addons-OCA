{
    "name": "Paraguay - Accounting",
    "version": "16.0.1.1.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Localización contable para Paraguay",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        # Data - orden importante: try_loading debe ser el ÚLTIMO
        # porque necesita que todos los templates existan antes de ejecutarse
        "data/account_tax_group_data.xml",
        "data/account_chart_template_data.xml",
        "data/account.account.template.csv",
        "data/account_group.xml",
        "data/account_chart_template_account_account_link.xml",
        "data/account_tax_template_data.xml",
        "data/fiscal_position_template_data.xml",
        "data/account_chart_template_configure_data.xml",
        # Views
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
