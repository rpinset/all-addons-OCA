# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @property
    def _release_channel_possible_candidate_domain_apply_extras(self):
        """Do not apply extra domains when the delivery date is forced on the SO"""
        if self.sale_id.commitment_date:
            return False
        return super()._release_channel_possible_candidate_domain_apply_extras

    @api.depends("group_id")
    def _compute_delivery_date(self):
        # when there is an SO commitment date, always use that one as delivery date
        for picking in self:
            channel = picking.release_channel_id
            if not channel or picking.need_release:
                super(StockPicking, picking)._compute_delivery_date()
                continue
            commitment_date_dt = picking.group_id.sale_id.commitment_date
            if commitment_date_dt:
                picking.delivery_date = channel._localize(commitment_date_dt).date()
            else:
                super(StockPicking, picking)._compute_delivery_date()
        return
