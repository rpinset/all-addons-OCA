# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpHost(models.Model):
    """
    Source of origin of our platform,
    e.g. GitHub, GitLab, My Own Gitlab instance, etc.
    """

    _name = "vcp.host"
    _description = "VCP Host"

    name = fields.Char(required=True)
    type_id = fields.Many2one(
        "vcp.host.type",
    )
    active = fields.Boolean(default=True)

    @tools.ormcache("self.id", "username")
    def _get_user(self, username):
        user = (
            self.env["vcp.user"]
            .with_context(active_test=False)
            .search([("external_id", "=ilike", username)], limit=1)
        )
        if not user:
            user = self.env["vcp.user"].create(
                {
                    "name": username,
                    "external_id": username,
                    "host_id": self.id,
                }
            )
        return user.id

    @tools.ormcache("self.id", "organization")
    def _get_organization(self, organization):
        org = (
            self.env["vcp.organization"]
            .with_context(active_test=False)
            .search([("external_id", "=ilike", organization)], limit=1)
        )
        if not org:
            org = self.env["vcp.organization"].create(
                {
                    "name": organization,
                    "external_id": organization,
                    "host_id": self.id,
                }
            )
        return org.id
