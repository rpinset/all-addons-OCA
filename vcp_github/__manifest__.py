# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp Github",
    "summary": """Integrate Version Control Platform with Github""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": [
        "vcp_git",
    ],
    "external_dependencies": {
        "python": ["github3.py", "markdown"],
    },
    "data": [
        "data/data.xml",
    ],
    "demo": [
        "demo/demo_vcp_platform.xml",
    ],
}
