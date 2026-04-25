# Copyright 2025 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        new_self = self.with_context(sale_prebook_check_exceptions=True)
        return super(SaleOrder, new_self).action_confirm()

    def release_reservation(self):
        if self.env.context.get("sale_prebook_check_exceptions"):
            if self.detect_exceptions():
                return
        super().release_reservation()
