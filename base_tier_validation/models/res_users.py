# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, modules
from odoo.exceptions import AccessError
from odoo.fields import Domain

_logger = logging.getLogger(__name__)

# Default for the ``base_tier_validation.late_after_days`` system parameter
# used by the systray to split pending reviews into a "Late" bucket.
DEFAULT_LATE_AFTER_DAYS = 7


class Users(models.Model):
    _inherit = "res.users"

    review_ids = fields.Many2many(
        string="Reviews", comodel_name="tier.review", copy=False
    )

    @api.model
    def review_user_count(self):
        """Counts driving the tier-review systray dropdown.

        Each returned dict represents one model that has reviews touching
        the current user and reports three buckets so the dropdown can
        mirror Odoo's activity systray layout:

        - ``late_count`` -- reviews pending for longer than the configured
          *late* threshold (``base_tier_validation.late_after_days``,
          default ``7``). The reviewer should prioritise these.
        - ``pending_count`` -- pending reviews within the threshold.
          Standard work the reviewer can act on today.
        - ``future_count`` -- waiting reviews where the current user is
          assigned as reviewer but the sequence has not yet promoted the
          review to pending. "What is incoming for me". Records already
          counted as late or pending are left out.

        The per-bucket record ids are returned alongside the counts so
        clicking a bucket in the systray opens exactly those records.
        """
        user_reviews = {}
        user = self.env.user
        user.review_ids._update_review_status()
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "base_tier_validation.late_after_days",
                default=str(DEFAULT_LATE_AFTER_DAYS),
            )
        )
        try:
            late_after_days = max(0, int(param))
        except (TypeError, ValueError):
            late_after_days = DEFAULT_LATE_AFTER_DAYS
        late_cutoff = fields.Datetime.subtract(
            fields.Datetime.now(), days=late_after_days
        )
        # Fetch every actionable review touching this user (pending +
        # waiting) in one read_group so we only pay the SQL cost once.
        domain = Domain("status", "in", ["pending", "waiting"]) & Domain(
            "id", "in", user.review_ids.ids
        )
        review_groups = self.env["tier.review"]._read_group(
            domain=domain,
            groupby=["model"],
            aggregates=["id:recordset"],
        )
        for model, tier_reviews in review_groups:
            # Skip Models not having Tier Validation enabled (example: was unistalled)
            if model not in self.env:
                continue
            Model = self.env[model]
            if not hasattr(Model, "can_review"):
                continue
            pending_reviews = tier_reviews.filtered(
                lambda r: r.status == "pending" and r.can_review
            )
            future_reviews = tier_reviews.filtered(lambda r: r.status == "waiting")
            # Late counts from when the review became pending, so a later
            # tier of an Approve by sequence validation is not late as soon
            # as it reaches its reviewer. Reviews pending from before that
            # date was stored fall back to their creation date.
            late_reviews = pending_reviews.filtered(
                lambda r: (r.pending_date or r.create_date) < late_cutoff
            )
            records_domain = Domain("id", "in", tier_reviews.mapped("res_id")) & Domain(
                "validation_status", "!=", "rejected"
            )
            # Excludes any cancelled records depending on the structure of
            # the model. Let PostgreSQL do it whenever the state field is a
            # real column -- which it is on every model that stores its
            # state -- and keep the Python pass only as the fallback for
            # models whose state field is computed and not stored.
            state_field = Model._fields.get(Model._state_field)
            state_in_db = state_field is not None and state_field.store
            if state_in_db:
                records_domain &= Domain(Model._state_field, "!=", Model._cancel_state)
            try:
                # Resolve pending and waiting reviews to their records in a
                # single search, honouring ACL + record rules + the active
                # flag.
                records = (
                    Model.with_user(user)
                    .with_context(active_test=False)
                    .search(records_domain)
                )
            except AccessError:
                # The user is a reviewer on records of a model whose
                # ir.model.access does not grant them read access (e.g.
                # a tier definition pointing at account.move while the
                # reviewer has no accounting group). Skip silently so
                # the systray keeps working; the reviewer cannot act on
                # these reviews anyway without read access.
                _logger.debug(
                    "User %s has no read access to %s; skipping in systray.",
                    user.login,
                    model,
                )
                continue
            if not state_in_db and Model._state_field in Model._fields:
                records = records.filtered(
                    lambda x: x[x._state_field] != x._cancel_state
                )
            pending_res_ids = set(pending_reviews.mapped("res_id"))
            future_res_ids = set(future_reviews.mapped("res_id"))
            late_res_ids = set(late_reviews.mapped("res_id"))
            # ``can_review`` is deliberately *not* part of ``records_domain``.
            # Its search method re-searches the reviewer's whole backlog on
            # this model and then evaluates the field in Python over all of
            # it, so putting it in the domain made the systray cost grow
            # with the backlog -- on every call, for every reviewer. The
            # candidate set is already narrowed to the reviews found above,
            # so evaluate the field on those records instead: same answer,
            # one prefetched batch instead of a second search.
            pending_records = records.filtered(
                lambda x, ids=pending_res_ids: x.id in ids and x.can_review
            )
            # A record the user can already act on is not shown as Future
            # as well, the buckets count documents.
            future_records = (
                records.filtered(lambda x, ids=future_res_ids: x.id in ids)
                - pending_records
            )
            late_records = pending_records.filtered(
                lambda x, ids=late_res_ids: x.id in ids
            )
            pending_ontime_records = pending_records - late_records
            if not (late_records or pending_ontime_records or future_records):
                continue
            first_record = (
                late_records[:1] or pending_ontime_records[:1] or future_records[:1]
            )
            user_reviews[model] = {
                "id": first_record.id,
                "name": Model._description,
                "model": model,
                "active_field": "active" in Model._fields,
                "icon": modules.module.get_module_icon(Model._original_module),
                "type": "tier_review",
                "late_count": len(late_records),
                "pending_count": len(pending_ontime_records),
                "future_count": len(future_records),
                "late_ids": late_records.ids,
                "pending_ids": pending_ontime_records.ids,
                "future_ids": future_records.ids,
            }
        return list(user_reviews.values())

    @api.model
    def tier_review_dashboard_action(self):
        """Optional hook returning the action a downstream module wants the
        systray's "Show all reviews" footer link to open. Default is
        ``False`` so no link is rendered. ``base_tier_validation_board``
        (and any other dashboard module) overrides this to point at its
        global review dashboard, matching the pattern of Odoo's
        "View all activities" footer in the activity systray."""
        return False
