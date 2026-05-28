# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import base64

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vcp_merged_requests = fields.Integer(
        compute="_compute_vcp_contributions",
        string="Merged Requests",
        prefetch=False,
    )
    vcp_created_requests = fields.Integer(
        compute="_compute_vcp_contributions",
        string="Created Requests",
        prefetch=False,
    )
    vcp_comments = fields.Integer(
        compute="_compute_vcp_contributions", string="Comments", prefetch=False
    )
    vcp_reviews = fields.Integer(
        compute="_compute_vcp_contributions", string="Reviews", prefetch=False
    )
    vcp_user_ids = fields.One2many(
        "vcp.user",
        inverse_name="partner_id",
    )
    vcp_organization_ids = fields.One2many(
        "vcp.organization",
        inverse_name="partner_id",
    )
    image_1920 = fields.Image(
        compute="_compute_image_1920",
        store=True,
        readonly=False,
    )

    @api.depends(
        "vcp_user_ids.sync_image_to_partner",
        "vcp_user_ids.avatar_url",
    )
    def _compute_image_1920(self):
        for record in self:
            sync_user = record.vcp_user_ids.filtered("sync_image_to_partner")
            if len(sync_user) > 1:
                raise UserError(
                    self.env._(
                        "Only one Vcp User can be use for synchronising the main image"
                    )
                )
            elif sync_user.avatar_url:
                try:
                    response = requests.get(sync_user.avatar_url, timeout=10)
                    response.raise_for_status()
                except Exception as e:
                    raise UserError(
                        self.env._("Fail to download avatar, %s.please retry".format())
                    ) from e
                record.image_1920 = base64.b64encode(response.content).decode("utf-8")

    @api.depends()
    def _compute_vcp_contributions(self):
        self.filtered(lambda p: p.vcp_user_ids)._compute_vcp_contributions_field(
            "partner_id"
        )
        self.filtered(lambda p: not p.vcp_user_ids)._compute_vcp_contributions_field(
            "partner_organization_id"
        )

    @api.model
    def _get_contributors_field_map(self):
        return {
            "vcp_merged_requests": "merged_requests",
            "vcp_created_requests": "created_requests",
            "vcp_comments": "comments",
            "vcp_reviews": "reviews",
        }

    def _compute_vcp_contributions_field(self, field):
        today = fields.Date.today()
        start, end = self.env["vcp.platform"]._get_dates(today.year, today.month, "MAT")
        data = (
            self.env["vcp.platform"]
            .search([])
            ._generate_data(
                start=start,
                end=end,
                field=field,
                kind="user",
                extra_domain=[(field, "in", self.ids)],
            )
        )
        field_map = self._get_contributors_field_map()
        for partner in self:
            partner.update(
                {key: data[partner.id].get(field_map[key], 0) for key in field_map}
            )
