# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

SEARCH_PAGE = 50


class MercadoLibreSaleAdapter(Component):
    _name = "mercadolibre.sale.adapter"
    _inherit = "mercadolibre.adapter"
    _apply_on = "mercadolibre.sale.order"

    def read_order(self, order_id):
        return self.read(f"/orders/{order_id}")

    def read_billing_info(self, order_id):
        return self.read(f"/orders/{order_id}/billing_info")

    def read_payment(self, resource):
        path = resource if str(resource).startswith("/") else f"/{resource}"
        return self.read(path)

    def search_orders(self, since=None):
        seller_id = self.backend_record.seller_id
        params = {"seller": seller_id, "sort": "date_asc"}
        if since:
            params["order.date_last_updated.from"] = since
        first = self.search(
            "/orders/search",
            params=params,
            limit=SEARCH_PAGE,
            offset=0,
        )
        total = (first.get("paging") or {}).get("total") or 0
        order_ids = self._ids_from_page(first)
        offset = len(order_ids)
        while offset < total:
            page = self.search(
                "/orders/search",
                params=params,
                limit=SEARCH_PAGE,
                offset=offset,
            )
            batch = self._ids_from_page(page)
            if not batch:
                break
            order_ids.extend(batch)
            offset += len(batch)
        return order_ids

    def _ids_from_page(self, page):
        order_ids = []
        for row in page.get("results") or []:
            if isinstance(row, dict):
                if row.get("id"):
                    order_ids.append(str(row["id"]))
            elif row:
                order_ids.append(str(row))
        return order_ids


class MercadoLibreShipmentAdapter(Component):
    _name = "mercadolibre.shipment.adapter"
    _inherit = "mercadolibre.adapter"
    _apply_on = "mercadolibre.shipment"

    def read_shipment(self, shipment_id):
        return self.read(f"/shipments/{shipment_id}")

    def export_tracking(self, shipment_id, tracking_number):
        return self.write(
            f"/shipments/{shipment_id}",
            {
                "tracking_number": tracking_number,
                "status": "shipped",
            },
        )
