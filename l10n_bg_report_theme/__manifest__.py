# Copyright 2023 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Bulgaria - Report Theme Sections",
    "summary": (
        "Professional report theme with modular section-based layout for Bulgarian "
        "business documents."
    ),
    "version": "18.0.5.0.4",
    "development_status": "Production/Stable",
    "license": "LGPL-3",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["web", "sale", "account", "stock", "purchase", "l10n_bg_config"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/report_templates.xml",
        "data/report_layout.xml",
        "data/report_paperformat_data.xml",
        "views/res_company_views.xml",
        "views/base_document_layout_views.xml",
        "views/ir_action_report_templates.xml",
        "views/report_invoice.xml",
        "views/purchase_order_templates.xml",
        "views/purchase_quotation_templates.xml",
    ],
    "external_dependencies": {"python": ["webcolors"]},
    "demo": [],
    "images": ["static/description/banner.png"],
    "assets": {
        "web.report_assets_common": [
            "l10n_bg_report_theme/static/src/webclient/actions/sffont.scss",
            "l10n_bg_report_theme/static/src/webclient/actions/reports/report_variable_fonts.scss",
        ]
    },
    "tags": ["localization", "accounting", "bulgaria", "configuration"],
    "odoo_version": "18.0",
    "python_version": ">=3.11",
    "maintainers": ["rosenvladimirov"],
}
