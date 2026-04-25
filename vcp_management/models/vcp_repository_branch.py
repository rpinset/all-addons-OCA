# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class VcpRepositoryBranch(models.Model):
    _name = "vcp.repository.branch"
    _inherit = ["vcp.rule.information.mixin"]
    _description = "Links Branches with Repositories"

    branch_id = fields.Many2one(
        "vcp.branch",
        string="Branch",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    repository_id = fields.Many2one(
        "vcp.repository",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    platform_id = fields.Many2one(
        related="repository_id.platform_id",
        readonly=True,
    )
    last_commit = fields.Char(readonly=True)
    rule_ids = fields.Many2many(
        "vcp.rule",
        string="Processing Rules",
    )
    override_parent_rules = fields.Boolean()
    update_rule_processing_date = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
    )

    def _cron_process_branch_rules(self, limit):
        branches = self.search([], limit=limit, order="update_rule_processing_date asc")
        for branch in branches:
            branch.process_rules()

    @api.constrains("branch_id", "repository_id")
    def _check_branch_repository(self):
        for record in self:
            if record.branch_id.platform_id != record.repository_id.platform_id:
                raise ValidationError(
                    _("The branch and the repository must belong to the same platform.")
                )

    def _get_rules(self):
        rules = self.rule_ids
        if not self.override_parent_rules:
            rules |= self.repository_id._get_rules()
        return rules

    def _get_local_path(self):
        return f"{self.repository_id.local_path}/{self.branch_id.name}"

    def process_rules(self):
        for record in self:
            rules = record._get_rules()
            # This parameters dict can be used to store parameters that will
            # be used by other rules.
            parameters = {}
            for rule in rules:
                if re.match(rule.branch_pattern, record.branch_id.name):
                    rule._process_rule(record, parameters)

    def _download_code(self):
        result = super()._download_code()
        local_path = self.local_path
        try:
            os.makedirs(local_path, exist_ok=True)
        except PermissionError as err:
            raise ValidationError(
                _(
                    "Unable to create a folder in '%(local_path)s'.",
                    local_path=local_path,
                )
            ) from err
        code_kind = self.repository_id.platform_id.host_id.type_id.code_kind
        getattr(self, f"_download_code_{code_kind}")(local_path)
        return result

    def _compute_display_name(self):
        if not self._context.get("display_only_branch_name"):
            return super()._compute_display_name()

        for record in self:
            record.display_name = record.branch_id.name
