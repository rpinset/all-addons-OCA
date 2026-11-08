# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import HttpCaseWithUserPortal


@tagged("post_install", "-at_install")
class TestPurchaseTierValidationPortal(HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        reviewer = new_test_user(
            cls.env, login="portal_test_reviewer", groups="purchase.group_purchase_user"
        )
        cls.env["tier.definition"].create(
            {
                "model_id": cls.env.ref("purchase.model_purchase_order").id,
                "review_type": "individual",
                "reviewer_id": reviewer.id,
            }
        )
        product = cls.env["product.product"].create({"name": "Product for test"})
        cls.order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner_portal.id,
                "order_line": [
                    Command.create({"product_id": product.id, "price_unit": 10.0})
                ],
            }
        )
        cls.order.write({"state": "sent"})
        cls.order.request_validation()

    def test_portal_user_cannot_read_reviews(self):
        self.assertTrue(self.order.review_ids)
        portal_env = self.env(user=self.user_portal)
        for model in ("tier.review", "tier.definition"):
            self.assertFalse(portal_env[model].has_access("read"))

    def test_portal_vendor_views_order_under_validation(self):
        self.authenticate(self.user_portal.login, self.user_portal.login)
        for url in (
            f"/my/purchase/{self.order.id}",
            f"/my/purchase/{self.order.id}?report_type=pdf",
        ):
            response = self.url_open(url)
            self.assertEqual(response.status_code, 200)

    def test_public_views_order_under_validation(self):
        token = self.order._portal_ensure_token()
        response = self.url_open(f"/my/purchase/{self.order.id}?access_token={token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.order.name, response.text)
