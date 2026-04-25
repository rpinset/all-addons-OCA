# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpHostType(models.Model):
    _name = "vcp.host.type"
    _description = "Vcp Host Type"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    code_kind = fields.Char(required=True)
    active = fields.Boolean(default=True)
