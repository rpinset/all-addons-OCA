from odoo.tests import TransactionCase

from odoo.addons.openupgrade_framework import openupgrade_test


@openupgrade_test
class TestAccountMigration(TransactionCase):
    def test_sending_data(self):
        """
        Test that me migrate send_and_print_values correctly to sending_data
        """
        moves_with_sending_data = self.env["account.move"].search(
            [
                ("sending_data", "!=", False),
            ]
        )
        self.assertTrue(moves_with_sending_data)
        self.assertEqual(
            moves_with_sending_data[0].sending_data["author_user_id"],
            self.env.user.id,
        )
        self.assertEqual(
            moves_with_sending_data[0].sending_data["author_partner_id"],
            self.env.user.partner_id.id,
        )
