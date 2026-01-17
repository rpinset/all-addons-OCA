# Copyright 2025 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Allergen",
    "summary": "Add allergen information to products",
    "version": "18.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "data/allergen_data.xml",
        "views/allergen_allergen_views.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "report/product_product_templates.xml",
    ],
    "installable": True,
}
