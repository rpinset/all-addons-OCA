#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccount(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_model = cls.env["account.account"]

    def test_type_prepayments(self):
        prepayment_account = self.account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_prepayments").id,
                ),
            ],
            limit=1,
        )
        self.assertEqual(
            prepayment_account.financial_statements_report_section, "assets"
        )
