# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp Odoo",
    "summary": """Import Odoo modules from VCP Repositories""",
    "version": "18.0.1.0.1",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["vcp_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/vcp_odoo_module.xml",
        "views/vcp_odoo_module_version.xml",
        "views/vcp_odoo_bin_package.xml",
        "views/vcp_odoo_python_library.xml",
        "views/vcp_odoo_author.xml",
        "views/vcp_rule.xml",
        "views/menu.xml",
        "views/res_partner.xml",
        "data/vcp_rule.xml",
    ],
    "demo": [],
}
