# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Repair Picking",
    "version": "17.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "category": "Repair",
    "website": "https://github.com/OCA/repair",
    "summary": "Enhanced repair order management with pickings "
    "for adding and removing components",
    "depends": ["repair_restrict_lot", "repair_stock"],
    "data": [
        "views/stock_warehouse_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
}
