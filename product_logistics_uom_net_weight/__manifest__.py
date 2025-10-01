# Copyright 2025 Factor Libre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Logistics UoM Net Weight Integration",
    "summary": (
        "Integration module for product_logistics_uom and "
        "product_net_weight compatibility"
    ),
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Factor Libre, Odoo Community Association (OCA)",
    "maintainers": ["factorlibre"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "product_logistics_uom",
        "product_net_weight",
    ],
    "data": [
        "views/product_product.xml",
        "views/product_template.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
