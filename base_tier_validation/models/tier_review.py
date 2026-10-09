# Copyright 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class TierReview(models.Model):
    _name = "tier.review"
    _description = "Tier Review"
    _order = "sequence, id"

    name = fields.Char(related="definition_id.name")
    status = fields.Selection(
        [
            ("waiting", "Waiting"),
            ("pending", "Pending"),
            ("rejected", "Rejected"),
            ("approved", "Approved"),
            ("cancel", "Cancel"),
        ],
        default="waiting",
    )
    model = fields.Char(string="Related Document Model", index=True)
    res_id = fields.Many2oneReference(
        string="Related Document ID",
        index=True,
        model_field="model",
    )
    definition_id = fields.Many2one(comodel_name="tier.definition")
    company_id = fields.Many2one(
        related="definition_id.company_id",
        store=True,
    )
    review_type = fields.Selection(related="definition_id.review_type")
    reviewer_id = fields.Many2one(related="definition_id.reviewer_id")
    reviewer_group_id = fields.Many2one(related="definition_id.reviewer_group_id")
    reviewer_field_id = fields.Many2one(related="definition_id.reviewer_field_id")
    reviewer_ids = fields.Many2many(
        string="Reviewers",
        comodel_name="res.users",
        compute="_compute_reviewer_ids",
        store=True,
    )
    display_status = fields.Char(compute="_compute_display_status")
    sequence = fields.Integer(string="Tier")
    todo_by = fields.Char(compute="_compute_todo_by", store=True)
    done_by = fields.Many2one(comodel_name="res.users")
    requested_by = fields.Many2one(comodel_name="res.users")
    reviewed_date = fields.Datetime(string="Validation Date")
    reviewed_formated_date = fields.Char(
        string="Validation Formated Date", compute="_compute_reviewed_formated_date"
    )
    has_comment = fields.Boolean(related="definition_id.has_comment")
    comment = fields.Char(string="Comments")
    can_review = fields.Boolean(
        compute="_compute_can_review",
        store=True,
        help="""Can review will be marked if the review is pending and the
        approve sequence has been achieved""",
    )
    approve_sequence = fields.Boolean(related="definition_id.approve_sequence")
    approve_sequence_bypass = fields.Boolean(
        related="definition_id.approve_sequence_bypass"
    )
    last_reminder_date = fields.Datetime(readonly=True)

    @api.depends("status")
    def _compute_display_status(self):
        """
        Compute the display status based on the current status value to get the
        translated status value.
        """
        selection = self.fields_get(["status"])["status"]["selection"]
        selection_dict = dict(selection)
        for record in self:
            record.display_status = selection_dict[record.status]

    @api.depends_context("tz")
    def _compute_reviewed_formated_date(self):
        for review in self:
            if not review.reviewed_date:
                review.reviewed_formated_date = False
                continue
            reviewed_date_tz = fields.Datetime.context_timestamp(
                self, review.reviewed_date
            )
            review.reviewed_formated_date = reviewed_date_tz.replace(tzinfo=None)

    @api.depends("status", "approve_sequence", "sequence", "model", "res_id")
    def _compute_can_review(self):
        # Only open reviews of sequential definitions reach the branch of
        # ``_can_review_value`` that looks at the document, so only those are
        # worth warming.
        self.filtered(
            lambda r: r.approve_sequence and r.status in ("waiting", "pending")
        )._prefetch_resource_reviews()
        for record in self:
            record.can_review = record._can_review_value()

    def _has_resource_model(self, model=None):
        """Whether the review's document model (or ``model``) still has tier
        validation. It may have been uninstalled, or have dropped tier
        validation, while reviews pointing at it survive."""
        model = model or self.model
        return (
            bool(model)
            and model in self.env
            and "review_ids" in self.env[model]._fields
        )

    def _prefetch_resource_reviews(self):
        """Warm the cache with the reviews of every resource in ``self``.

        ``_can_review_value`` browses its own ``res_id`` to find the lowest
        pending sequence on that document. Record by record, that browse has a
        prefetch set of exactly one id, so every review pays a fresh read of
        its document's ``review_ids`` -- a handful of queries per review, on
        every recompute of this (stored) field. The systray recount flushes
        ``can_review``, so the cost of the counter grew with the reviewer's
        backlog.

        Reading the same relation once per model puts the values in the
        environment cache, where the per-record browse then finds them for
        free. Callers pass the subset whose documents they are about to look
        at.
        """
        res_ids_per_model = defaultdict(list)
        for record in self:
            if record.model and record.res_id:
                res_ids_per_model[record.model].append(record.res_id)
        for model, res_ids in res_ids_per_model.items():
            if not self._has_resource_model(model):
                continue
            self.env[model].browse(res_ids).review_ids.fetch(["status", "sequence"])

    def _update_review_status(self):
        """Promote reviews that are currently available to pending."""
        # To defer recompute, use context key
        # `tier_validation_defer_compute_can_review`.
        # Be sure to explicitely call the method afterwards.
        if self.env.context.get("tier_validation_defer_compute_can_review"):
            return
        reviews = self.filtered(lambda rev: rev.status in ["waiting", "pending"])
        if not reviews:
            return
        # Lowest still-open sequence *per record*, computed over the whole
        # record's reviews -- NOT just this recordset. Computing it over
        # ``self`` promotes a later tier prematurely whenever the method runs on
        # a subset that excludes the lower-sequence predecessors, e.g.
        # ``review_user_count`` calling ``user.review_ids._update_review_status()``
        # for a second-tier reviewer (their own review is then the only -- and
        # thus "minimum" -- sequence in the set, so it wrongly goes ``pending``).
        # One grouped query for all records, rather than reading each
        # document's reviews in turn: the systray calls this on the reviewer's
        # whole backlog. Reading tier.review directly also copes with reviews
        # whose model was uninstalled or no longer has tier validation.
        groups = self.env["tier.review"]._read_group(
            [
                ("model", "in", list(set(reviews.mapped("model")))),
                ("res_id", "in", list(set(reviews.mapped("res_id")))),
                ("status", "in", ("waiting", "pending")),
            ],
            groupby=["model", "res_id"],
            aggregates=["sequence:min"],
        )
        min_seq_by_record = {
            (model, res_id): sequence for model, res_id, sequence in groups
        }
        for record in reviews:
            if record.status != "waiting":
                continue
            # Nobody can act on a review whose document is gone, and notifying
            # its reviewers would fail on the missing model.
            if not (record.res_id and record._has_resource_model()):
                continue
            if record.approve_sequence and record.sequence != min_seq_by_record.get(
                (record.model, record.res_id)
            ):
                continue
            record.status = "pending"
            if record.definition_id.notify_on_pending:
                record._notify_pending_status(record)
        reviews.flush_recordset(["status", "can_review"])

    def _can_review_value(self):
        if self.status not in ("pending", "waiting"):
            return False
        if not self.approve_sequence:
            return True
        # An orphaned review can neither be opened nor approved.
        if not (self.res_id and self._has_resource_model()):
            return False
        resource = self.env[self.model].browse(self.res_id)
        reviews = resource.review_ids.filtered(lambda r: r.status == "pending")
        if not reviews:
            return True
        sequence = min(reviews.mapped("sequence"))
        return self.sequence == sequence

    @api.model
    def _get_reviewer_fields(self):
        return [
            "reviewer_id",
            "reviewer_group_id",
            "reviewer_group_id.user_ids",
            "definition_id.exclude_requester",
            "requested_by",
        ]

    @api.depends(lambda self: self._get_reviewer_fields())
    def _compute_reviewer_ids(self):
        for rec in self:
            rec.reviewer_ids = rec._get_reviewers()

    @api.depends("reviewer_ids")
    def _compute_todo_by(self):
        """Show by group or by abbrev list of names"""
        num_show = 3  # Max number of users to display
        for rec in self:
            todo_by = False
            if rec.reviewer_group_id:
                todo_by = self.env._("Group %s", rec.reviewer_group_id.name)
            else:
                todo_by = ", ".join(rec.reviewer_ids[:num_show].mapped("display_name"))
                num_users = len(rec.reviewer_ids)
                if num_users > num_show:
                    todo_by = f"{todo_by} (and {num_users - num_show} more)"
            rec.todo_by = todo_by

    def _get_reviewers(self):
        reviewers = self.env["res.users"]
        if self.reviewer_id or self.reviewer_group_id.user_ids:
            reviewers = self.reviewer_id + self.reviewer_group_id.user_ids
        elif self.reviewer_field_id:
            resource = self.env[self.model].browse(self.res_id)
            reviewer_field = getattr(resource, self.reviewer_field_id.name, False)
            if reviewer_field:
                if reviewer_field._name == "res.groups":
                    reviewers = reviewer_field.user_ids
                elif reviewer_field._name == "res.users":
                    reviewers = reviewer_field
                else:
                    raise ValidationError(
                        self.env._(
                            "Validation reviewer field "
                            "should be of the appropriate type"
                        )
                    )
        # Four-eyes: drop the requester from the reviewer pool if the
        # definition opted in. Done as a post-filter so it applies
        # uniformly across individual / group / field review types.
        if self.definition_id.exclude_requester and self.requested_by:
            reviewers -= self.requested_by
        return reviewers

    def _notify_pending_status(self, review_ids):
        """Method to call and reuse abstract notification method"""
        resource = self.env[self.model].browse(self.res_id)
        resource._notify_review_available(review_ids)

    def _get_reminder_notification_subtype(self):
        return "base_tier_validation.mt_tier_validation_reminder"

    def _get_reminder_activity_type(self):
        return "base_tier_validation.mail_act_tier_validation_reminder"

    def _notify_review_reminder_body(self):
        delay = (fields.Datetime.now() - self.create_date).days
        return self.env._("A review has been requested %s days ago.", delay)

    def _send_review_reminder(self):
        for rev in self:
            record = self.env[rev.model].browse(rev.res_id)
            if not record.exists():  # <-- skip orphaned reviews
                continue
            # Only schedule activity if reviewer is a single user and model
            # has activities. Excluded from coverage: exercising it needs a
            # validated model mixing in ``mail.activity.mixin``, which none of
            # the base test models do (they are ``mail.thread`` at most).
            if (  # pragma: no cover
                len(rev.reviewer_ids) == 1 and hasattr(record, "activity_ids")
            ):
                rev._schedule_review_reminder_activity(record)
            elif hasattr(record, "message_post"):
                rev._notify_review_reminder(record)
            else:
                msg = f"Could not send reminder for record {record}"
                _logger.exception(msg)
            rev.last_reminder_date = fields.Datetime.now()

    def _notify_review_reminder(self, record):
        record.message_post(
            subtype_xmlid=self._get_reminder_notification_subtype(),
            body=self._notify_review_reminder_body(),
        )

    def _schedule_review_reminder_activity(self, record):
        record.activity_schedule(
            act_type_xmlid=self._get_reminder_activity_type(),
            note=self._notify_review_reminder_body(),
            user_id=self.reviewer_ids.id,
        )
