# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class MercadoLibreSaleImportMapper(Component):
    _name = "mercadolibre.sale.import.mapper"
    _inherit = ["mercadolibre.backend.component", "base.import.mapper"]
    _apply_on = "mercadolibre.sale.order"
    _usage = "import.mapper"

    @mapping
    def header(self, record):
        shipping = record.get("shipping") or {}
        shipping_id = shipping.get("id")
        pack_id = record.get("pack_id")
        status_mapper = self.component(usage="status.mapper")
        return {
            "external_id": str(record.get("id") or ""),
            "pack_id": str(pack_id) if pack_id else False,
            "order_status": record.get("status") or False,
            "payment_status": status_mapper.payment_status(record) or False,
            "sale_fee": status_mapper.sale_fee(record),
            "currency_id": self._currency_id(record.get("currency_id")),
            "shipment_external_id": str(shipping_id) if shipping_id else False,
            "date_order": self._datetime(record.get("date_created")),
            "date_updated": self._datetime(record.get("date_last_updated")),
        }

    def _currency_id(self, code):
        if not code:
            return False
        currency = (
            self.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", code)], limit=1)
        )
        return currency.id

    def _datetime(self, value):
        return self.env["mercadolibre.notification"]._parse_sent(value)
