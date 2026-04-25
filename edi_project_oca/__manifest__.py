# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Edi Project",
    "summary": """
        Define EDI Configuration for Projects and Tasks
    """,
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "development_status": "Beta",
    "website": "https://github.com/OCA/edi-framework",
    "depends": [
        # Odoo addons
        "project",
        # OCA/connector
        "component_event",
        # OCA/edi-framework
        "edi_oca",
    ],
    "data": [
        "views/edi_exchange_record.xml",
        "views/project_project.xml",
        "views/project_task.xml",
    ],
    "demo": [],
}
