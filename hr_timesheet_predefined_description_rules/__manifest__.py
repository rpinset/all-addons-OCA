# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "HR Timesheet Predefined Description Rules",
    "version": "16.0.1.0.0",
    "category": "Timesheet",
    "summary": "Manage predefined descriptions for timesheet entries",
    "license": "AGPL-3",
    "author": "Sygel, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/timesheet",
    "installable": True,
    "auto_install": False,
    "depends": ["hr_timesheet_sheet", "hr_timesheet_predefined_description"],
    "data": [
        "views/timesheet_predefined_description_views.xml",
        "views/account_analytic_line_views.xml",
    ],
}
