# Copyright 2016-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestMandate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.company = cls.env.ref("base.main_company")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner SDD",
                "company_id": cls.company.id,
            }
        )
        cls.partner_bank = cls.env["res.partner.bank"].create(
            {
                "acc_number": "FR451111 9999 8888 5555 9999 421",
                "partner_id": cls.partner.id,
            }
        )
        cls.mandate = cls.env["account.banking.mandate"].create(
            {
                "partner_id": cls.partner.id,
                "partner_bank_id": cls.partner_bank.id,
                "format": "sepa_core",
                "type": "oneoff",
                "signature_date": "2015-01-01",
                "company_id": cls.company.id,
            }
        )
        cls.partner_bank_non_iban = cls.env["res.partner.bank"].create(
            {
                "acc_number": "FR42NOTANIBAN",
                "partner_id": cls.partner.id,
            }
        )

    def test_contrains(self):
        with self.assertRaises(ValidationError):
            self.env["account.banking.mandate"].create(
                {
                    "partner_id": self.partner.id,
                    "partner_bank_id": self.partner_bank_non_iban.id,
                    "format": "sepa_core",
                }
            )

    def test_expire(self):
        self.mandate.signature_date = fields.Date.today() + relativedelta(months=-50)
        self.mandate.validate()
        self.assertEqual(self.mandate.state, "valid")
        self.env["account.banking.mandate"]._sdd_mandate_set_state_to_expired()
        self.assertEqual(self.mandate.state, "expired")
