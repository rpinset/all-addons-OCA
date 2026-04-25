# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

_STATUS_SELECTION = [
    ("draft", "Draft"),
    ("open", "Open"),
    ("merged", "Merged"),
    ("closed", "Closed"),
]


class VcpRequest(models.Model):
    """
    Request of changes on a repository, e.g. pull request on GitHub
    or merge request on GitLab.
    """

    _name = "vcp.request"
    _description = "Code Request"

    external_id = fields.Char(string="Externa ID", readonly=True, index=True)
    name = fields.Char(readonly=True)
    user_id = fields.Many2one(
        comodel_name="vcp.user",
        string="Contributor",
        readonly=True,
    )
    partner_id = fields.Many2one(
        related="user_id.partner_id",
    )
    repository_id = fields.Many2one(
        comodel_name="vcp.repository",
        readonly=True,
        ondelete="cascade",
    )
    branch_id = fields.Many2one(
        comodel_name="vcp.branch",
        readonly=True,
        ondelete="restrict",
    )
    organization_id = fields.Many2one(
        comodel_name="vcp.organization",
        readonly=True,
    )
    partner_organization_id = fields.Many2one(
        related="organization_id.partner_id",
        string="Organization Partner",
    )
    review_ids = fields.One2many(
        comodel_name="vcp.review",
        string="Reviews",
        readonly=True,
        inverse_name="request_id",
    )
    review_count = fields.Integer(compute="_compute_review_count", store=True)
    comment_ids = fields.One2many(
        comodel_name="vcp.comment",
        string="Comments",
        readonly=True,
        inverse_name="request_id",
    )
    comment_count = fields.Integer(compute="_compute_comment_count", store=True)
    url = fields.Char(readonly=True)
    state = fields.Char(readonly=True)
    status = fields.Selection(
        selection=_STATUS_SELECTION, compute="_compute_status", store=True
    )
    is_merged = fields.Boolean(readonly=True)
    is_draft = fields.Boolean(readonly=True)
    created_at = fields.Datetime(readonly=True)
    updated_at = fields.Datetime(readonly=True)
    closed_at = fields.Datetime(readonly=True)
    number = fields.Integer(readonly=True)
    label_ids = fields.Many2many(
        comodel_name="vcp.request.label",
        string="Labels",
        readonly=True,
    )
    commits = fields.Integer(readonly=True)
    additions = fields.Integer(readonly=True)
    deletions = fields.Integer(readonly=True)
    total_comments = fields.Integer(readonly=True)
    review_comments = fields.Integer(readonly=True)

    _sql_constraints = [
        ("external_id_uniq", "unique(external_id)", "External ID must be unique.")
    ]

    @api.depends("review_ids")
    def _compute_review_count(self):
        for record in self:
            record.review_count = len(record.review_ids)

    @api.depends("comment_ids")
    def _compute_comment_count(self):
        for record in self:
            record.comment_count = len(record.comment_ids)

    @api.depends("is_draft", "is_merged", "state")
    def _compute_status(self):
        for record in self:
            if record.is_merged:
                record.status = "merged"
            elif record.closed_at:
                record.status = "closed"
            elif record.is_draft:
                record.status = "draft"
            else:
                record.status = "open"
