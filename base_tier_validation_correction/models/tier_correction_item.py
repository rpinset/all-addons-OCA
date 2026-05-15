# Copyright 2020 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, fields, models


class TierCorrectionItem(models.Model):
    _name = "tier.correction.item"
    _description = "Tier Correction Detail"

    correction_id = fields.Many2one(
        comodel_name="tier.correction",
        index=True,
    )
    res_model = fields.Char(readonly=True)
    res_id = fields.Integer(readonly=True)
    resource_ref = fields.Reference(
        string="Resource",
        selection=lambda self: [
            (model.model, model.name) for model in self.env["ir.model"].search([])
        ],
        readonly=True,
    )
    reference = fields.Char(readonly=True)
    new_reviewer_ids = fields.Many2many(
        comodel_name="res.users",
        relation="tier_correction_item_new_reviewer_rel",
        string="New Reviewers",
        help="These reviewers will overwrite the existing reviewer_ids in tier.review",
    )
    review_ids = fields.Many2many(
        comodel_name="tier.review",
        string="Affected Tier Reviews",
        help="Tier reivews that will be affected by this correction.",
    )

    def _notify_reviewer_change(self, ttype="correct"):
        self.ensure_one()
        post = "message_post"
        if hasattr(self.resource_ref, post):
            tier_reviews = self.review_ids
            reviews = ", ".join(tier_reviews.filtered("name").mapped("name"))
            reviewers = ", ".join(
                tier_reviews.reviewer_ids.filtered("name").mapped("name")
            )
            message = self.env._(
                "The Correction '%(name)s', "
                "corrrected reviewers "
                "on '%(reviews)s' to '%(reviewers)s'",
                name=self.correction_id.name,
                reviews=reviews,
                reviewers=reviewers,
            )
            if ttype == "revert":
                message = self.env._(
                    "The Correction '%(name)s', "
                    "reverted reviewers on '%(reviews)s' "
                    "back to '%(reviewers)s'",
                    name=self.correction_id.name,
                    reviews=reviews,
                    reviewers=reviewers,
                )
            getattr(self.resource_ref.sudo(), post)(
                subtype_xmlid=(
                    "base_tier_validation_correction.mt_tier_validation_correction"
                ),
                body=message,
            )

    def correct(self):
        for item in self:
            # Only waiting/pending reviews will gets updated
            reviews = item.review_ids.filtered(
                lambda record: record.status in ["waiting", "pending"]
            )
            reviews.write({"reviewer_ids": [Command.set(item.new_reviewer_ids.ids)]})
            item._notify_reviewer_change("correct")

    def revert(self):
        for item in self:
            reviews = item.review_ids.filtered(
                lambda record: record.status in ["waiting", "pending"]
            )
            for review in reviews:
                review.reviewer_ids = review._get_reviewers()
            item._notify_reviewer_change("revert")
