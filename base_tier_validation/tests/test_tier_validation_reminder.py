# Copyright 2018-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from freezegun import freeze_time

from odoo import fields
from odoo.tests.common import tagged
from odoo.tools import mute_logger

from .common import CommonTierValidation


@tagged("post_install", "-at_install")
class TierTierValidation(CommonTierValidation):
    def test_validation_reminder(self):
        """Check the posting of reminder to reviews."""
        tier_definition = self.tier_definition
        tier_definition.notify_reminder_delay = 3

        # Request a review today
        self.test_record.with_user(self.test_user_2.id).request_validation()
        review = self.env["tier.review"].search(
            [("definition_id", "=", tier_definition.id)]
        )
        self.assertTrue(review)
        self.assertEqual(review.last_reminder_date, False)

        # 2 days later no reminder should be posted
        in_2_days = fields.Datetime.add(fields.Datetime.now(), days=2)
        with freeze_time(in_2_days):
            tier_definition._cron_send_review_reminder()
        self.assertEqual(review.last_reminder_date, False)
        # 4 days later first reminder
        in_4_days = fields.Datetime.add(fields.Datetime.now(), days=4)
        with freeze_time(in_4_days):
            self.tier_definition._cron_send_review_reminder()
        self.assertEqual(review.last_reminder_date, in_4_days)
        # 5 days later no new reminder
        in_6_days = fields.Datetime.add(fields.Datetime.now(), days=6)
        with freeze_time(in_6_days):
            self.tier_definition._cron_send_review_reminder()
        self.assertEqual(review.last_reminder_date, in_4_days)
        # 9 days later second reminder
        in_9_days = fields.Datetime.add(fields.Datetime.now(), days=9)
        with freeze_time(in_9_days):
            self.tier_definition._cron_send_review_reminder()
        self.assertEqual(review.last_reminder_date, in_9_days)

    def test_validation_reminder_batch(self):
        """A single cron run reminds every eligible review in a definition,
        not just the first one.

        Regression coverage for the recordset-aware iteration in
        ``_send_review_reminder`` plus the bumped ``limit`` in
        ``_get_review_needing_reminder``. Before the fix, only the first
        review of the batch ever got ``last_reminder_date`` set per cron
        tick -- a silent backlog on installations with many pending
        reviews under the same definition.
        """
        tier_definition = self.tier_definition
        tier_definition.notify_reminder_delay = 1
        extra_records = self.test_model.create([{"test_field": 1.0} for _ in range(2)])
        records = self.test_record + extra_records
        for record in records:
            record.with_user(self.test_user_2.id).request_validation()
        reviews = self.env["tier.review"].search(
            [
                ("definition_id", "=", tier_definition.id),
                ("res_id", "in", records.ids),
            ]
        )
        self.assertEqual(len(reviews), 3)
        for rev in reviews:
            self.assertFalse(rev.last_reminder_date)
        later = fields.Datetime.add(fields.Datetime.now(), days=2)
        with freeze_time(later):
            tier_definition._cron_send_review_reminder()
        for rev in reviews:
            self.assertEqual(rev.last_reminder_date, later)

    def test_validation_reminder_skips_orphans(self):
        """A tier.review whose validated record no longer exists must not
        crash the cron. Such orphans only happen when the document was
        deleted by something that bypassed the cascade unlink (raw SQL,
        broken module uninstall, ...). The reminder cron is then expected
        to skip them silently."""
        tier_definition = self.tier_definition
        tier_definition.notify_reminder_delay = 1
        self.test_record.with_user(self.test_user_2.id).request_validation()
        review = self.env["tier.review"].search(
            [
                ("definition_id", "=", tier_definition.id),
                ("res_id", "=", self.test_record.id),
            ]
        )
        self.assertTrue(review)
        # Drop the validated record at the SQL level so the cascade
        # unlink defined on ``tier.validation`` does not also remove the
        # review row -- that's what makes the review an orphan.
        self.env.cr.execute(
            "DELETE FROM tier_validation_tester WHERE id = %s",
            (self.test_record.id,),
        )
        self.env.invalidate_all()
        later = fields.Datetime.add(fields.Datetime.now(), days=2)
        # Before the orphan guard, this raised on browse(...).message_post().
        with freeze_time(later):
            tier_definition._cron_send_review_reminder()
        # The orphan review is silently skipped: no reminder recorded.
        self.assertFalse(review.last_reminder_date)

    @mute_logger("odoo.addons.base_tier_validation.models.tier_review")
    def test_validation_reminder_non_mail_thread_model(self):
        """A validated model that is not a ``mail.thread`` (no
        ``message_post``) must not break the reminder cron. Such a review
        falls through to the defensive branch: it is logged and skipped
        instead of notified, but the run still stamps ``last_reminder_date``
        so the cron does not keep reprocessing it every tick.
        """
        definition = self.env["tier.definition"].create(
            {
                "model_id": self.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '=', 2.5)]",
                "notify_reminder_delay": 1,
                "name": "tester2 reminder -- no mail.thread",
            }
        )
        record = self.test_model_2.create({"test_field": 2.5})
        record.with_user(self.test_user_2.id).request_validation()
        review = self.env["tier.review"].search(
            [
                ("definition_id", "=", definition.id),
                ("res_id", "=", record.id),
            ]
        )
        self.assertTrue(review)
        self.assertFalse(review.last_reminder_date)
        later = fields.Datetime.add(fields.Datetime.now(), days=2)
        with freeze_time(later):
            definition._cron_send_review_reminder()
        # ``tier.validation.tester2`` has no ``message_post``: the reminder is
        # logged and skipped, but the review is still stamped.
        self.assertEqual(review.last_reminder_date, later)
