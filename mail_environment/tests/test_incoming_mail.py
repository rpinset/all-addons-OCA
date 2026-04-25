# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)


from odoo.addons.server_environment.tests.common import ServerEnvironmentCase

fetchmail_config = """
[incoming_mail.fetchmail1]
server = safe_server
port = 993
server_type = imap
is_ssl = 1
attach = 1
original = 1
user = admin
password = admin
state = done
priority = 1
active = 1

[incoming_mail.fetchmail2]
server = unsafe_server
port = 143
server_type = imap
is_ssl = 0
attach = 1
original = 1
user = admin
password = admin
state = done
priority = 1
active = 1
"""


class TestFetchMailEnvironment(ServerEnvironmentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.FetchmailServer = cls.env["fetchmail.server"]
        cls.fetchmail1 = cls.FetchmailServer.create({"name": "fetchmail1"})
        cls.fetchmail2 = cls.FetchmailServer.create({"name": "fetchmail2"})

    def test_fetchmail_search_is_ssl(self):
        with self.load_config(public=fetchmail_config):
            # Test basic properties
            self.assertTrue(self.fetchmail1.is_ssl)
            self.assertEqual(self.fetchmail1.port, 993)
            self.assertFalse(self.fetchmail2.is_ssl)
            self.assertEqual(self.fetchmail2.port, 143)

            # Test is_ssl search method
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "=", True)]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )
            self.assertNotIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "=", True)]),
            )
            self.assertNotIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", False)]),
            )
            self.assertIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "=", False)]),
            )
            self.assertIn(
                self.fetchmail2,
                self.env["fetchmail.server"].search([("is_ssl", "!=", True)]),
            )

    def test_fetchmail_search_server_type(self):
        with self.load_config(public=fetchmail_config):
            # Test server_type search method
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "=", "imap")]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "!=", "pop3")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "=", "pop3")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "!=", "imap")]),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search(
                    [("server_type", "=ilike", "IMAP")]
                ),
            )
            self.assertIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "ilike", "IM")]),
            )
            self.assertNotIn(
                self.fetchmail1,
                self.env["fetchmail.server"].search([("server_type", "ilike", "POP")]),
            )
