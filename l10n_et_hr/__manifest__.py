# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Human Resources - Ethiopia",
    "summary": "Ethiopian localization of basic HR records",
    "version": "14.0.1.0.0",
    "category": "Localization",
    "images": ["static/src/img/main_screenshot.png"],
    "license": "AGPL-3",
    "author": "TREVI Software, Michael Telahun Makonnen",
    "website": "https://github.com/trevi-software/trevi-hr",
    "depends": [
        "hr",
        "ethiopic_calendar",
    ],
    "data": [
        "views/hr_employee_public_views.xml",
        "views/hr_employee_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
