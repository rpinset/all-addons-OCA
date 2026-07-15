{
    "name": "Paraguay - Accounting",
    "version": "18.0.2.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Localización contable para Paraguay",
    "author": "KMEE, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-paraguay",
    "license": "LGPL-3",
    "countries": ["py"],
    "depends": [
        "account",
    ],
    # El plan de cuentas vive en data/template/*.csv y models/template_py.py
    # (arquitectura de chart template de Odoo 17+); esos archivos se cargan
    # bajo demanda por account.chart.template y NO deben listarse en "data".
    "data": [],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
