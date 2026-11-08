# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import HttpCaseWithUserPortal

SIGNATURE = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


@tagged("post_install", "-at_install")
class TestSaleTierValidationPortal(HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reviewer = new_test_user(
            cls.env,
            login="portal_test_reviewer",
            groups="sales_team.group_sale_salesman_all_leads",
        )
        so_model = cls.env.ref("sale.model_sale_order")
        cls.env["tier.definition"].create(
            {
                "model_id": so_model.id,
                "review_type": "individual",
                "reviewer_id": cls.reviewer.id,
            }
        )
        # Without it, signing is refused while the quotation is not confirmed
        cls.env["tier.validation.exception"].create(
            {
                "model_id": so_model.id,
                "field_ids": [
                    Command.set(
                        so_model.field_id.filtered(
                            lambda f: f.name in ("signature", "signed_by", "signed_on")
                        ).ids
                    )
                ],
            }
        )
        product = cls.env["product.product"].create(
            {"name": "Product for test", "list_price": 100.0}
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_portal.id,
                "require_signature": True,
                "require_payment": False,
                "order_line": [Command.create({"product_id": product.id})],
            }
        )
        cls.order.action_quotation_sent()
        cls.order.request_validation()

    def test_portal_user_cannot_read_reviews(self):
        self.assertTrue(self.order.review_ids)
        portal_env = self.env(user=self.user_portal)
        for model in ("tier.review", "tier.definition"):
            self.assertFalse(portal_env[model].has_access("read"))

    def test_portal_flow_with_reviews(self):
        self.authenticate(self.user_portal.login, self.user_portal.login)
        response = self.url_open(f"/my/orders/{self.order.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.order.name, response.text)
        self.make_jsonrpc_request(
            "/mail/message/post",
            {
                "thread_model": "sale.order",
                "thread_id": self.order.id,
                "post_data": {"body": "Any news on the approval?"},
            },
        )
        self.order.with_user(self.reviewer).validate_tier()
        self.assertEqual(self.order.validation_status, "validated")
        self.make_jsonrpc_request(
            f"/my/orders/{self.order.id}/accept",
            {"name": "Joel Willis", "signature": SIGNATURE},
        )
        self.assertEqual(self.order.state, "sale")

    def test_public_flow_with_reviews(self):
        token = self.order._portal_ensure_token()
        response = self.url_open(f"/my/orders/{self.order.id}?access_token={token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.order.name, response.text)
        self.order.with_user(self.reviewer).validate_tier()
        self.make_jsonrpc_request(
            f"/my/orders/{self.order.id}/accept?access_token={token}",
            {"name": "Joel Willis", "signature": SIGNATURE},
        )
        self.assertEqual(self.order.state, "sale")
