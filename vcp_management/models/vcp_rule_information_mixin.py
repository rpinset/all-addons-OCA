# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class VcpRuleInformation(models.AbstractModel):
    _name = "vcp.rule.information.mixin"
    _description = "Mixin to link rule information models"

    rule_information_ids = fields.One2many(
        "vcp.rule.information",
        inverse_name="res_id",
        domain=lambda self: [("res_model", "=", self._name)],
    )
    local_path = fields.Char(compute="_compute_local_path")

    def _download_code(self):
        """To be implemented on each subclass"""
        self.ensure_one()

    def _compute_local_path(self):
        for record in self:
            record.local_path = record._get_local_path()

    def _get_local_path(self):
        """To be implemented on each subclass"""
        return False
