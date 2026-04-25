# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Bulgarian Invoice Copy",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Add COPY watermark to Bulgarian invoice reports",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["account", "l10n_bg_report_theme"],
    "data": ["views/report_invoice_copy.xml"],
    "demo": [],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["static/description/banner.png"],
    "maintainers": ["rosenvladimirov"],
}
