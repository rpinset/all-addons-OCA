# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        date_priority_of_reservation = self.env.context.get(
            "date_priority_of_reservation"
        )
        if date_priority_of_reservation:
            values["date_priority"] = date_priority_of_reservation
        return values
