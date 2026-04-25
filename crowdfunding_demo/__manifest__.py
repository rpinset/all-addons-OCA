# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Crowdfunding (demo data)",
    "summary": "Installs demo data to have crowdfunding up and running on runbot",
    "version": "14.0.1.0.1",
    "development_status": "Alpha",
    "category": "Crowdfunding",
    "website": "https://github.com/OCA/crowdfunding",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "crowdfunding",
        "payment_test",
        "payment_transfer",
        "l10n_ch",
    ],
    "demo": [
        "demo/payment_acquirer.xml",
        "demo/product_product.xml",
        "demo/res_company.xml",
    ],
}
