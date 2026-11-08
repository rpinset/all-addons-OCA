# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mercado Libre Connector - Products",
    "summary": "Listings, prices, and seller stock for Mercado Libre",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "category": "Connector",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/connector-mercadolibre",
    "license": "AGPL-3",
    "depends": ["connector_mercadolibre", "product", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "security/mercadolibre_product_security.xml",
        "data/queue_job_data.xml",
        "data/ir_cron.xml",
        "views/mercadolibre_backend_views.xml",
        "views/mercadolibre_product_views.xml",
        "views/mercadolibre_category_views.xml",
        "views/product_views.xml",
        "views/mercadolibre_menus.xml",
    ],
    "installable": True,
}
