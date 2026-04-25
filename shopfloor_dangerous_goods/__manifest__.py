# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Shopfloor Dangerous Goods",
    "summary": "Glue Module Between Shopfloor and Stock Dangerous Goods",
    "version": "18.0.1.1.0",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["mmequignon", "TDu", "jbaudoux"],
    "license": "AGPL-3",
    "application": True,
    "depends": [
        "shopfloor",
        # OCA/stock-logistics-workflow
        "stock_dangerous_goods",
    ],
    "data": [],
}
