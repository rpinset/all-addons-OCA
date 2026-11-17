# Copyright 2024 ForgeFlow S.L.  <https://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import SQL, split_every

# Fallback for the ``base_tier_validation.late_after_days`` system parameter:
# the number of days after which a still-pending/waiting review counts as
# "late". Shared with base_tier_validation's reviewer systray (the "Late"
# bucket), so the board's ``is_late`` indicator/filter and the systray agree
# on one admin-configurable threshold (Settings > Technical > System
# Parameters). Used by the kanban "rotten" colour and the "Late" search filter.
DEFAULT_LATE_AFTER_DAYS = 7


class TierReview(models.Model):
    _name = "tier.review"
    _inherit = ["tier.review", "mail.thread", "mail.activity.mixin"]

    @api.depends("model", "res_id")
    def _compute_res_name(self):
        for record in self:
            if record.res_id and record.model in self.env:
                record.res_name = (
                    self.env[record.model].browse(record.res_id).display_name
                )
            else:
                record.res_name = False

    related_model_instance = fields.Reference(
        selection="_selection_related_model_instance",
        compute="_compute_related_model_instance",
        string="Document",
    )
    res_name = fields.Char(
        "Resource Name", compute="_compute_res_name", compute_sudo=True
    )
    # Stored m2o to ir.model (rather than the base `model` char) so the
    # list/pivot/graph show and group by the model's human-friendly
    # description (e.g. "Journal Entry") instead of its technical name
    # ("account.move"). The help below is what the user sees on hover, so
    # keep it plain.
    model_id = fields.Many2one(
        comodel_name="ir.model",
        related="definition_id.model_id",
        store=True,
        string="Model",
        help="The kind of document this review is for (e.g. Journal Entry, Contract).",
    )
    response_days = fields.Float(
        string="Response time (days)",
        compute="_compute_response_days",
        store=True,
        # Aggregate as an AVERAGE, not a sum: the useful KPI is "reviews
        # took N days on average", whereas a sum of everyone's turnaround
        # is a meaningless total. Drives the "avg days" measure in the
        # Review Statistics pivot/graph.
        aggregator="avg",
        help="Days between the review being created and it being done "
        "(0 until it is approved or rejected). Averaged in pivot/graph "
        "views, so the measure reads as the mean review turnaround.",
    )
    age_display = fields.Char(
        compute="_compute_age_display",
        string="Waiting",
        help="How long an open (pending/waiting) review has been waiting, in "
        "a short relative form (e.g. 3d, 2w, 4mo). Empty once the review is "
        "done. Used on the kanban card so aging stands out.",
    )
    is_late = fields.Boolean(
        compute="_compute_is_late",
        search="_search_is_late",
        string="Late",
        help="Set when the review is still waiting for a decision and has "
        "been pending longer than the configured threshold "
        "(base_tier_validation.late_after_days, default 7 days). Shown on "
        "the kanban with a 'rotten' colour and available as the 'Late' "
        "filter.",
    )

    @api.model
    def _late_after_days(self):
        """Days before a pending/waiting review counts as late.

        Read from the ``base_tier_validation.late_after_days`` system
        parameter (the same one the reviewer systray uses) so a single,
        admin-configurable value drives both. Falls back to
        ``DEFAULT_LATE_AFTER_DAYS`` when the parameter is unset.
        """
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "base_tier_validation.late_after_days",
                default=str(DEFAULT_LATE_AFTER_DAYS),
            )
        )

    @api.depends("create_date", "reviewed_date")
    def _compute_response_days(self):
        for rec in self:
            if rec.create_date and rec.reviewed_date:
                rec.response_days = (
                    rec.reviewed_date - rec.create_date
                ).total_seconds() / 86400.0
            else:
                rec.response_days = 0.0

    @api.depends("status", "create_date")
    def _compute_is_late(self):
        cutoff = fields.Datetime.subtract(
            fields.Datetime.now(), days=self._late_after_days()
        )
        for rec in self:
            rec.is_late = (
                rec.status in ("waiting", "pending")
                and rec.create_date
                and rec.create_date < cutoff
            )

    @api.depends("status", "create_date")
    def _compute_age_display(self):
        now = fields.Datetime.now()
        for rec in self:
            if rec.status in ("waiting", "pending") and rec.create_date:
                days = (now - rec.create_date).days
                if days < 1:
                    rec.age_display = self.env._("today")
                elif days < 14:
                    rec.age_display = f"{days}d"
                elif days < 60:
                    rec.age_display = f"{days // 7}w"
                else:
                    rec.age_display = f"{days // 30}mo"
            else:
                rec.age_display = False

    @api.model
    def _search_is_late(self, operator, value):
        # Odoo 19 hands search methods normalized operators: a filter on
        # ``is_late = True`` arrives as ``in [True]``. Accept both forms.
        if operator in ("=", "!="):
            operator = "in" if operator == "=" else "not in"
            value = [value]
        if operator not in ("in", "not in"):
            return [("id", "=", False)]
        values = {bool(v) for v in value}
        wanted = values if operator == "in" else {True, False} - values
        if not wanted:
            return [("id", "=", False)]
        if wanted == {True, False}:
            return [("id", "!=", False)]
        cutoff = fields.Datetime.subtract(
            fields.Datetime.now(), days=self._late_after_days()
        )
        late_ids = (
            self.sudo()
            .search(
                [
                    ("status", "in", ["waiting", "pending"]),
                    ("create_date", "<", cutoff),
                ]
            )
            .ids
        )
        return [("id", "in" if True in wanted else "not in", late_ids)]

    @api.depends("res_id", "model")
    def _compute_related_model_instance(self):
        for record in self:
            ref = False
            if record.res_id:
                ref = f"{record.model},{record.res_id}"
            record.related_model_instance = ref

    @api.model
    def _selection_related_model_instance(self):
        # Restrict the Reference selection to models that actually carry
        # tier validation. Avoids the pylint `no-search-all` warning and
        # mirrors the domain used in `tier.definition.model_id`.
        model_names = self.env["tier.definition"]._get_tier_validation_model_names()
        if not model_names:
            return []
        models = self.env["ir.model"].sudo().search([("model", "in", model_names)])
        return [(model.model, model.name) for model in models]

    def open_origin(self):
        self.ensure_one()
        vid = self.env[self.model].browse(self.res_id).get_formview_id()
        response = {
            "type": "ir.actions.act_window",
            "res_model": self.model,
            "view_mode": "form",
            "res_id": self.res_id,
            "target": "current",
            "views": [(vid, "form")],
        }
        return response

    @api.model
    def _search(self, domain, *args, **kwargs):
        # Forward arbitrary kwargs to super() (the v19 ORM keeps adding
        # them: ``bypass_access``, ``active_test``, ...). When the caller
        # has explicitly opted out of ACL or is the superuser, skip the
        # board's per-document filter -- the board filter is itself an
        # ACL, so bypass_access=True should bypass it too.
        if kwargs.get("bypass_access") or self.env.is_superuser():
            return super()._search(domain, *args, **kwargs)
        query = super()._search(domain, *args, **kwargs)
        ids = self.browse(query).ids
        if not ids:
            return query

        super().check_access("read")

        self.flush_model(["model", "res_id"])
        reviews_to_check = []
        for sub_ids in split_every(self.env.cr.IN_MAX, ids):
            self.env.cr.execute(
                SQL(
                    """
                SELECT DISTINCT review.id, review.model, review.res_id
                FROM %(table)s review
                WHERE review.id = ANY (%(ids)s) AND review.res_id != 0""",
                    table=SQL.identifier(self._table),
                    ids=list(sub_ids),
                )
            )
            reviews_to_check += self.env.cr.dictfetchall()

        review_to_documents = {}
        for review in reviews_to_check:
            review_to_documents.setdefault(review["model"], set()).add(review["res_id"])

        allowed_ids = set()
        for doc_model, doc_ids in review_to_documents.items():
            if doc_model not in self.env:
                # Left behind by an uninstalled module: no document to show.
                continue
            doc_operation = "read"
            DocumentModel = self.env[doc_model].with_user(self.env.uid)
            right = DocumentModel.has_access(doc_operation)
            if right:
                valid_docs = DocumentModel.browse(doc_ids)._filtered_access(
                    doc_operation
                )
                valid_doc_ids = set(valid_docs.ids)
                allowed_ids.update(
                    review["id"]
                    for review in reviews_to_check
                    if review["model"] == doc_model
                    and review["res_id"] in valid_doc_ids
                )

        id_list = [id for id in ids if id in allowed_ids]

        return super()._search([("id", "in", id_list)], *args, **kwargs)

    # NOTE: previous Odoo versions overrode ``_read_group_raw`` here to
    # re-apply the same per-document ACL the ``_search`` override above
    # enforces -- needed because the read_group path used to bypass
    # ``_search``. From Odoo 17 onwards ``_read_group_raw`` is gone and
    # ``_read_group`` routes through ``_search`` internally, so the
    # ``_search`` override already covers the read_group case and the
    # explicit override is no longer required.
