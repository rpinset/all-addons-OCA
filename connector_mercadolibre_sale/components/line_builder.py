# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class MercadoLibreProductLineBuilder(Component):
    _name = "mercadolibre.sale.line.builder.product"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "sale.order.line.builder"
    _sequence = 10

    def add_lines(self, binding, order, payload):
        lines = self.env["sale.order.line"]
        for item_line in payload.get("order_items") or []:
            lines |= self._add_item(order, item_line)
        return lines

    def _add_item(self, order, item_line):
        item = item_line.get("item") or {}
        product = self._product(item)
        title = item.get("title") or item.get("id") or "Mercado Libre item"
        quantity = item_line.get("quantity") or 0.0
        if not product:
            return self.env["sale.order.line"].create(
                {
                    "order_id": order.id,
                    "display_type": "line_note",
                    "name": self.env._(
                        "Unmatched Mercado Libre item %(item)s (%(title)s).",
                        item=item.get("id") or "",
                        title=title,
                    ),
                    "product_uom_qty": 0.0,
                    "price_unit": 0.0,
                    "customer_lead": 0.0,
                    "mercadolibre_unmatched": True,
                }
            )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": product.id,
                "product_uom_qty": quantity,
                "name": title,
            }
        )
        line.price_unit = item_line.get("unit_price") or 0.0
        return line

    def _product(self, item):
        external_id = item.get("id")
        if not external_id:
            return self.env["product.product"]
        variation = item.get("variation_id")
        binding = self.env["mercadolibre.product.product"].search(
            [
                ("backend_id", "=", self.backend_record.id),
                ("external_id", "=", str(external_id)),
                ("variation_id", "=", str(variation) if variation else False),
            ],
            limit=1,
        )
        return binding.odoo_id


class MercadoLibreShippingLineBuilder(Component):
    _name = "mercadolibre.sale.line.builder.shipping"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "sale.order.line.builder"
    _sequence = 20

    def add_lines(self, binding, order, payload):
        product = self.backend_record.shipping_product_id
        amount = self._amount(payload)
        if not product or not amount:
            return self.env["sale.order.line"]
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": product.id,
                "product_uom_qty": 1.0,
                "name": product.display_name,
            }
        )
        line.price_unit = amount
        return line

    def _amount(self, payload):
        shipment = payload.get("_shipment") or {}
        option = shipment.get("shipping_option") or {}
        if option.get("cost"):
            return option["cost"]
        shipping = payload.get("shipping") or {}
        return shipping.get("cost") or 0.0


class MercadoLibreFeeLineBuilder(Component):
    _name = "mercadolibre.sale.line.builder.fee"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "sale.order.line.builder"
    _sequence = 30

    def add_lines(self, binding, order, payload):
        product = self.backend_record.fee_product_id
        amount = self.component(usage="status.mapper").sale_fee(payload)
        if not product or not amount:
            return self.env["sale.order.line"]
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": product.id,
                "product_uom_qty": 1.0,
                "name": product.display_name,
            }
        )
        line.price_unit = amount
        return line
