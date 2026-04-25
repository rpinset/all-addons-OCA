# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "VCP Management",
    "summary": """Management for your Version Control Platforms""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "templates/templates.xml",
        "views/vcp_comment.xml",
        "views/vcp_review.xml",
        "views/vcp_request.xml",
        "views/vcp_request_label.xml",
        "views/vcp_repository.xml",
        "views/vcp_repository_branch.xml",
        "views/vcp_branch.xml",
        "views/vcp_platform.xml",
        "views/vcp_organization.xml",
        "views/vcp_user.xml",
        "views/vcp_host.xml",
        "views/vcp_rule.xml",
        "views/vcp_rule_information.xml",
        "views/menu.xml",
        "data/vcp_rule.xml",
    ],
    "demo": [],
    "external_dependencies": {
        "python": ["pathspec"],
        "bin": ["cloc"],
        # special definition used by OCA to install packages
        "deb": ["cloc"],
    },
}
