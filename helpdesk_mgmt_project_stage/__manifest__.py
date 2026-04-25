# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Helpdesk/Project stage synchronization",
    "summary": "Keeps the stages of tickets and tasks in sync",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "After-Sales",
    "website": "https://github.com/OCA/helpdesk",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "helpdesk_mgmt_project",
    ],
    "data": [
        "views/helpdesk_ticket_state.xml",
        "views/project_task_type.xml",
    ],
    "demo": [
        "demo/project_task_type.xml",
    ],
}
