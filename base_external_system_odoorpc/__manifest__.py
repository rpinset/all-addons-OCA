# Copyright 2026 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Base External System Odoo-rpc",
    "summary": "Connect to a remote Odoo instance via the odoorpc library.",
    "version": "16.0.1.0.0",
    "category": "Base",
    "website": "https://github.com/OCA/server-backend",
    "author": "Therp BV, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base_external_system"],
    "external_dependencies": {"python": ["odoorpc"]},
    "data": [
        "demo/external_system_odoo_demo.xml",
        "security/ir.model.access.csv",
        "views/external_system_views.xml",
    ],
}
