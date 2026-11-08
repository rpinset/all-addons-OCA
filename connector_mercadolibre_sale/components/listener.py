# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class MercadoLibrePickingListener(Component):
    _name = "mercadolibre.picking.listener"
    _inherit = ["mercadolibre.backend.component", "base.connector.listener"]
    _apply_on = "stock.picking"

    @skip_if(lambda self, record, *args, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        self._link_shipment(record)

    @skip_if(lambda self, record, *args, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        self._link_shipment(record)
        if "state" in set(fields or []) and record.state == "done":
            self._export_tracking(record)

    def _link_shipment(self, picking):
        shipment = picking.mercadolibre_shipment_id
        if shipment:
            if not shipment.picking_id:
                shipment.picking_id = picking
            return
        sale = picking.sale_id
        shipment = sale.mercadolibre_bind_ids[:1].shipment_id
        if shipment and not shipment.picking_id:
            shipment.picking_id = picking
            picking.mercadolibre_shipment_id = shipment

    def _export_tracking(self, picking):
        shipment = picking.mercadolibre_shipment_id
        if shipment and shipment._seller_provides_tracking():
            shipment._enqueue_tracking_export()
