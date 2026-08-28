# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mautic Connector",
    "summary": "Connect Odoo to a Mautic instance (OAuth2 backend configuration)",
    "version": "18.0.1.0.0",
    "category": "Connector",
    "website": "https://github.com/OCA/connector-mautic",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["CristianoMafraJunior"],
    "depends": [
        "connector",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "data": [
        "security/mautic_security.xml",
        "security/ir.model.access.csv",
        "views/mautic_backend_views.xml",
        "views/mautic_menuitem.xml",
    ],
    "installable": True,
    "application": False,
}
