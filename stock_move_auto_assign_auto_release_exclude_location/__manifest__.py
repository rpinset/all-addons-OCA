# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock Move Auto Assign Auto Release Exclude Location",
    "summary": """
        Exclude locations from auto release moves after auto assign""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "BCIM, Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "depends": [
        "stock_move_auto_assign_auto_release",
        "stock_available_immediately_exclude_location",
    ],
    "data": [],
    "demo": [],
    "installable": True,
    "autoinstall": True,
}
