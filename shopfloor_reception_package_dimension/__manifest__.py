# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Shopfloor Reception Package Dimension",
    "summary": "Collect Package Dimension from the Reception scenario",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["TDu"],
    "license": "AGPL-3",
    "installable": True,
    # Although `stock_storage_type`is already a shopfloor dependency.
    # It is planned to be removed there.
    "depends": [
        "shopfloor_reception",
        "stock_quant_package_dimension",
        "stock_storage_type",
    ],
}
