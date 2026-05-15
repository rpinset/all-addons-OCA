# Copyright 2020 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain

_logger = logging.getLogger(__name__)


class TierCorrection(models.Model):
    _name = "tier.correction"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Tier Review Correction"
    _order = "id desc"

    name = fields.Char(
        string="Description",
        required=True,
    )
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="On Model",
        domain=lambda self: [
            (
                "model",
                "in",
                self.env["tier.definition"]._get_tier_validation_model_names(),
            )
        ],
    )
    model = fields.Char(related="model_id.model", index=True, store=True)
    correction_type = fields.Selection(
        selection=[
            ("reviewer", "Reassign Reviewer(s)"),
        ],
        default="reviewer",
        required=True,
    )
    search_name = fields.Char(
        string="Name Search",
    )
    old_reviewer_ids = fields.Many2many(
        comodel_name="res.users",
        relation="tier_correction_old_reviewer_rel",
        string="Original Reviewer(s)",
        help="Find documents with tier reviews matching some reviewers",
    )
    new_reviewer_ids = fields.Many2many(
        comodel_name="res.users",
        relation="tier_correction_new_reviewer_rel",
        string="Reassign Reviewer(s)",
        help="Reassign these reviewers to the tier reviews of the found document",
    )
    item_ids = fields.One2many(
        comodel_name="tier.correction.item",
        inverse_name="correction_id",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("prepare", "Preparing"),
            ("done", "Corrected"),
            ("cancel", "Cancelled"),
            ("revert", "Reverted"),
        ],
        string="Status",
        copy=False,
        index=True,
        tracking=1,
        default="draft",
    )
    reference = fields.Char(
        string="Affected Documents",
        compute="_compute_reference",
        store=True,
    )
    date_schedule_correct = fields.Datetime(
        string="Scheduled Correction Date",
        copy=False,
    )
    date_actual_correct = fields.Datetime(
        string="Actual Correction Date",
        copy=False,
    )
    date_schedule_revert = fields.Datetime(
        string="Scheduled Revert Date",
        copy=False,
    )
    date_actual_revert = fields.Datetime(
        string="Actual Revert Date",
        copy=False,
    )

    @api.constrains("date_schedule_correct", "date_schedule_revert")
    def _check_date(self):
        """Correct Date < Revert Date"""
        for rec in self:
            now = fields.Datetime.now()
            correct = rec.date_schedule_correct or now
            revert = rec.date_schedule_revert or correct or now
            if not (correct <= revert):
                raise ValidationError(
                    self.env._("Revert Date should be after Correct Date")
                )

    def search_document(self):
        for rec in self:
            rec.item_ids.unlink()
            if rec.correction_type == "reviewer":
                doc_domain = Domain("review_ids.status", "in", ["waiting", "pending"])
                review_domain = Domain("status", "in", ["waiting", "pending"])
                if rec.search_name:
                    doc_ids = self.env[rec.model].name_search(rec.search_name)
                    doc_domain &= Domain("id", "in", list(dict(doc_ids).keys()))
                if rec.old_reviewer_ids:
                    doc_domain &= Domain(
                        "review_ids.reviewer_ids", "in", rec.old_reviewer_ids.ids
                    )
                    review_domain &= Domain(
                        "reviewer_ids", "in", rec.old_reviewer_ids.ids
                    )
                items = []
                for doc in self.env[rec.model].search_fetch(
                    doc_domain, ["review_ids", "display_name"]
                ):
                    review_ids = doc.review_ids.filtered_domain(review_domain).ids
                    items.append(
                        Command.create(
                            {
                                "res_model": doc._name,
                                "res_id": doc.id,
                                "resource_ref": f"{doc._name},{doc.id}",
                                "reference": doc.display_name,
                                "new_reviewer_ids": [
                                    Command.set(rec.new_reviewer_ids.ids)
                                ],
                                "review_ids": [Command.set(review_ids)],
                            },
                        )
                    )
                rec.write({"item_ids": items})

    @api.depends("item_ids")
    def _compute_reference(self):
        for rec in self:
            rec.reference = ", ".join(
                rec.item_ids.filtered("reference").mapped("reference")
            )

    def do_correct(self):
        for rec in self:
            if rec.state != "prepare":
                raise ValidationError(
                    self.env._("Correction is allowed on state = 'prepare' only")
                )
            if rec.correction_type == "reviewer":
                rec.item_ids.correct()
        self.write({"date_actual_correct": fields.Datetime.now()})

    def do_revert(self):
        for rec in self:
            if rec.state != "done":
                raise ValidationError(
                    self.env._("Correction is allowed on state = 'done' only")
                )
            if rec.correction_type == "reviewer":
                rec.item_ids.revert()
        self.write({"date_actual_revert": fields.Datetime.now()})

    def action_draft(self):
        self.mapped("item_ids").unlink()
        self.write({"state": "draft"})

    def action_prepare(self):
        self.search_document()
        self.write({"state": "prepare"})

    def action_done(self):
        self.do_correct()
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_revert(self):
        self.do_revert()
        self.write({"state": "revert"})

    def view_scheduled_action(self):
        self.ensure_one()
        result = self.env["ir.actions.act_window"]._for_xml_id("base.ir_cron_act")
        cron = self.env.ref("base_tier_validation_correction.tier_correction_scheduler")
        result["domain"] = list(Domain("id", "in", cron.ids))
        return result

    def _tier_correction_auto_run(self):
        # To correct
        to_correct = self.search(
            Domain("state", "=", "prepare")
            & Domain("date_schedule_correct", "!=", False)
            & Domain("date_schedule_correct", "<=", fields.Datetime.now())
        )
        to_correct.action_done()
        _logger.info("Tier Correction - Correction: %s", to_correct)
        # To revert
        to_revert = self.search(
            Domain("state", "=", "done")
            & Domain("date_schedule_revert", "!=", False)
            & Domain("date_schedule_revert", "<=", fields.Datetime.now())
        )
        to_revert.action_revert()
        _logger.info("Tier Correction - Reversion: %s", to_revert)
