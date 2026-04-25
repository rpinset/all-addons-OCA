# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Shopfloor - Delivery with shipment advice",
    "summary": "Manage delivery process with shipment advices",
    "version": "18.0.1.2.0",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-shopfloor",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "maintainers": ["jbaudoux", "sebalix", "TDu", "mmequignon"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        # OCA/wms
        "shopfloor",
        # OCA/stock-logistics-transport
        "shipment_advice",
    ],
    "data": ["data/shopfloor_scenario_data.xml", "views/shopfloor_menu.xml"],
    "demo": ["demo/shopfloor_profile_demo.xml", "demo/shopfloor_menu_demo.xml"],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
