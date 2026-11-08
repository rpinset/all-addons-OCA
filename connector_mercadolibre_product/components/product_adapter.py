# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

SEARCH_PAGE = 50
SCAN_THRESHOLD = 1000


class MercadoLibreProductAdapter(Component):
    _name = "mercadolibre.product.adapter"
    _inherit = "mercadolibre.adapter"
    _apply_on = "mercadolibre.product.product"

    def read_item(self, item_id):
        return self.read(f"/items/{item_id}")

    def update_prices(self, item_id, payload):
        return self.create(f"/items/{item_id}/prices", payload)

    def update_legacy_stock(self, item_id, payload):
        return self.write(f"/items/{item_id}", payload)

    def update_user_product_stock(self, user_product_id, stock_type, payload):
        path = f"/user-products/{user_product_id}/stock/type/{stock_type}"
        return self.write(path, payload)

    def read_stock(self, resource):
        path = resource if str(resource).startswith("/") else f"/{resource}"
        return self.read(path)

    def search_item_ids(self):
        seller_id = self.backend_record.seller_id
        path = f"/users/{seller_id}/items/search"
        first = self.search(path, limit=SEARCH_PAGE, offset=0)
        total = (first.get("paging") or {}).get("total") or 0
        if total > SCAN_THRESHOLD:
            return self._search_item_ids_scan(path)
        return self._search_item_ids_offset(path, first, total)

    def _search_item_ids_offset(self, path, first, total):
        item_ids = list(first.get("results") or [])
        offset = len(item_ids)
        while offset < total:
            page = self.search(path, limit=SEARCH_PAGE, offset=offset)
            batch = list(page.get("results") or [])
            if not batch:
                break
            item_ids.extend(batch)
            offset += len(batch)
        return item_ids

    def _search_item_ids_scan(self, path):
        page = self.search(path, search_type="scan", limit=SEARCH_PAGE)
        item_ids = list(page.get("results") or [])
        scroll_id = page.get("scroll_id")
        seen_scrolls = set()
        while scroll_id and scroll_id not in seen_scrolls:
            seen_scrolls.add(scroll_id)
            page = self.search(
                path,
                search_type="scan",
                scroll_id=scroll_id,
                limit=SEARCH_PAGE,
            )
            batch = list(page.get("results") or [])
            if not batch:
                break
            item_ids.extend(batch)
            scroll_id = page.get("scroll_id")
        return item_ids
