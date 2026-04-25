# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
import os
from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models, tools

_logger = logging.getLogger(__name__)


class VcpPlatform(models.Model):
    """
    This model should define how to interact with a Version Control Platform
    (VCP) such as GitHub, GitLab, etc.
    1 platform should correspond to 1 organization/account on the VCP.
    """

    _name = "vcp.platform"
    _inherit = ["image.mixin"]
    _description = "VCP Platform"

    name = fields.Char(required=True)
    description = fields.Char(readonly=True)
    short_description = fields.Char(readonly=True)
    last_update = fields.Datetime(readonly=True)
    active = fields.Boolean(default=True)
    update_interval_days = fields.Integer(default=3)
    branch_ids = fields.One2many(
        "vcp.branch",
        inverse_name="platform_id",
    )
    host_id = fields.Many2one(
        "vcp.host",
        required=True,
    )
    kind = fields.Char(related="host_id.type_id.code")
    key_ids = fields.One2many(
        comodel_name="vcp.platform.key",
        inverse_name="platform_id",
        string="API Keys",
    )
    repository_ids = fields.One2many(
        "vcp.repository",
        inverse_name="platform_id",
    )
    repository_count = fields.Integer(compute="_compute_repository_count", store=True)
    default_repository_scheduled_information_update = fields.Boolean(
        help="If checked, the cron that update repositories"
        " will look for up to date information, for this repository.",
    )
    default_repository_scheduled_branch_update = fields.Boolean(
        help="If checked, the cron that update repository branches"
        " will look for up to date branches, for this repository.",
    )
    scheduled_information_update = fields.Boolean(
        default=True,
        help="If checked, the cron that update platform informations"
        " will look for up to date information, for this platform.",
    )
    fetch_repository_fork = fields.Boolean(
        help="If checked, all repositories will be fetched (sources and forks)."
        " Otherwise, only sources repositories will be fetched"
    )
    fetch_repository_archived = fields.Boolean(
        help="If checked, all repositories will be fetched (actives and archived)."
        " Otherwise, only active repositories will be fetched"
    )
    fetch_repository_branch_pattern = fields.Char(
        help="Regular Expression. If set, only branches whose names are matching"
        " the pattern will be fetched, when fetching branches of the repositories"
        " of the platform."
    )
    local_path = fields.Char(compute="_compute_local_path")
    rule_ids = fields.Many2many(
        "vcp.rule",
        string="Processing Rules",
    )

    def _get_source_path(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("vcp_management.source_code_local_path", "")
            or tools.config.get("source_code_local_path", "")
            or os.environ.get("SOURCE_CODE_LOCAL_PATH", "")
        )

    @api.depends()
    def _compute_local_path(self):
        source_path = self._get_source_path()
        for record in self:
            record.local_path = f"{source_path}/{record.id}"

    @api.depends("repository_ids")
    def _compute_repository_count(self):
        for record in self:
            record.repository_count = len(record.repository_ids)

    def update_information(self):
        self.ensure_one()
        getattr(self, f"_update_information_{self.kind}")()
        self.last_update = fields.Datetime.now()

    def _cron_update_platforms(self):
        for platform in self.search([("scheduled_information_update", "=", True)]):
            try:
                platform.update_information()
            except Exception as e:
                _logger.error("Error updating platform %s: %s", platform.name, str(e))
                raise e

    @tools.ormcache("self.id", "name")
    def _get_branch(self, name):
        self.ensure_one()
        branch = self.env["vcp.branch"].search(
            [("platform_id", "=", self.id), ("name", "=", name)],
            limit=1,
        )
        if not branch:
            branch = (
                self.env["vcp.branch"]
                .sudo()
                .create(
                    {
                        "platform_id": self.id,
                        "name": name,
                    }
                )
            )
        return branch.id

    def _get_merged_domain(self, start, end, **values):
        return [
            ("repository_id.platform_id", "in", self.ids),
            ("is_merged", "=", True),
            ("closed_at", ">=", start),
            ("closed_at", "<", end),
        ]

    def _get_created_domain(self, start, end, **values):
        return [
            ("repository_id.platform_id", "in", self.ids),
            ("created_at", ">=", start),
            ("created_at", "<", end),
        ]

    def _get_comments_domain(self, start, end, **values):
        return [
            ("request_id.repository_id.platform_id", "in", self.ids),
            ("created_at", ">=", start),
            ("created_at", "<", end),
        ]

    def _get_reviews_domain(self, start, end, **values):
        return [
            ("request_id.repository_id.platform_id", "in", self.ids),
            ("submitted_at", ">=", start),
            ("submitted_at", "<", end),
        ]

    def _get_default_data(self, start, end, field, kind, **values):
        return {
            "name": "",
            "created_requests": 0,
            "merged_requests": 0,
            "comments": 0,
            "reviews": 0,
            "developers": 0,
        }

    def _generate_data(self, start, end, field, kind, extra_domain=None, **values):
        if extra_domain is None:
            extra_domain = []
        default_dict = self._get_default_data(start, end, field, kind, **values)
        data = defaultdict(lambda: default_dict.copy())
        if not field:
            return data
        for merged in (
            self.env["vcp.request"]
            .sudo()
            .read_group(
                self._get_merged_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[merged[field][0]]["merged_requests"] = merged[f"{field}_count"]
        for pr in (
            self.env["vcp.request"]
            .sudo()
            .read_group(
                self._get_created_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field, "user_id:count_distinct"] if field != "user_id" else [field],
                [field],
            )
        ):
            data[pr[field][0]]["created_requests"] = pr[f"{field}_count"]
            if field != "user_id":
                data[pr[field][0]]["developers"] = pr["user_id"]
        for comment in (
            self.env["vcp.comment"]
            .sudo()
            .read_group(
                self._get_comments_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[comment[field][0]]["comments"] = comment[f"{field}_count"]
        for review in (
            self.env["vcp.review"]
            .sudo()
            .read_group(
                self._get_reviews_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[review[field][0]]["reviews"] = review[f"{field}_count"]
        return data

    def _get_dates(self, year, month, period, **values):
        if month == 12:
            end = datetime(year + 1, 1, 1, 0, 0, 0)
        else:
            end = datetime(year, month + 1, 1, 0, 0, 0)
        if period == "YTD":
            start = datetime(year, 1, 1, 0, 0, 0)
        elif period == "MAT":
            start = end - relativedelta(years=1)
        else:
            start = datetime(year, month, 1, 0, 0, 0)
        return start, end

    def _get_vcp_columns(self, kind):
        """
        Returns the columns to display in the VCP contributors view in Portal
        We keep it here to avoid glue modules having to override models just to
        add columns.
        """
        if kind == "contributors":
            return [
                {"field": "name", "title": _("Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        elif kind == "organizations":
            return [
                {"field": "name", "title": _("Organization Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "developers",
                    "title": _("Developers"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        elif kind == "repositories":
            return [
                {"field": "name", "title": _("Repository Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "developers",
                    "title": _("Developers"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        return []

    def _improve_vcp_data(self, data, kind, **kwargs):
        """
        This method improves the raw data generated by _generate_data by adding
        names and URLs for each key (contributor, organization, repository).
        It is kept here to avoid glue modules having to override models just to
        add extra information
        """
        for key, values in data.items():
            if kind == "contributors":
                partner = self.env["vcp.user"].browse(key)
                values["name"] = partner._get_contributors_name(kind, **kwargs)
                values["url"] = partner._get_contributor_url()
            elif kind == "organizations":
                organization = self.env["vcp.organization"].browse(key)
                values["name"] = organization._get_contributors_name(kind, **kwargs)
                values["url"] = organization._get_contributor_url()
            elif kind == "repositories":
                repository = self.env["vcp.repository"].browse(key)
                values["name"] = repository.name
                values["url"] = repository._get_repository_url()
        return data
