# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class VcpRepository(models.Model):
    _inherit = "vcp.repository"

    def _get_git_url(self):
        self.ensure_one()
        return self.platform_id._get_git_url(self)
