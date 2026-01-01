# Copyright 2025 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Cancel Optional Email",
    "version": "18.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "category": "Sales",
    "license": "AGPL-3",
    "summary": "Cancel sales orders directly without "
    "proposing to send email to customer",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": ["sale"],
    "data": [
        "views/sale_order_views.xml",
        "wizard/sale_order_cancel_views.xml",
    ],
    "installable": True,
}
