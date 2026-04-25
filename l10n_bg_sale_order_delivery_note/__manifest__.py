# Copyright 2023 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Bulgarian Sale Order Delivery Note",
    "version": "18.0.1.0.0",
    "category": "Sales/Bulgaria",
    "summary": "Generate Accepted Delivery Report for Bulgarian Sale Orders",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["sale", "l10n_bg_report_theme"],
    "data": ["report/ir_action_report_templates.xml", "report/ir_actions_report.xml"],
    "demo": [],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
    "development_status": "Beta",
    "tags": ["localization", "sales", "bulgaria", "delivery", "report"],
    "maintainers": ["rosenvladimirov"],
    "images": ["static/description/banner.png"],
}
