# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpReview(models.Model):
    """
    Reviews of a request, e.g. pull request review on GitHub or
    merge request review on GitLab.
    """

    _name = "vcp.review"
    _description = "Review"  # TODO

    external_id = fields.Char(readonly=True, required=True, index=True)
    body = fields.Html(readonly=True)
    state = fields.Char(readonly=True)
    user_id = fields.Many2one("vcp.user", readonly=True)
    partner_id = fields.Many2one(
        related="user_id.partner_id",
    )
    submitted_at = fields.Datetime(readonly=True)
    repository_id = fields.Many2one(
        related="request_id.repository_id",
        readonly=True,
        store=True,
    )
    request_id = fields.Many2one(
        "vcp.request",
        readonly=True,
        required=True,
        ondelete="cascade",
    )
    organization_id = fields.Many2one(
        related="request_id.organization_id",
        readonly=True,
        store=True,
    )
    platform_id = fields.Many2one(
        related="request_id.repository_id.platform_id",
        readonly=True,
        store=True,
    )
    partner_organization_id = fields.Many2one(
        related="request_id.organization_id.partner_id",
        string="Organization Partner",
    )

    _sql_constraints = [
        ("external_id_uniq", "unique(external_id)", "External ID must be unique.")
    ]
