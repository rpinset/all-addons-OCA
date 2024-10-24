# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Base User Role History",
    "summary": """
        This module allows to track the changes on users roles.""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-backend",
    "depends": [
        # Odoo
        "mail",
        # OCA
        "base_user_role",
    ],
    "data": [
        "security/base_user_role_line_history.xml",
        "views/base_user_role_line_history.xml",
        "views/res_users.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["ThomasBinsfeld"],
}
