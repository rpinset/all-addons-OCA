# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class MercadoLibreProductListener(Component):
    _name = "mercadolibre.product.listener"
    _inherit = ["mercadolibre.backend.component", "base.connector.listener"]
    _apply_on = ["product.product", "stock.move"]

    @skip_if(lambda self, record, *args, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields = set(fields or [])
        price_fields = {"lst_price", "list_price"}
        if record._name == "product.product" and price_fields & fields:
            self._export_prices(record)
        elif record._name == "stock.move" and record.state == "done":
            self._export_stock_for_move(record)

    @skip_if(lambda self, record, *args, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if record._name == "stock.move" and record.state == "done":
            self._export_stock_for_move(record)

    def _export_prices(self, product):
        for binding in product.mercadolibre_bind_ids:
            if binding.backend_id.export_prices and binding.external_id:
                binding._enqueue_price_export()

    def _export_stock_for_move(self, move):
        locations = move.location_id | move.location_dest_id
        internal = locations.filtered(lambda loc: loc.usage == "internal")
        if not internal:
            return
        for binding in move.product_id.mercadolibre_bind_ids:
            if not binding.backend_id.export_stock or binding.fulfillment:
                continue
            for mapping in binding.backend_id.warehouse_mapping_ids:
                if mapping.stock_type == "fulfillment" or not mapping.location_id:
                    continue
                if self._mapping_touched(mapping, internal):
                    binding._enqueue_stock_export(mapping)

    def _mapping_touched(self, mapping, locations):
        stock_location = mapping.location_id
        stock_path = stock_location.parent_path or ""
        for location in locations:
            path = location.parent_path or ""
            if location == stock_location:
                return True
            if stock_path and path.startswith(stock_path):
                return True
            if path and stock_path.startswith(path):
                return True
        return False
