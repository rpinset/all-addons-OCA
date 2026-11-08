# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class MercadoLibreSaleStatusMapper(Component):
    """Map a Mercado Libre status onto the sales order.

    Override ``apply`` for a different confirmation rule. Paid orders stay
    in draft so ``sale_automatic_workflow`` can confirm them.
    """

    _name = "mercadolibre.sale.status.mapper"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "status.mapper"

    def payment_status(self, payload):
        if not isinstance(payload, dict):
            return False
        if payload.get("order_id") or isinstance(payload.get("order"), dict):
            return payload.get("status") or False
        payments = payload.get("payments") or []
        if payments and isinstance(payments[0], dict):
            return payments[0].get("status") or False
        return False

    def sale_fee(self, payload):
        total = 0.0
        for line in payload.get("order_items") or []:
            total += line.get("sale_fee") or 0.0
        return total

    def order_id(self, payload):
        if not isinstance(payload, dict):
            return False
        if payload.get("order_id"):
            return str(payload["order_id"])
        order = payload.get("order")
        if isinstance(order, dict) and order.get("id"):
            return str(order["id"])
        return False

    def apply(self, binding, payload):
        status = payload.get("status")
        payment = self.payment_status(payload)
        values = {}
        if status and not self.order_id(payload):
            values["order_status"] = status
        if payment:
            values["payment_status"] = payment
        if values:
            binding.write(values)
        if binding.order_status == "cancelled":
            self._cancel_sale_order(binding.odoo_id)

    def _cancel_sale_order(self, order):
        if not order or order.state == "cancel":
            return
        done = order.picking_ids.filtered(lambda picking: picking.state == "done")
        if done:
            return
        if order.state in ("draft", "sent", "sale"):
            order.with_context(disable_cancel_warning=True).action_cancel()
