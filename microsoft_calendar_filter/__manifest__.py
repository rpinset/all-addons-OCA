# Copyright 2025-2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Microsoft Calendar Filter",
    "summary": "Limit the records that are synchronized from Outlook to Odoo",
    "version": "16.0.1.0.0",
    "category": "Appointments",
    "website": "https://github.com/OCA/calendar",
    "author": "Odoo Community Association (OCA), Therp BV",
    "maintainers": ["NL66278"],
    "license": "AGPL-3",
    "depends": [
        "microsoft_calendar",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
