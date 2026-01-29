# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CRM Team ZIP Assignment",
    "summary": "Auto-assign CRM teams to partners based on ZIP code patterns",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "depends": ["crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_team_views.xml",
        "views/res_partner_views.xml",
    ],
}
