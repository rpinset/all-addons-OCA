from odoo.tests import TransactionCase

from odoo.addons.openupgrade_framework import openupgrade_test


@openupgrade_test
class TestBaseMigration(TransactionCase):
    def test_new_message_separator(self):
        """
        Test that discuss channel members get correct new_message_separator
        """
        channel_member_demo = self.env["discuss.channel.member"].search(
            [
                ("partner_id", "=", self.env.ref("base.user_demo").partner_id.id),
                ("channel_id", "=", self.env.ref("mail.channel_all_employees").id),
            ]
        )
        message = self.env["mail.message"].search(
            [
                (
                    "subject",
                    "=",
                    "This message should become demo's new_message_separator",
                ),
            ]
        )
        self.assertTrue(message)
        self.assertEqual(channel_member_demo.new_message_separator, message.id)
