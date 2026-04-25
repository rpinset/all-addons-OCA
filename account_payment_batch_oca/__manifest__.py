# © 2009 EduSense BV (<http://www.edusense.nl>)
# © 2011-2013 Therp BV (<https://therp.nl>)
# © 2013-2014 ACSONE SA (<https://acsone.eu>).
# © 2016 Akretion (<https://www.akretion.com>).
# © 2016 Aselcis (<https://www.aselcis.com>).
# © 2014-2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Account Payment Batch OCA",
    "summary": "Add payment orders and debit orders",
    "version": "18.0.3.4.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, "
    "Therp BV, "
    "Tecnativa, "
    "Akretion, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment-alternative",
    "development_status": "Mature",
    "category": "Banking addons",
    "depends": [
        "account_payment_base_oca",
        "base_iban",
    ],
    "excludes": ["account_payment_order"],
    "data": [
        "views/account_payment_method.xml",
        "security/payment_security.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "wizard/account_payment_line_create_view.xml",
        "views/account_payment_method_line.xml",
        "views/account_payment.xml",
        "views/account_payment_lot.xml",
        "views/account_payment_order.xml",
        "views/account_payment_line.xml",
        "views/account_move.xml",
        "reports/account_payment_order.xml",
        "reports/ir_actions_report.xml",
        "data/payment_seq.xml",
    ],
    "installable": True,
}
