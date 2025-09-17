# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    filter_mode = fields.Selection(
        [("global", "Global"), ("include", "Include"), ("exclude", "Exclude")],
        default="global",
    )
    partner_ids = fields.Many2many("res.partner")

    @api.model
    def _get_compatible_providers(self, company_id, partner_id, *args, **kwargs):
        result = super()._get_compatible_providers(
            company_id, partner_id, *args, **kwargs
        )
        return result.filtered(
            lambda r: not r.filter_mode
            or r.filter_mode == "global"
            or (r.filter_mode == "include" and partner_id in r.partner_ids.ids)
            or (r.filter_mode == "exclude" and partner_id not in r.partner_ids.ids)
        )
