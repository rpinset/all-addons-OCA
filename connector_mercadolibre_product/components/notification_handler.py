# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class MercadoLibreItemsNotificationHandler(Component):
    _name = "mercadolibre.notification.handler.items"
    _inherit = "mercadolibre.notification.handler"
    _apply_on = "mercadolibre.notification"
    _usage = "notification.handler"
    _topic = "items"

    def handle(self):
        notification = self.work.notification
        item_id = self._resource_id(notification.resource, "items")
        backend = notification.backend_id
        description = self.env._(
            "Import Mercado Libre item %(item)s",
            item=item_id,
        )
        backend.with_delay(
            identity_key=f"meli:item:{backend.id}:{item_id}:",
            description=description,
        )._job_import_item(item_id)
        notification.write({"state": "done", "error_message": False})

    def _resource_id(self, resource, marker):
        parts = [part for part in (resource or "").split("/") if part]
        if marker in parts:
            index = parts.index(marker) + 1
            if index < len(parts):
                return parts[index]
        return parts[-1] if parts else ""


class MercadoLibreStockNotificationHandler(Component):
    _name = "mercadolibre.notification.handler.stock"
    _inherit = "mercadolibre.notification.handler"
    _apply_on = "mercadolibre.notification"
    _usage = "notification.handler"
    _topic = "stock-location"

    def handle(self):
        notification = self.work.notification
        adapter = self.component(
            usage="backend.adapter",
            model_name="mercadolibre.product.product",
        )
        payload = adapter.read_stock(notification.resource)
        binding = self._binding(notification, payload)
        if not binding:
            notification.write({"state": "skipped", "error_message": False})
            return
        binding.write(
            {
                "marketplace_qty": self._quantity(payload),
                "state": "synced",
                "error_message": False,
            }
        )
        notification.write({"state": "done", "error_message": False})

    def _quantity(self, payload):
        if not isinstance(payload, dict):
            return 0.0
        if "available_quantity" in payload:
            return payload.get("available_quantity") or 0.0
        locations = payload.get("locations") or []
        if locations:
            return sum(location.get("quantity") or 0.0 for location in locations)
        return payload.get("quantity") or 0.0

    def _binding(self, notification, payload):
        bindings = self.env["mercadolibre.product.product"]
        backend = notification.backend_id
        user_product_id = False
        if isinstance(payload, dict):
            user_product_id = payload.get("user_product_id")
        parts = [part for part in (notification.resource or "").split("/") if part]
        if not user_product_id and "user-products" in parts:
            index = parts.index("user-products") + 1
            if index < len(parts):
                user_product_id = parts[index]
        if user_product_id:
            found = bindings.search(
                [
                    ("backend_id", "=", backend.id),
                    ("user_product_id", "=", user_product_id),
                ],
                limit=1,
            )
            if found:
                return found
        if "items" in parts:
            item_id = parts[parts.index("items") + 1]
            return bindings.search(
                [
                    ("backend_id", "=", backend.id),
                    ("external_id", "=", item_id),
                ],
                limit=1,
            )
        return bindings.browse()
