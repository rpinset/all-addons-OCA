# Copyright 2025 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "L10n Bg Report Stock",
    "summary": "Bulgaria - Accepted delivery documents in stock picking",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "license": "AGPL-3",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["stock", "l10n_bg_report_theme"],
    "data": [
        "report/report_accepted_deliveryslip.xml",
        "report/report_handover_protocol.xml",
        "report/stock_report_views.xml",
    ],
    "demo": [],
    "images": ["static/description/banner.png"],
    "tags": ["localization", "stock", "bulgaria", "reports"],
    "odoo_version": "18.0",
    "python_version": ">=3.11",
    "maintainers": ["rosenvladimirov"],
}
