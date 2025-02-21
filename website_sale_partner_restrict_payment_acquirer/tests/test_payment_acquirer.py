# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPaymentAcquirer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_partner_gemini = cls.env.ref("base.res_partner_3")
        cls.acquirer_obj = cls.env["payment.acquirer"]
        cls.acquirers_list = cls.acquirer_obj.search(
            [("state", "in", ["enabled", "test"])]
        )
        cls.wire_transfer = cls.env.ref("payment.payment_acquirer_transfer")
        cls.website = cls.env.ref("website.default_website")
        cls.company = cls.env.ref("base.main_company")

    def _get_compatible_acquirers(self, partner):
        self.env.user.partner_id = partner
        return self.acquirer_obj._get_compatible_acquirers(
            company_id=self.company.id,
            partner_id=partner.id,
            website_id=self.website.id,
        )

    def test_get_compatible_acquirers_no_restriction(self):
        acquirers = self._get_compatible_acquirers(self.res_partner_gemini)
        self.assertEqual(acquirers, self.acquirers_list)

    def test_get_compatible_acquirers_with_partner_restriction_order(self):
        self.res_partner_gemini.write(
            {"allowed_acquirer_ids": [(4, self.wire_transfer.id)]}
        )
        acquirers = self._get_compatible_acquirers(
            self.res_partner_gemini,
        )
        self.assertEqual(acquirers, self.wire_transfer)
