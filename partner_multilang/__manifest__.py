{
    "name": "Partner Multilang",
    "version": "18.0.3.0.4",
    "license": "LGPL-3",
    "category": "Localization",
    "author": "Rosen Vladimirov, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "summary": "\n"
    "            Automatic multilingual partner names with intelligent\n"
    "            transliteration and language detection.",
    "external_dependencies": {"python": ["transliterate", "unidecode", "lingua"]},
    "depends": ["base", "contacts"],
    "development_status": "Production/Stable",
    "data": ["views/res_lang_views.xml", "views/res_config_settings_view.xml"],
    "images": ["static/description/banner.png"],
    "demo": [],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "maintainers": ["rosenvladimirov"],
}
