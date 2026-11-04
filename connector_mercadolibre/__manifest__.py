# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mercado Libre Connector",
    "summary": "Backend, OAuth, and notifications for Mercado Libre",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "category": "Connector",
    "author": "Gray Matter Logic, Odoo Community Association (OCA)",
    "maintainers": ["max3903"],
    "website": "https://github.com/OCA/connector-mercadolibre",
    "license": "AGPL-3",
    "depends": ["connector", "sale_management"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/mercadolibre_security.xml",
        "security/ir.model.access.csv",
        "data/queue_job_data.xml",
        "data/ir_cron.xml",
        "views/mercadolibre_backend_views.xml",
        "views/mercadolibre_notification_views.xml",
        "views/mercadolibre_menus.xml",
    ],
    "application": True,
    "installable": True,
}
