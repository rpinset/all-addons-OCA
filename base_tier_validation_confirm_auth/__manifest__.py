# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Tier Validation Confirm Auth",
    "summary": "Authentication confirmation for base tiers.",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/server-ux",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base_tier_validation"],
    "data": [
        "views/tier_definition_view.xml",
    ],
    "application": False,
    "installable": True,
}
