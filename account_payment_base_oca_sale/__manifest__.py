# Copyright 2014-2016 Akretion France (https://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Account Payment Base OCA - Sale",
    "version": "18.0.2.0.0",
    "category": "Banking addons",
    "license": "AGPL-3",
    "summary": "Adds payment method on sale orders",
    "author": "Akretion, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "depends": ["sale", "account_payment_base_oca"],
    "data": [
        "views/sale_order.xml",
        "views/sale_report.xml",
        "views/sale_report_templates.xml",
    ],
    "auto_install": True,
}
