# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Discount",
    "summary": """Advance management of discount on payments""",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "depends": [
        "account_payment_batch_oca",
    ],
    "data": [
        "views/account_payment_line.xml",
        "wizards/account_payment_line_create.xml",
    ],
    "demo": [],
    "maintainers": ["AnizR"],
}
