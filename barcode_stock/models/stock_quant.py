# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


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

    @api.model
    def barcode_lot_location(self, product_id, lot_id, location_id):
        """Where a lot would be picked from under a location, as Odoo's own
        reservation takes it: the first of its quants there in the order of
        the removal strategy (FIFO, LIFO, closest, FEFO...), one with stock not
        reserved yet if any; otherwise one with stock, whose reservation Odoo
        frees on validation.

        :return: the location as ``[id, display_name]``, or False when the lot
            has no stock there
        """
        product = self.env["product.product"].browse(product_id)
        lot = self.env["stock.lot"].browse(lot_id)
        location = self.env["stock.location"].browse(location_id)
        rounding = product.uom_id.rounding
        quants = self._gather(product, location, lot_id=lot).filtered(
            lambda quant: quant.lot_id == lot
            and float_compare(quant.quantity, 0, precision_rounding=rounding) > 0
        )
        free = quants.filtered(
            lambda quant: float_compare(
                quant.available_quantity, 0, precision_rounding=rounding
            )
            > 0
        )
        quant = (free or quants)[:1]
        if not quant:
            return False
        return [quant.location_id.id, quant.location_id.display_name]
