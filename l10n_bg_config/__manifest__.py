# Copyright 2023 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Bulgaria localization Configuration",
    "summary": "\n"
    "        This module allows you to install and configure all\n"
    "        the localization modules related to Bulgaria.",
    "version": "18.0.8.0.5",
    "development_status": "Production/Stable",
    "category": "Localization",
    "license": "LGPL-3",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": [
        "base",
        "account",
        "base_vat",
        "l10n_bg",
        "l10n_bg_ledger",
        "l10n_bg_tariff_code",
    ],
    "external_dependencies": {"python": ["xmltodict"]},
    "data": [
        "data/res_lang_data.xml",
        "security/ir.model.access.csv",
        "wizards/account_account_tag_bulk_edit_wizard.xml",
        "wizards/account_settings_preview_xml_file.xml",
        "wizards/account_chart_template_plugins.xml",
        "views/res_config_view.xml",
        "views/account_account_tag_views.xml",
        "views/partner_view.xml",
        "views/res_company_views.xml",
        "views/account_move_views.xml",
    ],
    "demo": [],
    "images": ["static/description/banner.png"],
    "assets": {"web.assets_backend": ["l10n_bg_config/static/src/**/*"]},
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "auto_install": ["l10n_bg"],
    "tags": ["localization", "accounting", "bulgaria", "configuration"],
    "countries": ["BG"],
    "odoo_version": "18.0",
    "python_version": ">=3.11",
    "maintainers": ["rosenvladimirov"],
}
