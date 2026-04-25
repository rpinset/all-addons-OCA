# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class VcpRepository(models.Model):
    """
    Repository of code
    """

    _name = "vcp.repository"
    _description = "Repository"

    name = fields.Char(required=True, index=True)
    description = fields.Char(readonly=True)
    platform_id = fields.Many2one(
        comodel_name="vcp.platform",
        required=True,
    )
    created_at = fields.Datetime(readonly=True)
    last_commit_date = fields.Datetime(readonly=True)
    fetch_branch_pattern = fields.Char(
        help="Regular Expression. If set, only branches whose names are matching"
        " the pattern will be fetched. You can define that value at platform level."
    )
    stargazers_count = fields.Integer(readonly=True)
    is_fork = fields.Boolean(
        readonly=True,
        help="Specify if the repo is a Source or a Fork repository",
    )
    fork_count = fields.Integer(readonly=True)
    watchers_count = fields.Integer(readonly=True)
    from_date = fields.Datetime(required=True)
    request_ids = fields.One2many("vcp.request", inverse_name="repository_id")
    request_count = fields.Integer(compute="_compute_request_count")
    test_field = fields.Char()  # TODO remove after testing
    active = fields.Boolean(default=True, readonly=True)
    scheduled_information_update = fields.Boolean(
        compute="_compute_scheduled_information_update",
        store=True,
        readonly=False,
        help="If checked, the cron that update repository informations"
        " will look for up to date information, for this repository."
        " This update include the recovery of requests, comments and reviews.",
    )
    scheduled_branch_update = fields.Boolean(
        compute="_compute_scheduled_branch_update",
        store=True,
        readonly=False,
        help="If checked, the cron that update repository branches"
        " will look for up to date branches, for this repository.",
    )
    branch_update_date = fields.Datetime(
        readonly=True, required=True, default=fields.Datetime.now
    )
    local_path = fields.Char(compute="_compute_local_path")
    rule_ids = fields.Many2many(
        "vcp.rule",
        string="Processing Rules",
    )
    override_parent_rules = fields.Boolean()
    branch_ids = fields.One2many(
        "vcp.repository.branch",
        inverse_name="repository_id",
    )
    branch_count = fields.Integer(compute="_compute_branch_count", store=True)

    def _get_rules(self):
        rules = self.rule_ids
        if not self.override_parent_rules:
            rules |= self.platform_id.rule_ids
        return rules

    @api.depends("platform_id.local_path", "name")
    def _compute_local_path(self):
        for record in self:
            record.local_path = f"{record.platform_id.local_path}/{record.name}"

    @api.depends("platform_id")
    def _compute_scheduled_information_update(self):
        for record in self:
            record.scheduled_information_update = (
                record.platform_id.default_repository_scheduled_information_update
            )

    @api.depends("platform_id")
    def _compute_scheduled_branch_update(self):
        for record in self:
            record.scheduled_branch_update = (
                record.platform_id.default_repository_scheduled_branch_update
            )

    @api.depends("request_ids")
    def _compute_request_count(self):
        for record in self:
            record.request_count = len(record.request_ids)

    @api.depends("branch_ids")
    def _compute_branch_count(self):
        for record in self:
            record.branch_count = len(record.branch_ids)

    def update_branches(self):
        self.ensure_one()
        now = fields.Datetime.now()
        getattr(self, f"_update_branches_{self.platform_id.kind}")()
        self.branch_update_date = now

    def force_update_information(self):
        self.update_information(update_interval_days=365)

    def update_information(self, update_interval_days=None):
        self.ensure_one()
        getattr(self, f"_update_information_{self.platform_id.kind}")(
            update_interval_days=update_interval_days
        )

    def _cron_update_repositories(self, limit):
        repositories = self.search(
            [("scheduled_information_update", "=", True)],
            limit=limit,
            order="from_date ASC",
        )
        for repository in repositories:
            repository.update_information()

    def _cron_update_branches(self, limit):
        repositories = self.search(
            [("scheduled_branch_update", "=", True)],
            limit=limit,
            order="branch_update_date ASC",
        )
        for repository in repositories:
            repository.update_branches()

    def _get_repository_url(self):
        self.ensure_one()
        return False
