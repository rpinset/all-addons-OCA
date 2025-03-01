# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestDocumentPageFollowers(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.user_1 = self.env["res.users"].create(
            {
                "name": "Test User 1",
                "login": "test_user_1",
                "email": "user1@test.com",
            }
        )

        self.user_2 = self.env["res.users"].create(
            {
                "name": "Test User 2",
                "login": "test_user_2",
                "email": "user2@test.com",
            }
        )

        self.category = self.env["document.page"].create(
            {
                "name": "Test Category",
                "type": "category",
            }
        )

        self.content_page = self.env["document.page"].create(
            {
                "name": "Test Content Page",
                "type": "content",
                "parent_id": self.category.id,
            }
        )

    def test_auto_subscribe_new_page(self):
        """When creating a page in a category with followers, they are subscribed"""

        self.category.message_subscribe(
            partner_ids=[self.user_1.partner_id.id, self.user_2.partner_id.id]
        )

        new_page = self.env["document.page"].create(
            {
                "name": "New Auto-Subscribed Page",
                "type": "content",
                "parent_id": self.category.id,
            }
        )

        followers = new_page.message_partner_ids.ids

        self.assertIn(self.user_1.partner_id.id, followers)
        self.assertIn(self.user_2.partner_id.id, followers)

    def test_follow_category_subscribes_documents(self):
        """Follow a category should subscribe to its existing pages"""
        self.category.message_subscribe([self.user_1.partner_id.id])

        self.assertIn(
            self.user_1.partner_id.id,
            self.content_page.parent_id.message_partner_ids.ids,
        )

    def test_unfollow_category_unsubscribes_documents(self):
        """Unfollowing a category should unsubscribe from its existing pages"""
        self.category.message_subscribe([self.user_1.partner_id.id])
        self.category.message_unsubscribe([self.user_1.partner_id.id])

        self.assertNotIn(
            self.user_1.partner_id.id,
            self.content_page.parent_id.message_partner_ids.ids,
        )

    def test_no_auto_subscribe_without_category(self):
        """Pages without a category should not have automatic subscriptions"""
        new_page = self.env["document.page"].create(
            {"name": "Orphan Page", "type": "content"}
        )

        self.assertFalse(new_page.message_partner_ids)
