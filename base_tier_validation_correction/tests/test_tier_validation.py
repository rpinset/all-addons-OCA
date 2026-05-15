# Copyright 2018 ForgeFlow S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.orm.model_classes import add_to_registry

from odoo.addons.base_tier_validation.tests.common import CommonTierValidation


class TierTierValidation(CommonTierValidation):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .tier_validation_tester import TierValidationTester

        add_to_registry(cls.registry, TierValidationTester)
        cls.registry._setup_models__(cls.env.cr, ["tier.validation.tester"])
        cls.registry.init_models(
            cls.env.cr,
            ["tier.validation.tester"],
            {"models_to_check": True},
        )

    def setUp(self):
        super().setUp()
        self.test_record.name = "test"

    def test_01_tier_correction(self):
        """With the document in validation,
        - User click on Change Reviewer to creat new correction
        - Change the reviewer to user 2, test that user 2 need_validation
        - Revert to user 1, test that now user 1 need validation
        - Click on Change Review link from the document again, then view the corrections
        """
        # User 2, request validation
        doc_user2 = self.test_record.with_user(self.test_user_2.id)
        reviews = doc_user2.request_validation()
        self.assertEqual(reviews.status, "pending")
        self.assertFalse(doc_user2.can_review)
        # User 1, is the reviewer as specified in the tier.definition
        doc_user1 = self.test_record.with_user(self.test_user_1.id)
        doc_user1.invalidate_recordset()
        self.assertTrue(doc_user1.can_review)
        # Change Reviewer from user 1 -> user 2
        ctx = {"active_id": doc_user1.id, "active_model": doc_user1._name}
        res = doc_user1.with_context(**ctx).view_tier_correction()
        self.assertFalse(res["domain"])  # No existing correction, create new
        correction = self.env["tier.correction"].create(
            {
                "name": res["context"].get("default_name"),
                "search_name": res["context"].get("default_search_name"),
                "model_id": res["context"].get("default_model_id"),
                "correction_type": res["context"].get("default_correction_type"),
                "new_reviewer_ids": [Command.set(self.test_user_2.ids)],
                "old_reviewer_ids": [Command.set(self.test_user_1.ids)],
            }
        )
        # Only on state = 'prepare', to allow correction
        with self.assertRaises(ValidationError):
            correction.do_correct()
        # Test cancel -> draft
        correction.action_cancel()
        self.assertEqual(correction.state, "cancel")
        correction.action_draft()
        self.assertEqual(correction.state, "draft")
        # Test view scheduled action
        action = correction.view_scheduled_action()
        self.assertEqual(action["name"], "Scheduled Actions")
        #  Continue
        correction.action_prepare()
        self.assertEqual(correction.state, "prepare")
        self.assertTrue(correction.reference)
        with self.assertRaises(ValidationError):
            correction.do_revert()
        item = correction.item_ids[0]
        self.assertEqual(item.resource_ref, self.test_record)
        self.assertEqual(item.new_reviewer_ids, correction.new_reviewer_ids)
        # View affected tier.reviews
        AffectedReview = self.env["affected.tier.reviews"]
        reviews = AffectedReview.with_context(active_id=item.id)._default_review_ids()
        self.assertTrue(reviews)
        # Make correction, now user 2 can review
        correction.action_done()
        doc_user2.invalidate_recordset()
        self.assertTrue(doc_user2.can_review)
        doc_user1.invalidate_recordset()
        self.assertFalse(doc_user1.can_review)
        # Make reversion, now user 1 can review
        correction.action_revert()
        doc_user1.invalidate_recordset()
        self.assertTrue(doc_user1.can_review)
        doc_user2.invalidate_recordset()
        self.assertFalse(doc_user2.can_review)
        # From the document, view tier correction once again
        res = doc_user1.with_context(**ctx).view_tier_correction()
        self.assertEqual(res["domain"][0][2], [correction.id])

    def test_01_tier_correction_by_scheduler(self):
        """With the document in validation,
        - User click on Change Reviewer to creat new correction
        - Setup Scheduled Correction Date and Scheduled Revert, test date constraints
        - Run scheduler which change reviewer to user 2, test user 2 need_validation
        - Run scheduler which revert to user 1, test user 1 need validation
        """
        # User 2, request validation
        doc_user2 = self.test_record.with_user(self.test_user_2.id)
        reviews = doc_user2.request_validation()
        self.assertEqual(reviews.status, "pending")
        self.assertFalse(doc_user2.can_review)
        # User 1, is the reviewer as specified in the tier.definition
        doc_user1 = self.test_record.with_user(self.test_user_1.id)
        doc_user1.invalidate_recordset()
        self.assertTrue(doc_user1.can_review)
        # Change Reviewer from user 1 -> user 2
        ctx = {"active_id": doc_user1.id, "active_model": doc_user1._name}
        res = doc_user1.with_context(**ctx).view_tier_correction()
        self.assertFalse(res["domain"])  # No existing correction, create new
        correction = self.env["tier.correction"].create(
            {
                "name": res["context"].get("default_name"),
                "search_name": res["context"].get("default_search_name"),
                "model_id": res["context"].get("default_model_id"),
                "correction_type": res["context"].get("default_correction_type"),
                "new_reviewer_ids": [Command.set(self.test_user_2.ids)],
            }
        )
        # Run Schedulder, to correct
        correction.date_schedule_correct = fields.Datetime.now()
        correction.action_prepare()
        self.assertEqual(correction.state, "prepare")
        self.env["tier.correction"]._tier_correction_auto_run()
        self.assertTrue(doc_user2.can_review)
        self.assertFalse(doc_user1.can_review)
        # Run Schedulder, to revert
        with self.assertRaises(ValidationError):
            correction.date_schedule_revert = fields.Datetime.now() - timedelta(days=1)
        correction.date_schedule_revert = fields.Datetime.now()
        self.assertEqual(correction.state, "done")
        self.env["tier.correction"]._tier_correction_auto_run()
        self.assertTrue(doc_user1.can_review)
        self.assertFalse(doc_user2.can_review)
