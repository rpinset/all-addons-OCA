# Copyright 2025 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Stock Sale Line Description",
    "summary": "Show sale order line description on pickings and delivery slips",
    "version": "18.0.1.0.1",
    "license": "LGPL-3",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["stock", "sale_stock"],
    "data": [
        "security/res_groups.xml",
        "views/stock_picking_views.xml",
        "report/report_deliveryslip.xml",
    ],
    "demo": [],
    "tags": ["stock", "sale", "reports"],
    "odoo_version": "18.0",
    "python_version": ">=3.11",
    "images": ["static/description/banner.png"],
    "maintainers": ["rosenvladimirov"],
}
