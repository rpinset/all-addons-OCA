# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class VcpPlatform(models.Model):
    _inherit = "vcp.platform"

    def _get_git_url(self, repository):
        return getattr(self, f"_get_git_url_{self.kind}")(repository)
