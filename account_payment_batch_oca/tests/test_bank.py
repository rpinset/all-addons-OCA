# © 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestBank(TransactionCase):
    def test_bank(self):
        bank = self.env["res.bank"].create(
            {
                "name": "Qonto",
                "bic": "QNTOFRP1XXX",
            }
        )
        with self.assertRaises(ValidationError):
            bank.bic = "TEST"
