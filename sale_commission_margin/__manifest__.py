# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Commission Margin",
    "summary": """This addons allows commissions to be deducted from the margin.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/commission",
    "depends": [
        "sale_margin",
        "sale_commission",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "demo": [],
}
