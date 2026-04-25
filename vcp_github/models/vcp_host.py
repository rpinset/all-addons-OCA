# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class VcpHost(models.Model):
    _inherit = "vcp.host"

    @api.constrains("type_id")
    def _check_kind_github(self):
        for record in self.filtered(lambda r: r.type_id.code == "github"):
            platforms = self.search(
                [("id", "!=", record.id), ("type_id.code", "=", "github")],
                limit=1,
            )
            if platforms:
                raise ValidationError(_("Only one GitHub Host type is allowed."))
