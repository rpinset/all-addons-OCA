# Copyright 2025 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    priority = fields.Selection(
        related="production_id.priority",
        store=True,
        readonly=True,
    )
