{
    "name": "Bulgarian Company Registry Integration",
    "version": "18.0.2.0.1",
    "category": "Localization",
    "summary": (
        "Real-time integration with Bulgarian Trade Registry "
        "(portal.registryagency.bg)"
    ),
    "author": "Odoo Community Association (OCA), Rosen Vladimirov",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "license": "LGPL-3",
    "depends": ["base", "contacts", "l10n_bg_config", "l10n_bg_city"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_actions_server.xml",
        "views/res_partner_views.xml",
        "wizard/bg_company_search_wizard_views.xml",
    ],
    "external_dependencies": {"python": ["requests"]},
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "maintainers": ["rosenvladimirov"],
}
