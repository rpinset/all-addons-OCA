# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

LISTING_STATUSES = {"active", "paused", "closed", "under_review", "inactive"}


class MercadoLibreProductImportMapper(Component):
    _name = "mercadolibre.product.import.mapper"
    _inherit = ["mercadolibre.backend.component", "base.import.mapper"]
    _apply_on = "mercadolibre.product.product"
    _usage = "import.mapper"

    @mapping
    def listing(self, record):
        variation = record.get("_variation") or {}
        sku = self._seller_sku(record, variation)
        status = record.get("status") or "active"
        if status not in LISTING_STATUSES:
            status = "inactive"
        quantity = variation.get("available_quantity", record.get("available_quantity"))
        user_product_id = variation.get("user_product_id") or record.get(
            "user_product_id"
        )
        variation_id = variation.get("id")
        shipping = record.get("shipping") or {}
        return {
            "external_id": record.get("id"),
            "variation_id": str(variation_id) if variation_id else False,
            "user_product_id": user_product_id or False,
            "seller_sku": sku or False,
            "listing_status": status,
            "permalink": record.get("permalink") or False,
            "picture_urls": self._picture_urls(record),
            "marketplace_qty": quantity or 0.0,
            "fulfillment": self._is_fulfillment(record, shipping),
            "currency_id": self._currency_id(record.get("currency_id")),
        }

    def _seller_sku(self, record, variation):
        for source in (variation, record):
            if not source:
                continue
            for attribute in source.get("attributes") or []:
                if attribute.get("id") == "SELLER_SKU" and attribute.get("value_name"):
                    return attribute["value_name"]
            custom = source.get("seller_custom_field")
            if custom:
                return custom
        return False

    def _picture_urls(self, record):
        urls = []
        for picture in record.get("pictures") or []:
            url = picture.get("secure_url") or picture.get("url")
            if url:
                urls.append(url)
        return urls

    def _is_fulfillment(self, record, shipping):
        logistic_type = shipping.get("logistic_type")
        return logistic_type == "fulfillment" or bool(record.get("inventory_id"))

    def _currency_id(self, code):
        if not code:
            return False
        currency = (
            self.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", code)], limit=1)
        )
        return currency.id


class MercadoLibreProductExportMapper(Component):
    _name = "mercadolibre.product.export.mapper"
    _inherit = ["mercadolibre.backend.component", "base.export.mapper"]
    _apply_on = "mercadolibre.product.product"
    _usage = "export.mapper"

    def price_payload(self, binding):
        product = binding.odoo_id
        currency = binding.currency_id or binding.backend_id.company_id.currency_id
        return {
            "prices": [
                {
                    "amount": product.lst_price,
                    "currency_id": currency.name,
                }
            ]
        }

    def legacy_stock_payload(self, binding, quantity):
        quantity = self._quantity(quantity)
        if binding.variation_id:
            return {
                "variations": [
                    {
                        "id": int(binding.variation_id),
                        "available_quantity": quantity,
                    }
                ]
            }
        return {"available_quantity": quantity}

    def user_product_stock_payload(self, mapping, quantity):
        location = {"quantity": self._quantity(quantity)}
        if mapping.store_id:
            location["store_id"] = mapping.store_id
        if mapping.network_node_id:
            location["network_node_id"] = mapping.network_node_id
        return {"locations": [location]}

    def _quantity(self, quantity):
        if quantity == int(quantity):
            return int(quantity)
        return quantity
