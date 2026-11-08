# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Removal Zone-Level FIFO",
    "summary": "Removal strategy giving priority to the goods that entered a"
    " storage zone first",
    "version": "18.0.1.0.0",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "category": "Stock Management",
    "depends": ["stock"],
    "data": [
        "data/stock_removal_data.xml",
        "views/stock_quant_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
    "development_status": "Beta",
    "license": "AGPL-3",
    "maintainers": ["jbaudoux"],
}
