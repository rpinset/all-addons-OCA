# Copyright 2018 ForgeFlow S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from datetime import timedelta

from lxml import etree

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
                "document_domain": res["context"].get("default_document_domain"),
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
                "document_domain": res["context"].get("default_document_domain"),
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

    def test_affected_tier_reviews_as_user(self):
        """A correction user can open the affected tier reviews."""
        self.test_record.with_user(self.test_user_2).request_validation()
        user = self.test_user_1
        user.group_ids |= self.env.ref(
            "base_tier_validation_correction.group_tier_correction"
        )
        correction = (
            self.env["tier.correction"]
            .with_user(user)
            .create(
                {
                    "name": "Correction",
                    "model_id": self.tester_model.id,
                    "old_reviewer_ids": [Command.set(self.test_user_1.ids)],
                    "new_reviewer_ids": [Command.set(self.test_user_2.ids)],
                }
            )
        )
        correction.action_prepare()
        item = correction.item_ids[0]
        wizard = (
            self.env["affected.tier.reviews"]
            .with_user(user)
            .with_context(active_id=item.id)
            .create({})
        )
        self.assertEqual(wizard.review_ids, item.review_ids)

    def test_scheduled_action_button(self):
        """The Scheduled Action button opens the correction's scheduled job."""
        arch = self.env["tier.correction"].get_view(view_type="form")["arch"]
        button = etree.fromstring(arch).xpath("//button[@string='Scheduled Action']")[0]
        self.assertEqual(button.get("name"), "view_scheduled_action")
        self.assertEqual(button.get("type"), "object")

    def _get_correction_messages(self):
        subtype = self.env.ref(
            "base_tier_validation_correction.mt_tier_validation_correction"
        )
        return self.test_record.message_ids.filtered(lambda m: m.subtype_id == subtype)

    def _prepare_correction(self, new_reviewer):
        correction = self.env["tier.correction"].create(
            {
                "name": "Correction",
                "model_id": self.tester_model.id,
                "document_domain": str([("id", "=", self.test_record.id)]),
                "old_reviewer_ids": [Command.set(self.test_user_1.ids)],
                "new_reviewer_ids": [Command.set(new_reviewer.ids)],
            }
        )
        correction.action_prepare()
        return correction

    def _make_correction(self, new_reviewer):
        correction = self._prepare_correction(new_reviewer)
        correction.action_done()
        return correction

    def _request_validation_in_sequence(self):
        """Tiers in sequence: user 1, user 2, then user 1 again.
        Return the first and the last review, both for user 1."""
        self.definition_1.approve_sequence = True
        for sequence, reviewer in ((10, self.test_user_1), (20, self.test_user_2)):
            self._create_tier_definition(
                model_id=self.tester_model.id,
                review_type="individual",
                reviewer_id=reviewer.id,
                definition_domain="[('test_field', '=', 1.0)]",
                approve_sequence=True,
                sequence=sequence,
            )
        self.test_record.request_validation()
        reviews = self.test_record.review_ids.sorted("sequence")
        return reviews[0], reviews[-1]

    def test_correct_message_lists_corrected_reviewers_only(self):
        """A review approved between Prepare and Done is not corrected, so the
        correction message does not name its reviewer."""
        new_reviewer = self.test_user_3_multi_company
        first, last = self._request_validation_in_sequence()
        correction = self._prepare_correction(new_reviewer)
        self.assertEqual(correction.item_ids.review_ids, first | last)
        # User 1 approves the first tier before the correction is done
        self.test_record.with_user(self.test_user_1).validate_tier()
        self.assertEqual(first.status, "approved")
        correction.action_done()
        self.assertEqual(first.reviewer_ids, self.test_user_1)
        self.assertEqual(last.reviewer_ids, new_reviewer)
        message = self._get_correction_messages()
        self.assertEqual(len(message), 1)
        self.assertIn(new_reviewer.name, message.body)
        self.assertNotIn(self.test_user_1.name, message.body)

    def test_revert_message_lists_restored_reviewers_only(self):
        """A review approved by the new reviewer is not reverted, so the
        revert message does not name that reviewer."""
        new_reviewer = self.test_user_3_multi_company
        first, last = self._request_validation_in_sequence()
        correction = self._make_correction(new_reviewer)
        self.assertEqual(first.reviewer_ids, new_reviewer)
        self.assertEqual(last.reviewer_ids, new_reviewer)
        # The new reviewer approves the first tier, the last one stays open
        self.test_record.with_user(new_reviewer).validate_tier()
        self.assertEqual(first.status, "approved")
        self.assertIn(last.status, ["waiting", "pending"])
        correction.action_revert()
        self.assertEqual(first.reviewer_ids, new_reviewer)
        self.assertEqual(last.reviewer_ids, self.test_user_1)
        message = self._get_correction_messages()[0]
        self.assertIn("reverted reviewers", message.body)
        self.assertIn(self.test_user_1.name, message.body)
        self.assertNotIn(new_reviewer.name, message.body)

    def test_revert_message_skipped_when_nothing_reverted(self):
        """No revert message when the new reviewer approved every review."""
        new_reviewer = self.test_user_3_multi_company
        self.test_record.request_validation()
        correction = self._make_correction(new_reviewer)
        self.test_record.with_user(new_reviewer).validate_tier()
        self.assertEqual(self.test_record.review_ids.status, "approved")
        messages_before = self._get_correction_messages()
        correction.action_revert()
        self.assertEqual(self._get_correction_messages(), messages_before)
