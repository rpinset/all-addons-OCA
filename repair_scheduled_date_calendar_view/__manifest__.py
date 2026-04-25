# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Scheduled Repair Calendar View",
    "summary": "Repair order calendar view based on scheduled data",
    "version": "18.0.1.0.0",
    "category": "Repair",
    "website": "https://github.com/OCA/repair",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base_repair_config"],
    "data": [
        "views/repair_order_views.xml",
        "views/res_config_settings_views.xml",
        "views/view_repair_order_form.xml",
    ],
}
