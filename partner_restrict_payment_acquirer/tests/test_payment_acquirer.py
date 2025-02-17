from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPaymentAcquirer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice_test_1 = cls.env.ref("account.1_demo_invoice_followup")
        cls.order_test_1 = cls.env.ref("sale.sale_order_7")
        cls.res_partner_deco = cls.env.ref("base.res_partner_2")
        cls.res_partner_gemini = cls.env.ref("base.res_partner_3")
        cls.acquirers_list = list(
            cls.env["payment.acquirer"].search([("state", "in", ["enabled", "test"])])
        )
        cls.wire_transfer = cls.env.ref("payment.payment_acquirer_transfer")

    def test_get_allowed_acquirers(self):
        payment_acquirer_obj = self.env["payment.acquirer"]
        acquirers = payment_acquirer_obj.get_allowed_acquirers(self.acquirers_list)
        self.assertListEqual(
            acquirers, self.acquirers_list, msg="Acquirers lists must be same"
        )

    def test_get_allowed_acquirers_order(self):
        """This test covers acquirer selection based on partner settings for sale order"""
        payment_acquirer_obj = self.env["payment.acquirer"]

        acquirers = payment_acquirer_obj.get_allowed_acquirers(
            self.acquirers_list, order_id=self.order_test_1.id
        )
        self.assertListEqual(
            acquirers, self.acquirers_list, msg="Acquirers lists must be same"
        )
        customer_acquirers = self.res_partner_gemini.allowed_acquirer_ids
        self.assertFalse(customer_acquirers, msg="Acquirers must be empty")

        self.res_partner_gemini.write(
            {"allowed_acquirer_ids": [(4, self.wire_transfer.id)]}
        )
        customer_acquirers = self.res_partner_gemini.allowed_acquirer_ids
        self.assertEqual(
            customer_acquirers,
            self.wire_transfer,
            msg="Customer acquirers must be contain 'Wire Transfer'",
        )
        acquirers = payment_acquirer_obj.get_allowed_acquirers(
            self.acquirers_list, order_id=self.order_test_1.id
        )
        self.assertEqual(
            acquirers, [self.wire_transfer], msg="Acquirers must be the same"
        )

    def test_get_allowed_acquirers_invoice(self):
        """This test covers acquirer selection based on partner settings for invoice"""
        payment_acquirer_obj = self.env["payment.acquirer"]

        acquirers = payment_acquirer_obj.get_allowed_acquirers(
            self.acquirers_list, invoice_id=self.invoice_test_1.id
        )
        self.assertListEqual(
            acquirers, self.acquirers_list, msg="Acquirers lists must be same"
        )

        customer_acquirers = self.res_partner_deco.allowed_acquirer_ids
        self.assertFalse(customer_acquirers, msg="Acquirers must be empty")

        self.res_partner_deco.write(
            {"allowed_acquirer_ids": [(4, self.wire_transfer.id)]}
        )
        customer_acquirers = self.res_partner_deco.allowed_acquirer_ids
        self.assertEqual(
            customer_acquirers,
            self.wire_transfer,
            msg="Customer acquirers must be contain 'Wire Transfer'",
        )
        acquirers = payment_acquirer_obj.get_allowed_acquirers(
            self.acquirers_list, invoice_id=self.invoice_test_1.id
        )
        self.assertEqual(
            acquirers, [self.wire_transfer], msg="Acquirers must be the same"
        )
