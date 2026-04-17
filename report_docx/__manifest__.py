# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "DOCX reports",
    "summary": "Create report templates in DOCX and receive DOCX files",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Reporting",
    "website": "https://github.com/OCA/reporting-engine",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "external_dependencies": {
        "python": ["docxtpl"],
    },
    "depends": [
        "mail",
    ],
    "data": [
        "views/ir_actions_report.xml",
        "views/templates.xml",
    ],
    "demo": [
        "demo/ir_actions_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/report_docx/static/src/report_docx.esm.js",
        ]
    },
}
