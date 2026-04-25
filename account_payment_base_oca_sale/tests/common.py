# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class CommonTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.bank = cls.env["res.partner.bank"].create(
            {
                "acc_number": "FR66 1234 5678 1212 6363 3636 098",
                "partner_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "test journal",
                "code": "123",
                "type": "bank",
                "company_id": cls.env.ref("base.main_company").id,
                "bank_account_id": cls.bank.id,
            }
        )
        cls.payment_method_line = cls.env["account.payment.method.line"].create(
            {
                "name": "test_mode",
                "payment_method_id": cls.env.ref(
                    "account.account_payment_method_manual_in"
                ).id,
                "bank_account_link": "fixed",
                "journal_id": cls.journal.id,
            }
        )
        cls.payment_method_line_2 = cls.env["account.payment.method.line"].create(
            {
                "name": "test_mode_2",
                "payment_method_id": cls.env.ref(
                    "account.account_payment_method_manual_in"
                ).id,
                "bank_account_link": "fixed",
                "journal_id": cls.journal.id,
            }
        )
        cls.base_partner = cls.env["res.partner"].create(
            {
                "name": "Dummy",
                "email": "dummy@example.com",
                "property_inbound_payment_method_line_id": cls.payment_method_line.id,
            }
        )
        cls.products = {
            "prod_order": cls.env["product.product"].create(
                {
                    "name": "Test consu invoice on order",
                    "type": "consu",
                    "invoice_policy": "order",
                    "list_price": 12.42,
                }
            ),
            "prod_del": cls.env["product.product"].create(
                {
                    "name": "Test consu invoice on delivery",
                    "type": "consu",
                    "invoice_policy": "delivery",
                    "list_price": 13.13,
                }
            ),
            "serv_order": cls.env["product.product"].create(
                {
                    "name": "Test service product order",
                    "type": "service",
                    "invoice_policy": "order",
                    "list_price": 42.12,
                }
            ),
            "serv_del": cls.env["product.product"].create(
                {
                    "name": "Test service product delivery",
                    "type": "service",
                    "invoice_policy": "delivery",
                    "list_price": 12.34,
                }
            ),
        }
