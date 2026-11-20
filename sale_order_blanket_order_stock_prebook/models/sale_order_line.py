# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _release_reservation(self):
        """Release the reservation of the stock for the order."""
        self.move_ids.filtered(lambda m: m.used_for_sale_reservation)._action_cancel()

    def _prepare_reserve_procurement_values(self, reference):
        values = super()._prepare_reserve_procurement_values(reference)
        # The reservation is made for the blanket order, not for the call-off
        # order being processed when the reservation is updated.
        values["call_off_sale_line_id"] = False
        return values

    def _prepare_reserve_procurements(self, reference):
        procurements = super()._prepare_reserve_procurements(reference)
        forced_qty = self.env.context.get("force_qty")
        if forced_qty:
            self.ensure_one()
            proc = procurements[0]
            product_qty, procurement_uom = self.product_uom_id._adjust_uom_quantities(
                forced_qty, self.product_id.uom_id
            )
            proc = self.env["stock.rule"].Procurement(
                proc.product_id,
                product_qty,
                procurement_uom,
                proc.location_id,
                proc.name,
                proc.origin,
                proc.company_id,
                values=proc.values,
            )
            procurements = [proc]
        return procurements

    def _prebook_stock_for_call_off_remaining_qty(self, previous_product_uom_qty=None):
        """Prebook the stock for qty remaining to call off."""
        previous_product_uom_qty = previous_product_uom_qty or {}
        self = self.with_context(sale_stock_prebook_stop_proc_run=True)
        procurements = []
        lines_by_order = defaultdict(self.browse)
        for line in self:
            lines_by_order[line.order_id] |= line
        for order, lines in lines_by_order.items():
            reference = None
            for line in lines:
                if line.id in previous_product_uom_qty:
                    line._release_reservation()
                remaining_qty = line.call_off_remaining_qty
                if (
                    line.product_uom_id.compare(remaining_qty, 0) > 0
                    and line._should_prebook_stock()
                ):
                    if not reference:
                        reference = order._get_or_create_reserve_stock_reference()
                    procurements += line.with_context(
                        force_qty=remaining_qty
                    )._prepare_reserve_procurements(reference)
        if procurements:
            self.env["stock.rule"].run(procurements)
        return procurements

    def _launch_stock_rule_for_call_off_line_qty(
        self, qty_to_deliver, previous_product_uom_qty
    ):  # pylint: disable=missing-return
        self.ensure_one()
        reservation_strategy = self.order_id.blanket_reservation_strategy
        if reservation_strategy == "at_confirm":
            self._release_reservation()
            # Create a new reservation for the remaining quantity on the blanket order
            # Since the call_off_remaining qty is computed from the qty consumed by
            # the call off order and the current line is part of this qty, it
            # represents the real remaining qty to consume and therefore the qty to
            # reserve on the blanket order.
            self._prebook_stock_for_call_off_remaining_qty(previous_product_uom_qty)

            # run normal delivery rule on the blanket order. This will create the
            # move on the call off order for the qty not reserved IOW the qty to
            # deliver.
            self.with_context(
                disable_call_off_stock_rule=True
            )._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty
            )
        else:
            super()._launch_stock_rule_for_call_off_line_qty(
                qty_to_deliver, previous_product_uom_qty
            )

    def _action_launch_stock_rule(self, *, previous_product_uom_qty=False):
        previous_product_uom_qty = previous_product_uom_qty or {}
        lines_to_update_reservation = self.filtered(
            lambda line: line.order_type == "blanket"
            and line.id in previous_product_uom_qty
            and line.order_id.blanket_reservation_strategy == "at_confirm"
        )
        lines_to_update_reservation._prebook_stock_for_call_off_remaining_qty(
            previous_product_uom_qty
        )
        others_lines = self - lines_to_update_reservation
        return super(SaleOrderLine, others_lines)._action_launch_stock_rule(
            previous_product_uom_qty=previous_product_uom_qty
        )
