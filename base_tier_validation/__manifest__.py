# Copyright 2017-24 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Tier Validation",
    "summary": "Implement a validation process based on tiers.",
    "version": "19.0.1.0.0",
    "development_status": "Mature",
    "maintainers": ["LoisRForgeFlow"],
    "category": "Tools",
    "website": "https://github.com/OCA/tier-validation",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mail"],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/tier_validation_security.xml",
        # Data
        "data/cron_data.xml",
        "data/mail_data.xml",
        # Views
        "views/tier_definition_view.xml",
        "views/tier_review_view.xml",
        "views/tier_validation_exception_view.xml",
        # Wizards
        "wizard/comment_wizard_view.xml",
        # Templates
        "templates/tier_validation_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "base_tier_validation/static/src/components/**/*",
            "base_tier_validation/static/src/js/**/*",
        ],
    },
}
