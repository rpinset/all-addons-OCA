# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPaymentPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.payment_provider_none = cls.env["payment.provider"].create(
            {
                "name": "Dummy Provider",
                "code": "none",
                "state": "test",
                "is_published": True,
                "allow_tokenization": True,
                "filter_mode": False,
            }
        )
        cls.payment_provider_global = cls.env["payment.provider"].create(
            {
                "name": "Dummy Provider",
                "code": "none",
                "state": "test",
                "is_published": True,
                "allow_tokenization": True,
                "filter_mode": "global",
            }
        )
        cls.payment_provider_include = cls.env["payment.provider"].create(
            {
                "name": "Dummy Provider",
                "code": "none",
                "state": "test",
                "is_published": True,
                "allow_tokenization": True,
                "filter_mode": "include",
            }
        )
        cls.payment_provider_exclude = cls.env["payment.provider"].create(
            {
                "name": "Dummy Provider",
                "code": "none",
                "state": "test",
                "is_published": True,
                "allow_tokenization": True,
                "filter_mode": "exclude",
            }
        )

    def test_partner(self):
        providers = self.env["payment.provider"]._get_compatible_providers(
            self.env.company.id, self.partner.id, 5
        )
        self.assertNotIn(self.payment_provider_include, providers)
        self.assertIn(self.payment_provider_exclude, providers)
        self.assertIn(self.payment_provider_global, providers)
        self.assertIn(self.payment_provider_none, providers)
        self.payment_provider_include.partner_ids = self.partner
        providers = self.env["payment.provider"]._get_compatible_providers(
            self.env.company.id, self.partner.id, 5
        )
        self.assertIn(self.payment_provider_include, providers)
        self.assertIn(self.payment_provider_exclude, providers)
        self.assertIn(self.payment_provider_global, providers)
        self.assertIn(self.payment_provider_none, providers)
        self.payment_provider_exclude.partner_ids = self.partner
        providers = self.env["payment.provider"]._get_compatible_providers(
            self.env.company.id, self.partner.id, 5
        )
        self.assertIn(self.payment_provider_include, providers)
        self.assertNotIn(self.payment_provider_exclude, providers)
        self.assertIn(self.payment_provider_global, providers)
        self.assertIn(self.payment_provider_none, providers)
