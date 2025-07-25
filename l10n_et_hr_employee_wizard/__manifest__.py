# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "New Employee Wizard - Ethiopia",
    "summary": "Ethiopian localization of new employee wizard",
    "version": "14.0.1.0.0",
    "category": "Localization",
    "images": ["static/src/img/main_screenshot.png"],
    "license": "AGPL-3",
    "author": "TREVI Software, Michael Telahun Makonnen",
    "website": "https://github.com/trevi-software/trevi-hr",
    "depends": [
        "ethiopic_calendar",
        "hr_employee_wizard",
        "l10n_et_hr",
    ],
    "data": [
        "views/hr_recruitment_view.xml",
        "wizard/hr_employee_wizard_views.xml",
    ],
    "installable": True,
}
