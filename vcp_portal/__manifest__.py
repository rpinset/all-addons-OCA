# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp Portal",
    "summary": """Version control platform integration with portal""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["vcp_management", "portal"],
    "data": [
        "templates/templates.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "vcp_portal/static/src/components/**/*.esm.js",
            "vcp_portal/static/src/components/**/*.xml",
            "vcp_portal/static/src/components/**/*.scss",
        ],
        "web.assets_tests": [
            "vcp_portal/static/tests/**/*",
        ],
    },
}
