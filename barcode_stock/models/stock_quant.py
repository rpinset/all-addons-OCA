# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_apply_inventory(self):
        for quant in self:
            if quant.product_id.tracking in ("lot", "serial") and not quant.lot_id:
                raise UserError(
                    _(
                        "A lot/serial number is required for product %(product)s "
                        "before applying the inventory adjustment.",
                        product=quant.product_id.display_name,
                    )
                )
        return super().action_apply_inventory()

    def action_apply_inventory_from_scanner(self):
        if not self:
            raise UserError(_("No inventory lines to apply."))
        # Go through action_apply_inventory so the scanner path enforces the same
        # guards as the back office (lot requirement plus core's checks).
        return self.action_apply_inventory()
