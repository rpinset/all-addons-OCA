# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Contract Recurrence In Price",
    "summary": """
        Add an option to include the recurrences
        in the total of a Sale Order Line.
    """,
    "version": "18.0.1.0.0",
    "category": "Contract Management",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/contract",
    "depends": ["product_contract"],
    "data": [
        "views/product_template.xml",
        "views/sale_order.xml",
        "wizards/product_contract_configurator_views.xml",
    ],
    "assets": {
        "web.assets_backend": ["product_contract_recurrence_in_price/static/src/js/*"]
    },
}
