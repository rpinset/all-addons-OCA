# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpBranch(models.Model):
    """
    Branches of code on our repository
    """

    _name = "vcp.branch"
    _description = "Branch"

    name = fields.Char(required=True)
    platform_id = fields.Many2one(
        comodel_name="vcp.platform",
        string="Platform",
        required=True,
        readonly=True,
    )
    _sql_constraints = [
        ("name_uniq", "unique(name, platform_id)", "Branch name must be unique.")
    ]
