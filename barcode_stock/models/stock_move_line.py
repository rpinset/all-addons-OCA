# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    validated_on_date = fields.Datetime()

    @api.constrains("quantity", "product_id", "lot_id")
    def _check_serial_quantity(self):
        for line in self:
            if line.product_id.tracking == "serial" and line.quantity > 1:
                raise ValidationError(
                    _(
                        "The quantity for product %(product)s (tracked by serial) "
                        "cannot exceed 1.",
                        product=line.product_id.display_name,
                    )
                )
