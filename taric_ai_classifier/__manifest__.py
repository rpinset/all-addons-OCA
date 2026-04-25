{
    "name": "AI TARIC & INTRASTAT Classifier",
    "version": "18.0.1.0.3",
    "category": "Accounting/Localizations",
    "summary": (
        "AI-powered automatic TARIC and INTRASTAT code classification for " "products"
    ),
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "license": "LGPL-3",
    "depends": ["base", "product", "stock", "stock_delivery", "account"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/taric_code_views.xml",
        "views/res_config_settings_views.xml",
        "wizard/batch_classify_wizard_views.xml",
    ],
    "demo": [],
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "maintainers": ["rosenvladimirov"],
}
