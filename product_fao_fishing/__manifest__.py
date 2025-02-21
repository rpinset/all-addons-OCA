# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product FAO Fishing",
    "summary": "Set fishing areas and capture technology",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Fishing",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product", "product_attribute_value_avoid_auto_fill"],
    "data": [
        "data/product_fao_fishing_data.xml",
        "data/product_fao_fishing_technique_data.xml",
        "views/product_attribute_views.xml",
    ],
    "maintainers": ["CarlosRoca13"],
}
