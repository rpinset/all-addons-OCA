# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class VcpRuleInformation(models.Model):
    _name = "vcp.rule.information"
    _description = "Information about the processing of a rule on a repository branch"

    res_id = fields.Integer(required=True)
    res_model = fields.Char(required=True)
    rule_id = fields.Many2one(
        "vcp.rule",
        required=True,
    )
    code_count = fields.Integer()
    documentation_count = fields.Integer()
    empty_count = fields.Integer()
    total_count = fields.Integer(store=True, compute="_compute_total_count")
    scanned_files = fields.Integer()

    @api.depends("code_count", "documentation_count", "empty_count")
    def _compute_total_count(self):
        for item in self:
            item.total_count = (
                item.code_count + item.documentation_count + item.empty_count
            )
