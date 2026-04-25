# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Crowdfunding",
    "summary": "Turn Odoo into a platform for crowdfunding",
    "version": "14.0.1.3.1",
    "development_status": "Alpha",
    "category": "Crowdfunding",
    "website": "https://github.com/OCA/crowdfunding",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "account_payment",
        "onchange_helper",
        "website",
    ],
    "data": [
        "data/product_product.xml",
        "data/website_menu.xml",
        "security/crowdfunding_security.xml",
        "security/ir.model.access.csv",
        "templates/assets.xml",
        "templates/crowdfunding_challenge.xml",
        "templates/payment.xml",
        "views/account_move.xml",
        "views/crowdfunding_challenge.xml",
        "views/payment_transaction.xml",
        "views/res_config_settings.xml",
        "views/menu.xml",
        "wizards/crowdfunding_invoicing_wizard.xml",
    ],
    "demo": [
        "demo/crowdfunding_challenge.xml",
    ],
}
