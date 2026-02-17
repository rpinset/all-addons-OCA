# Copyright 2025 Tecnativa - Víctor Martínez
# Copyright 2025 Tecnativa - David Bañón
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo import Command
from odoo.tests import new_test_user, tagged, users

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestAnnouncement(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_announcement = cls.env["announcement"].create(
            {
                "name": "Test announcement",
                "content": "<p>Test content for test announcement</p>",
                "is_general_announcement": True,
                "notification_date": datetime.now() + timedelta(days=-1),
                "notification_expiry_date": datetime.now() + timedelta(days=+1),
                "active": True,
            }
        )
        cls.expired_announcement = cls.env["announcement"].create(
            {
                "name": "Test expired announcement",
                "content": "<p>Its gone</p>",
                "is_general_announcement": True,
                "notification_date": datetime.now() + timedelta(days=-2),
                "notification_expiry_date": datetime.now() + timedelta(days=-1),
                "active": True,
            }
        )
        cls.user = new_test_user(cls.env, login="test-user")
        cls.user_system = new_test_user(
            cls.env, login="test-user-system", groups="base.group_system"
        )
        cls.admin_announcement = cls.env["announcement"].create(
            {
                "name": "Test admin only announcement",
                "content": "<p>Test content for admins only</p>",
                "announcement_type": "user_group",
                "user_group_ids": cls.env.ref("base.group_system"),
                "notification_date": datetime.now() + timedelta(days=-1),
                "notification_expiry_date": datetime.now() + timedelta(days=+1),
                "active": True,
            }
        )
        cls.custom_announcement = cls.env["announcement"].create(
            {
                "name": "Test custom only announcement",
                "content": "<p>Test content for custom users</p>",
                "announcement_type": "specific_users",
                "specific_user_ids": [
                    Command.link(cls.user.id),
                    Command.link(cls.user_system.id),
                ],
                "notification_date": datetime.now() + timedelta(days=-1),
                "notification_expiry_date": datetime.now() + timedelta(days=+1),
                "active": True,
            }
        )
        cls.test_group = cls.env["res.groups"].create(
            {"name": "Test Group for Exclusion", "users": [Command.link(cls.user.id)]}
        )

    @users("test-user-system")
    def test_announcements_user_system(self):
        res = self.env.user.get_announcements()
        announcement_ids = [announcement["id"] for announcement in res["data"]]
        self.assertIn(self.general_announcement.id, announcement_ids)
        self.assertIn(self.admin_announcement.id, announcement_ids)
        self.assertIn(self.custom_announcement.id, announcement_ids)
        self.assertNotIn(self.expired_announcement.id, announcement_ids)

    @users("test-user")
    def test_announcements_user(self):
        res = self.env.user.get_announcements()
        announcement_ids = [announcement["id"] for announcement in res["data"]]
        self.assertIn(self.general_announcement.id, announcement_ids)
        self.assertIn(self.custom_announcement.id, announcement_ids)
        self.assertNotIn(self.admin_announcement.id, announcement_ids)
        self.assertNotIn(self.expired_announcement.id, announcement_ids)

    def test_custom_anouncement_write(self):
        self.assertIn(self.custom_announcement, self.user.unread_announcement_ids)
        self.custom_announcement.write(
            {"specific_user_ids": [Command.unlink(self.user.id)]}
        )
        self.assertNotIn(self.custom_announcement, self.user.unread_announcement_ids)
        self.custom_announcement.write(
            {"specific_user_ids": [Command.link(self.user.id)]}
        )
        self.assertIn(self.custom_announcement, self.user.unread_announcement_ids)

    def test_excluded_user(self):
        """If a general announcement has excluded users, those users should not see it."""
        self.env.invalidate_all()
        self.general_announcement._compute_allowed_user_ids()
        self.assertIn(self.user, self.general_announcement.allowed_user_ids)

        self.general_announcement.write(
            {
                "excluded_users_ids": [Command.link(self.user.id)],
            }
        )

        self.env.invalidate_all()
        self.general_announcement._compute_allowed_user_ids()
        self.assertNotIn(self.user, self.general_announcement.allowed_user_ids)

    def test_excluded_group(self):
        """If a general announcement has excluded groups, users in those groups
        should not see it."""
        self.env.invalidate_all()
        self.general_announcement._compute_allowed_user_ids()
        self.assertIn(self.user, self.general_announcement.allowed_user_ids)

        self.general_announcement.write(
            {
                "excluded_groups_ids": [Command.link(self.test_group.id)],
            }
        )

        self.env.invalidate_all()
        self.general_announcement._compute_allowed_user_ids()
        self.assertNotIn(self.user, self.general_announcement.allowed_user_ids)
