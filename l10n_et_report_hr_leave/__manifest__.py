# Copyright (C) 2025 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Ethiopia - Individual Leave Report",
    "summary": "Employeee HR Leave application and report for Ethiopia",
    "version": "14.0.1.0.1",
    "category": "Localization",
    "images": ["static/src/img/main_screenshot.png"],
    "license": "AGPL-3",
    "author": "TREVI Software",
    "website": "https://github.com/trevi-software/trevi-hr",
    "depends": [
        "hr_holidays",
        "ethiopic_calendar",
        "report_py3o",
    ],
    "data": [
        "report/all_reports.xml",
        "views/hr_leave_view.xml",
    ],
    "installable": True,
}
