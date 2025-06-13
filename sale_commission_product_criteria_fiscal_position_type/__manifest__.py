# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Commission Product Criteria Fiscal Position Type",
    "summary": "Sale Commission Product Criteria Fiscal Position Type",
    "version": "16.0.1.0.0",
    "category": "Sales Management",
    "website": "https://github.com/OCA/commission",
    "author": "Sygel, Odoo Community Association (OCA)",
    "maintainers": ["tisho99"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_fiscal_position_partner_type",
        "sale_commission_product_criteria",
    ],
    "data": [
        "views/commission_item_views.xml",
    ],
}
