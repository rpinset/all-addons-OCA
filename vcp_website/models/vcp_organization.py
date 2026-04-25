# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class VcpOrganization(models.Model):
    _inherit = "vcp.organization"

    def _get_contributor_url(self):
        result = super()._get_contributor_url()
        if (
            not result
            and self.partner_id
            and self.partner_id.is_published
            and self.partner_id.website_url
        ):
            return self.partner_id.website_url
        return result
