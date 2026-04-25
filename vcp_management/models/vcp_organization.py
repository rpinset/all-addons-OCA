# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpOrganization(models.Model):
    """
    An organization on a platform, e.g. a GitHub organization or GitLab group.
    It is not the organization that we manage, it represents organization that relates
    somehow with our platform.
    For example, if we manage GitHub repositories, these are GitHub organizations.
    In GitLab, these are GitLab groups.

    They can be related to partners.
    """

    _name = "vcp.organization"
    _description = "Organization"

    name = fields.Char(required=True, readonly=True)
    external_id = fields.Char(required=True, readonly=True, index=True)
    host_id = fields.Many2one(
        comodel_name="vcp.host",
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
    )

    _sql_constraints = [
        (
            "external_id_uniq",
            "unique(external_id, host_id)",
            "External ID must be unique.",
        )
    ]

    def _get_contributor_url(self):
        return False

    def _get_contributors_name(self, kind, **kwargs):
        return self.partner_id.name or self.name
