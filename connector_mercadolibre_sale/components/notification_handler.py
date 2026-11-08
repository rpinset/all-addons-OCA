# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


def _resource_id(resource, marker):
    parts = [part for part in (resource or "").split("/") if part]
    if marker in parts:
        index = parts.index(marker) + 1
        if index < len(parts):
            return parts[index]
    return parts[-1] if parts else ""


def _missing(notification, message):
    notification.write({"state": "error", "error_message": message})


class MercadoLibreOrdersNotificationHandler(Component):
    _name = "mercadolibre.notification.handler.orders"
    _inherit = "mercadolibre.notification.handler"
    _apply_on = "mercadolibre.notification"
    _usage = "notification.handler"
    _topic = "orders_v2"

    def handle(self):
        notification = self.work.notification
        order_id = _resource_id(notification.resource, "orders")
        if not order_id:
            _missing(
                notification,
                self.env._("Mercado Libre order notification has no order id."),
            )
            return
        notification.backend_id._enqueue_order_import(order_id)
        notification.write({"state": "done", "error_message": False})


class MercadoLibreShipmentsNotificationHandler(Component):
    _name = "mercadolibre.notification.handler.shipments"
    _inherit = "mercadolibre.notification.handler"
    _apply_on = "mercadolibre.notification"
    _usage = "notification.handler"
    _topic = "shipments"

    def handle(self):
        notification = self.work.notification
        shipment_id = _resource_id(notification.resource, "shipments")
        if not shipment_id:
            _missing(
                notification,
                self.env._("Mercado Libre shipment notification has no shipment id."),
            )
            return
        notification.backend_id._enqueue_shipment_import(shipment_id)
        notification.write({"state": "done", "error_message": False})


class MercadoLibrePaymentsNotificationHandler(Component):
    _name = "mercadolibre.notification.handler.payments"
    _inherit = "mercadolibre.notification.handler"
    _apply_on = "mercadolibre.notification"
    _usage = "notification.handler"
    _topic = "payments"

    def handle(self):
        notification = self.work.notification
        if not notification.resource:
            _missing(
                notification,
                self.env._("Mercado Libre payment notification has no resource."),
            )
            return
        notification.backend_id._enqueue_payment_import(notification.resource)
        notification.write({"state": "done", "error_message": False})
