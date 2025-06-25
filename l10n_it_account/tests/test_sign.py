# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestSign(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_model = cls.env["account.account"]
        cls.prepayment_type = cls.env.ref("account.data_account_type_prepayments")
        cls.prepayment_account = cls.account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.prepayment_type.id,
                ),
            ],
            limit=1,
        )

    def test_prepayments_account(self):
        """Prepayments are positive."""
        prepayment_account = self.prepayment_account
        self.assertEqual(prepayment_account.user_type_id.account_balance_sign, 1)
