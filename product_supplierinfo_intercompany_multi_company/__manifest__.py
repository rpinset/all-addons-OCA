{
    "name": "Product SupplierInfo Intercompany Multi Company",
    "summary": """
    Compatibility of product_multi_company and product_supplierinfo_intercompany""",
    "version": "14.0.1.3.1",
    "category": "Generic Modules/Others",
    "license": "AGPL-3",
    "author": "Ilyas, Ooops404, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/multi-company",
    "depends": [
        "product_supplierinfo_intercompany",
        "product_multi_company",
    ],
    "data": [
        "views/product_supplierinfo_views.xml",
    ],
    "installable": True,
    "auto_install": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
