{
    "name": "Shopify Connector Website Sale",
    "summary": "Synchronize Shopify product media with eCommerce extra product media",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "author": "Sawir Studio, ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/connector-shopify",
    "license": "AGPL-3",
    "depends": ["shopify_connector", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "security/shopify_security.xml",
        "views/shopify_product_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
