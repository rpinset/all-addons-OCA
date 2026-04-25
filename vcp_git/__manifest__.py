# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp Git",
    "summary": """Allows to download code from git""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": [
        "vcp_management",
    ],
    "external_dependencies": {
        "python": ["GitPython"],
    },
}
