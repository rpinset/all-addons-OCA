# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Quotation Builder",
    "category": "Sales/Sales",
    "summary": "Build great quotation templates",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Odoo Community Association (OCA), Odoo SA",
    "version": "17.0.1.0.0",
    "depends": ["website", "sale_management", "website_mail"],
    "data": [
        "data/sale_order_template_data.xml",
        "views/sale_portal_templates.xml",
        "views/sale_order_template_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
    "pre_init_hook": "pre_init_hook",
}
