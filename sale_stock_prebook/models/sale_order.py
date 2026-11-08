# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    stock_is_reserved = fields.Boolean(
        compute="_compute_stock_is_reserved",
        store=True,
    )

    def _get_reservation_pickings(self):
        return self.picking_ids.filtered(
            lambda p: any(m.used_for_sale_reservation for m in p.move_ids)
        )

    @api.depends("picking_ids.move_ids.used_for_sale_reservation")
    def _compute_stock_is_reserved(self):
        for rec in self:
            rec.stock_is_reserved = (rec._get_reservation_pickings() and True) or False

    def _action_cancel(self):
        self.release_reservation()
        return super()._action_cancel()

    def action_confirm(self):
        self.release_reservation()
        return super().action_confirm()

    def _prepare_reserve_stock_reference_values(self):
        self.ensure_one()
        return {"name": f"Reservation for {self.name}"}

    def _create_reserve_stock_reference(self):
        return self.env["stock.reference"].create(
            self._prepare_reserve_stock_reference_values()
        )

    def reserve_stock(self):
        self = self.filtered(
            lambda s: not s.stock_is_reserved
            and s.state in ["draft", "sent"]
            or not s.order_line
        )
        if not self:
            return

        self = self.with_context(sale_stock_prebook_stop_proc_run=True)
        procurements = []

        for order in self:
            lines = order.order_line.filtered(lambda line: line._should_prebook_stock())
            if not lines:
                continue
            reference = order._create_reserve_stock_reference()
            procurements += lines._prepare_reserve_procurements(reference)
        if procurements:
            self.env["stock.rule"].run(procurements)

    def release_reservation(self):
        pickings = self._get_reservation_pickings()
        if pickings:
            pickings.action_cancel()
            pickings.reference_ids.sudo().unlink()
            pickings.sudo().unlink()
