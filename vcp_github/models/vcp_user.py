# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class VcpUser(models.Model):
    _inherit = "vcp.user"

    def _get_contributor_url(self):
        result = super()._get_contributor_url()
        if not result and self.host_id.type_id.code == "github":
            return f"https://github.com/{self.external_id}"
        return result
