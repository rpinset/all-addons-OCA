from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

mail_server_config = """
[outgoing_mail]
smtp_host = smtp.myserver.com
smtp_port = 587
smtp_user =
smtp_pass =
smtp_encryption = ssl

[outgoing_mail.mail_server1]
smtp_user = user1
smtp_pass = password1

[outgoing_mail.mail_server2]
smtp_user = user2
smtp_pass = password2
"""


class TestMailServerEnvironment(ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailServer = cls.env["ir.mail_server"]
        cls.mail_server1 = cls.mailServer.create({"name": "mail_server1"})
        cls.mail_server2 = cls.mailServer.create({"name": "mail_server2"})

    def test_mail_server_search_smtp_user(self):
        with self.load_config(public=mail_server_config):
            # Test basic properties
            self.assertEqual(self.mail_server1.smtp_user, "user1")
            self.assertEqual(self.mail_server2.smtp_user, "user2")

            # Test smtp_user search method
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "=", "user1")]),
            )
            self.assertNotIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "!=", "user1")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "=", "user2")]),
            )
            self.assertNotIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "!=", "user2")]),
            )
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_user", "ilike", "user")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_user", "ilike", "user")]),
            )

    def test_mail_server_search_smtp_host(self):
        with self.load_config(public=mail_server_config):
            # Test basic properties
            self.assertEqual(self.mail_server1.smtp_host, "smtp.myserver.com")
            self.assertEqual(self.mail_server2.smtp_host, "smtp.myserver.com")

            # Test smtp_user search method
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "=", "smtp.myserver.com")]
                ),
            )
            self.assertNotIn(
                self.mail_server1,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "!=", "smtp.myserver.com")]
                ),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "=", "smtp.myserver.com")]
                ),
            )
            self.assertNotIn(
                self.mail_server2,
                self.env["ir.mail_server"].search(
                    [("smtp_host", "!=", "smtp.myserver.com")]
                ),
            )
            self.assertIn(
                self.mail_server1,
                self.env["ir.mail_server"].search([("smtp_host", "ilike", "myserver")]),
            )
            self.assertIn(
                self.mail_server2,
                self.env["ir.mail_server"].search([("smtp_host", "ilike", "myserver")]),
            )
