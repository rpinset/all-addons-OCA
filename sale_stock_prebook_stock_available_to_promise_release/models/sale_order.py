# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        moves = self._get_reservation_pickings().move_ids
        if moves:
            date_priority_of_reservation = moves[0].date_priority
            self = self.with_context(
                date_priority_of_reservation=date_priority_of_reservation
            )
        return super().action_confirm()
