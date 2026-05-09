{
    "name": "Project Timesheet Billable per Line",
    "summary": "Generate sales orders from billable"
    " timesheets grouped by analytic account",
    "version": "17.0.1.0.0",
    "category": "Services/Timesheets",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/timesheet",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet",
        "sale",
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_task_views.xml",
        "views/hr_employee_views.xml",
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
