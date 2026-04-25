# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Crowdfunding: Public pledges",
    "summary": "Allow users to mark their pledges as public",
    "version": "14.0.1.0.0",
    "development_status": "Alpha",
    "category": "Crowdfunding",
    "website": "https://github.com/OCA/crowdfunding",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "crowdfunding",
    ],
    "data": [
        "templates/crowdfunding_challenge.xml",
        "templates/payment.xml",
        "views/account_move.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/crowdfunding_public_pledge/static/src/scss/crowdfunding_public_pledge.scss",
        ],
    },
}
