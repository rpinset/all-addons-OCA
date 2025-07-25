# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestResUsers(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ResPartner = cls.env["res.partner"]
        cls.ResUsers = cls.env["res.users"]

    def test_default_tz(self):

        john = self.ResUsers.create({"name": "John", "login": "john"})
        self.assertEqual(
            john.tz, "Africa/Addis_Ababa", "By default the user has Ethiopia timezone"
        )

    def test_admin_tz(self):

        admin = self.env.ref("base.user_admin")
        self.assertEqual(
            admin.tz,
            "Africa/Addis_Ababa",
            "By default the admin user has Ethiopia timezone",
        )
