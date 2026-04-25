# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Batch - Tier Validation",
    "summary": "Tier validation process on payment/debit orders",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "category": "Banking addons",
    "author": "Escodoo,Odoo Community Association (OCA)",
    "maintainers": ["marcelsavegnago"],
    "development_status": "Mature",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "depends": ["account_payment_batch_oca", "base_tier_validation"],
    "data": [
        "views/account_payment_order.xml",
    ],
    "installable": True,
}
