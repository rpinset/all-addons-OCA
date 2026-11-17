# Copyright 2026 OCA / @bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from freezegun import freeze_time

from odoo import fields
from odoo.fields import Domain
from odoo.tests.common import tagged

from odoo.addons.base_tier_validation.tests.common import CommonTierValidation


@tagged("post_install", "-at_install")
class TierValidationBoard(CommonTierValidation):
    def setUp(self):
        super().setUp()
        # Trigger a review on the standard test fixture so the board
        # always has at least one record to render.
        self.test_record.with_user(self.test_user_2.id).request_validation()
        self.review = self.env["tier.review"].search(
            Domain("res_id", "=", self.test_record.id)
            & Domain("model", "=", self.test_record._name),
            limit=1,
        )
        self.assertTrue(self.review)

    def test_related_model_instance_compute(self):
        """The board's Reference + Char computes resolve cleanly off a
        real tier review."""
        review = self.review
        self.assertEqual(review.res_name, self.test_record.display_name)
        self.assertEqual(review.related_model_instance._name, self.test_record._name)
        self.assertEqual(review.related_model_instance.id, self.test_record.id)

    def test_model_id_related(self):
        """The `model_id` related field resolves to the validated model's
        `ir.model` record so pivot/graph views can display its
        human-friendly description instead of the technical name."""
        self.assertEqual(self.review.model_id, self.tester_model)
        self.assertEqual(self.review.model_id.model, self.test_record._name)

    def test_search_is_late_returns_id_in_domain(self):
        """`_search_is_late` returns a domain shape the ORM can use --
        either ``[("id", "in", ids)]`` or ``[("id", "not in", ids)]``
        depending on the operator/value pair, and never raises."""
        Model = self.env["tier.review"]
        for value in (True, False):
            for operator in ("=", "!="):
                domain = Model._search_is_late(operator, value)
                self.assertEqual(len(domain), 1)
                cond = domain[0]
                self.assertEqual(cond[0], "id")
                self.assertIn(cond[1], ("in", "not in", "="))
        # Bad operator -> match nothing (does not raise).
        bad = Model._search_is_late("ilike", "garbage")
        self.assertEqual(bad, [("id", "=", False)])

    def test_late_filter(self):
        """The Late filter finds late reviews through a real search.

        Odoo 19 passes the search method ``in`` instead of ``=``.
        """
        TierReview = self.env["tier.review"].with_user(self.test_user_1)
        self.assertNotIn(self.review, TierReview.search([("is_late", "=", True)]))
        self.assertIn(self.review, TierReview.search([("is_late", "=", False)]))
        with freeze_time(fields.Datetime.add(fields.Datetime.now(), days=30)):
            self.assertIn(self.review, TierReview.search([("is_late", "=", True)]))
            self.assertNotIn(self.review, TierReview.search([("is_late", "!=", True)]))

    def test_selection_related_model_instance(self):
        """The Reference selection only exposes tier-validated models,
        not every model in the DB."""
        selection = self.env["tier.review"]._selection_related_model_instance()
        models = {m for m, _name in selection}
        expected = set(self.env["tier.definition"]._get_tier_validation_model_names())
        self.assertEqual(models, expected)
        # Sanity: at least the standard tester model is in there.
        self.assertIn(self.test_record._name, models)

    def test_open_origin(self):
        """The board's `Open` button returns an act_window pointing at
        the underlying validated record."""
        action = self.review.open_origin()
        self.assertEqual(action["res_model"], self.test_record._name)
        self.assertEqual(action["res_id"], self.test_record.id)
        self.assertEqual(action["view_mode"], "form")

    def test_response_days_is_zero_until_reviewed(self):
        """`response_days` only populates once the review is approved
        or rejected; it stays 0 while pending/waiting."""
        self.assertEqual(self.review.response_days, 0.0)
        # Force-set a reviewed_date so the compute fires deterministically.
        self.review.write(
            {
                "reviewed_date": fields.Datetime.add(self.review.create_date, days=2),
                "status": "approved",
                "done_by": self.test_user_1.id,
            }
        )
        self.assertAlmostEqual(self.review.response_days, 2.0, places=2)

    def test_is_late_compute(self):
        """`is_late` flips True for waiting/pending reviews older than the
        configured threshold, and resets when the review is completed.

        Uses ``freeze_time`` to move "now" past the threshold instead
        of rewriting create_date, keeping the test independent of any
        ORM-side cache invariants around the create_date magic field.
        """
        # Fresh review: not late.
        self.assertFalse(self.review.is_late)
        # Move "now" 14 days forward -- the review's real create_date
        # is now well past the 7-day default late threshold.
        later = fields.Datetime.add(fields.Datetime.now(), days=14)
        with freeze_time(later):
            self.review.invalidate_recordset(["is_late"])
            self.assertTrue(self.review.is_late)
            # Once approved, the review is no longer "late" -- even
            # if it took forever, it's done.
            self.review.write({"status": "approved", "done_by": self.test_user_1.id})
            self.assertFalse(self.review.is_late)

    def test_late_after_days_respects_system_parameter(self):
        """The late threshold is read from
        ``base_tier_validation.late_after_days`` so an admin can tune it
        without a code change."""
        self.env["ir.config_parameter"].sudo().set_param(
            "base_tier_validation.late_after_days", "30"
        )
        # 14 days old is late at the default 7 but not at 30.
        later = fields.Datetime.add(fields.Datetime.now(), days=14)
        with freeze_time(later):
            self.review.invalidate_recordset(["is_late"])
            self.assertFalse(self.review.is_late)
        # 40 days old crosses the 30-day threshold.
        much_later = fields.Datetime.add(fields.Datetime.now(), days=40)
        with freeze_time(much_later):
            self.review.invalidate_recordset(["is_late"])
            self.assertTrue(self.review.is_late)

    def test_tier_review_dashboard_action_for_authorised_user(self):
        """Users in the board group get the dashboard action back from
        the systray hook so the "Show all reviews" footer link can open
        it. Users without the group get `False` -- without that gate
        clicking the link would fail with an AccessError."""
        group = self.env.ref("base_tier_validation_board.group_show_tier_review_board")
        admin = self.env.ref("base.user_admin")
        # Admin is already in the group via the security/groups.xml
        # default; assert and read the action.
        self.assertIn(admin, group.user_ids)
        action = self.env["res.users"].with_user(admin).tier_review_dashboard_action()
        self.assertTrue(action)
        self.assertEqual(action.get("res_model"), "tier.review")
        # test_user_2 is a plain employee and not in the dashboard group
        # -> the hook returns False so the systray omits the link.
        self.assertNotIn(self.test_user_2, group.user_ids)
        no_action = (
            self.env["res.users"]
            .with_user(self.test_user_2)
            .tier_review_dashboard_action()
        )
        self.assertFalse(no_action)

    def test_search_filters_by_user_acl(self):
        """The `_search` override hides reviews whose underlying record
        the current user cannot read. The standard tester model has a
        public ACL so test_user_2 sees everything; revoke that ACL and
        the review should drop out of the board for them."""
        # Sanity: test_user_2 can see the review with the default ACL.
        visible = (
            self.env["tier.review"]
            .with_user(self.test_user_2)
            .search(Domain("id", "=", self.review.id))
        )
        self.assertEqual(visible, self.review)
        # Restrict the model's ACL to admins; test_user_2 loses access.
        self.env["ir.model.access"].search(
            Domain("model_id", "=", self.tester_model.id)
        ).write({"group_id": self.env.ref("base.group_system").id})
        self.env["ir.model.access"].call_cache_clearing_methods()
        hidden = (
            self.env["tier.review"]
            .with_user(self.test_user_2)
            .search(Domain("id", "=", self.review.id))
        )
        self.assertFalse(hidden)

    def test_age_display_relative_for_open_reviews(self):
        """`age_display` gives a short relative age for open reviews and is
        empty once the review is done."""
        # Fresh review created "today".
        self.assertIn(self.review.age_display, ("today", "0d"))
        later = fields.Datetime.add(fields.Datetime.now(), days=90)
        with freeze_time(later):
            self.review.invalidate_recordset(["age_display"])
            self.assertTrue(self.review.age_display.endswith("mo"))
            self.review.write({"status": "approved", "done_by": self.test_user_1.id})
            self.assertFalse(self.review.age_display)

    def test_age_display_days_and_weeks(self):
        """Between one day and two weeks the age is shown in days, then in
        weeks until two months."""
        for days, expected in ((5, "5d"), (21, "3w")):
            with freeze_time(
                fields.Datetime.add(self.review.create_date, days=days, hours=1)
            ):
                self.review.invalidate_recordset(["age_display"])
                self.assertEqual(self.review.age_display, expected)

    def test_review_without_document(self):
        """A review not linked to a document has no name and no reference."""
        review = self.env["tier.review"].new({"model": self.test_record._name})
        self.assertFalse(review.res_name)
        self.assertFalse(review.related_model_instance)

    def test_selection_related_model_instance_no_tier_models(self):
        """Without any tier-validated model the selection is empty."""
        with mock.patch.object(
            type(self.env["tier.definition"]),
            "_get_tier_validation_model_names",
            return_value=[],
        ):
            self.assertEqual(
                self.env["tier.review"]._selection_related_model_instance(), []
            )

    def test_search_no_match_for_regular_user(self):
        """The per-document filter is skipped when the search finds nothing."""
        found = (
            self.env["tier.review"]
            .with_user(self.test_user_2)
            .search(Domain("id", "=", 0))
        )
        self.assertFalse(found)

    def test_tier_review_dashboard_action_missing_action(self):
        """No link is offered when the board action has been deleted."""
        self.env.ref("base_tier_validation_board.open_boards_tier_reviews").unlink()
        admin = self.env.ref("base.user_admin")
        self.assertFalse(
            self.env["res.users"].with_user(admin).tier_review_dashboard_action()
        )
