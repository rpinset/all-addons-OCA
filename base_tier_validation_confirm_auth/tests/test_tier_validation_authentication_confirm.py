# Copyright 2026 ForgeFlow S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from unittest.mock import MagicMock, patch

from odoo.tests import Form, tagged

from odoo.addons.base_tier_validation.tests.common import CommonTierValidation


@tagged("post_install", "-at_install")
class TierTierValidationAuthenticationConfirm(CommonTierValidation):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_01_authentication_confirmation_and_comment(self):
        # Set user password for validation
        self.test_user_1.password = "test_user_1"

        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})

        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "has_comment": True,
                "require_authentication": True,
            }
        )
        # Request validation
        review = test_record.with_user(self.test_user_2.id).request_validation()
        self.assertTrue(review)

        # Let _compute_can_review assign status 'pending' instead of waiting
        review.flush_recordset()
        record = test_record.with_user(self.test_user_1.id)
        res = record.validate_tier()
        ctx = res.get("context")
        wizard = Form(self.env["comment.wizard"].with_context(**ctx))
        wizard.comment = "Test Comment"
        wiz = wizard.save()

        # Mock requests to avoid errors outside HTTP request
        with patch(
            "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
            MagicMock(),
        ):
            res = wiz.add_comment()

        self.assertEqual(res["res_model"], "res.users.identitycheck")
        identity_wiz_id = res["res_id"]
        identity_wiz = (
            self.env["res.users.identitycheck"]
            .sudo()
            .browse(identity_wiz_id)
            .with_user(self.test_user_1)
        )
        identity_wiz.sudo().write({"password": "test_user_1"})

        # Mock requests to avoid errors outside HTTP request
        with (
            patch("odoo.addons.base.models.res_users.request", MagicMock()),
            patch(
                "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
                MagicMock(),
            ),
        ):
            identity_wiz.sudo().run_check()

        self.assertTrue(review.status == "approved")
        self.assertTrue(review.done_by == self.test_user_1)
        self.assertTrue(review.comment == "Test Comment")

    def test_02_authentication_confirmation_without_comment(self):
        # Set user password for validation
        self.test_user_1.password = "test_user_1"

        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})

        # Create tier definition with no comment + require authentication
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "has_comment": False,
                "require_authentication": True,
            }
        )

        # Request validation
        review = test_record.with_user(self.test_user_2).request_validation()
        self.assertTrue(review)
        record = test_record.with_user(self.test_user_1)

        # Mock requests to avoid errors outside HTTP request
        with patch(
            "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
            MagicMock(),
        ):
            res = record.validate_tier()

        # Identity confirmation wizard
        self.assertEqual(res["res_model"], "res.users.identitycheck")
        identity_wiz_id = res["res_id"]
        identity_wiz = (
            self.env["res.users.identitycheck"]
            .sudo()
            .browse(identity_wiz_id)
            .with_user(self.test_user_1)
        )
        identity_wiz.sudo().write({"password": "test_user_1"})

        # Mock requests to avoid errors outside HTTP request
        with (
            patch("odoo.addons.base.models.res_users.request", MagicMock()),
            patch(
                "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
                MagicMock(),
            ),
        ):
            identity_wiz.sudo().run_check()

        self.assertTrue(review.status == "approved")
        self.assertTrue(review.done_by == self.test_user_1)

    def test_03_authentication_confirmation_reject_with_comment(self):
        # Set user password for validation
        self.test_user_1.password = "test_user_1"

        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})

        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "has_comment": True,
                "require_authentication": True,
            }
        )
        # Request validation
        review = test_record.with_user(self.test_user_2.id).request_validation()
        self.assertTrue(review)

        # Let _compute_can_review assign status 'pending' instead of waiting
        review.flush_recordset()
        record = test_record.with_user(self.test_user_1.id)
        res = record.reject_tier()
        ctx = res.get("context")
        wizard = Form(self.env["comment.wizard"].with_context(**ctx))
        wizard.comment = "Test Comment"
        wiz = wizard.save()

        # Mock requests to avoid errors outside HTTP request
        with patch(
            "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
            MagicMock(),
        ):
            res = wiz.add_comment()

        # Identity confirmation wizard
        self.assertEqual(res["res_model"], "res.users.identitycheck")
        identity_wiz_id = res["res_id"]
        identity_wiz = (
            self.env["res.users.identitycheck"]
            .sudo()
            .browse(identity_wiz_id)
            .with_user(self.test_user_1)
        )
        identity_wiz.sudo().write({"password": "test_user_1"})

        # Mock requests to avoid errors outside HTTP request
        with (
            patch("odoo.addons.base.models.res_users.request", MagicMock()),
            patch(
                "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
                MagicMock(),
            ),
        ):
            identity_wiz.sudo().run_check()

        self.assertTrue(review.status == "rejected")
        self.assertTrue(review.done_by == self.test_user_1)
        self.assertTrue(review.comment == "Test Comment")

    def test_04_authentication_confirmation_reject_without_comment(self):
        # Set user password for validation
        self.test_user_1.password = "test_user_1"

        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})

        # Create tier definition with no comment + require authentication
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "has_comment": False,
                "require_authentication": True,
            }
        )

        # Request validation
        review = test_record.with_user(self.test_user_2).request_validation()
        self.assertTrue(review)
        record = test_record.with_user(self.test_user_1)

        # Mock requests to avoid errors outside HTTP request
        with patch(
            "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
            MagicMock(),
        ):
            res = record.reject_tier()

        # Identity confirmation wizard
        self.assertEqual(res["res_model"], "res.users.identitycheck")
        identity_wiz_id = res["res_id"]
        identity_wiz = (
            self.env["res.users.identitycheck"]
            .sudo()
            .browse(identity_wiz_id)
            .with_user(self.test_user_1)
        )
        identity_wiz.sudo().write({"password": "test_user_1"})

        # Mock requests to avoid errors outside HTTP request
        with (
            patch("odoo.addons.base.models.res_users.request", MagicMock()),
            patch(
                "odoo.addons.base_tier_validation_confirm_auth.models.res_users.request",
                MagicMock(),
            ),
        ):
            identity_wiz.sudo().run_check()

        self.assertTrue(review.status == "rejected")
        self.assertTrue(review.done_by == self.test_user_1)
