# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Tier Review Activity Board",
    "summary": "Dashboard with kanban, list, pivot and graph views over"
    " every pending/approved/rejected tier review, gated by an opt-in"
    " group and per-document ACL.",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "maintainers": ["JasminSForgeFlow"],
    "category": "Tools",
    "website": "https://github.com/OCA/tier-validation",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_tier_validation", "spreadsheet_dashboard"],
    "data": ["security/groups.xml", "views/tier_review_view.xml"],
}
