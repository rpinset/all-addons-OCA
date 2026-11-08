# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.component.core import Component
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

TAX_ID_TYPES = {"CUIT", "CUIL", "RFC", "RUT", "CNPJ", "CPF", "NIT", "RUC", "VAT"}
SELLER_LOGISTIC_TYPES = {
    "drop_off",
    "xd_drop_off",
    "cross_docking",
    "self_service",
}


class MercadoLibrePartnerImporter(Component):
    _name = "mercadolibre.partner.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.res.partner"
    _usage = "record.importer"

    def run(self, buyer, order_id=None):
        external_id = str(buyer.get("id") or "")
        binder = self.component(usage="binder")
        binding = (
            binder.to_internal(external_id) if external_id else binder.model.browse()
        )
        partner = binding.odoo_id or self._create_partner(buyer)
        if not binding:
            binding = self.model.create(
                {
                    "backend_id": self.backend_record.id,
                    "external_id": external_id,
                    "odoo_id": partner.id,
                    "nickname": buyer.get("nickname") or False,
                }
            )
        else:
            binding.nickname = buyer.get("nickname") or binding.nickname
        self._apply_billing(binding, order_id)
        binding.mark_synced()
        return binding

    def _create_partner(self, buyer):
        first = buyer.get("first_name") or ""
        last = buyer.get("last_name") or ""
        name = " ".join(part for part in (first, last) if part)
        return self.env["res.partner"].create(
            {
                "name": name or buyer.get("nickname") or "Mercado Libre buyer",
                "company_id": self.backend_record.company_id.id,
                "customer_rank": 1,
            }
        )

    def _apply_billing(self, binding, order_id):
        if not order_id:
            return
        payload = self._billing_payload(order_id)
        doc_type, doc_number = self._document(payload)
        binding.write(
            {
                "billing_doc_type": doc_type or False,
                "billing_doc_number": doc_number or False,
                "raw_billing": payload or False,
            }
        )
        if doc_type in TAX_ID_TYPES and doc_number:
            binding.odoo_id.vat = doc_number

    def _billing_payload(self, order_id):
        adapter = self.component(
            usage="backend.adapter",
            model_name="mercadolibre.sale.order",
        )
        try:
            return adapter.read_billing_info(order_id)
        except RetryableJobError:
            raise
        except FailedJobError:
            return {}

    def _document(self, payload):
        if not isinstance(payload, dict):
            return False, False
        info = payload.get("billing_info") or payload
        if isinstance(info, dict) and info.get("doc_type"):
            return info.get("doc_type"), info.get("doc_number")
        buyer = payload.get("buyer") or {}
        billing = buyer.get("billing_info") or {}
        identification = billing.get("identification") or billing
        if isinstance(identification, dict):
            return identification.get("type"), identification.get("number")
        return False, False


class MercadoLibreSaleImporter(Component):
    _name = "mercadolibre.sale.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "record.importer"

    def run(self, order_id, order=None):
        binding = self.model.browse()
        try:
            if order is None:
                order = self.component(usage="backend.adapter").read_order(order_id)
            binding = self._import_order(order)
        except RetryableJobError:
            raise
        except Exception as error:
            if binding:
                binding.mark_error(str(error))
            if isinstance(error, FailedJobError):
                raise
            raise FailedJobError(str(error)) from error
        return binding

    def _import_order(self, order):
        values = self.component(usage="import.mapper").map_record(order).values()
        buyer = order.get("buyer") or {}
        partner_binding = self.component(
            usage="record.importer",
            model_name="mercadolibre.res.partner",
        ).run(buyer, order_id=values["external_id"])
        binding = self.component(usage="binder").to_internal(values["external_id"])
        sale_order = binding.odoo_id or self._create_sale_order(
            partner_binding.odoo_id, values
        )
        self._update_sale_order(sale_order, partner_binding.odoo_id, values)
        if binding:
            binding.write(values)
        else:
            values["backend_id"] = self.backend_record.id
            values["odoo_id"] = sale_order.id
            binding = self.model.create(values)
        shipment_payload = self._read_shipment_payload(order)
        if shipment_payload:
            order["_shipment"] = shipment_payload
        if sale_order.state in ("draft", "sent"):
            self._rebuild_lines(binding, sale_order, order)
        shipment = self._import_shipment(order, binding, shipment_payload)
        if shipment:
            binding.shipment_id = shipment
            self._assign_receiver(sale_order, shipment)
        self._apply_fiscal_position(sale_order)
        sale_order.mercadolibre_unmapped_logistic = self._unmapped_logistic(shipment)
        self.component(usage="status.mapper").apply(binding, order)
        sale_order.detect_exceptions()
        binding.mark_synced()
        return binding

    def _create_sale_order(self, partner, values):
        return (
            self.env["sale.order"]
            .with_company(self.backend_record.company_id)
            .create(self._sale_values(partner, values))
        )

    def _update_sale_order(self, sale_order, partner, values):
        if sale_order.state not in ("draft", "sent"):
            return
        sale_order.write(self._sale_values(partner, values))

    def _sale_values(self, partner, values):
        backend = self.backend_record
        vals = {
            "partner_id": partner.id,
            "partner_invoice_id": partner.id,
            "company_id": backend.company_id.id,
            "workflow_process_id": backend.workflow_process_id.id,
            "fiscal_position_id": backend.fiscal_position_id.id or False,
            "client_order_ref": values["external_id"],
            "origin": f"Mercado Libre {values['external_id']}",
            "date_order": values["date_order"] or fields.Datetime.now(),
        }
        if backend.team_id:
            vals["team_id"] = backend.team_id.id
        pricelist = self._pricelist(backend.company_id)
        if pricelist:
            vals["pricelist_id"] = pricelist.id
        return vals

    def _pricelist(self, company):
        return self.env["product.pricelist"].search(
            [
                "|",
                ("company_id", "=", False),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )

    def _rebuild_lines(self, binding, sale_order, order):
        sale_order.order_line.unlink()
        builders = self.many_components(usage="sale.order.line.builder")
        for builder in sorted(builders, key=lambda item: item._sequence):
            builder.add_lines(binding, sale_order, order)

    def _read_shipment_payload(self, order):
        shipping = order.get("shipping") or {}
        shipment_id = shipping.get("id")
        if not shipment_id:
            return None
        return self.component(
            usage="backend.adapter",
            model_name="mercadolibre.shipment",
        ).read_shipment(shipment_id)

    def _import_shipment(self, order, binding, payload):
        shipping = order.get("shipping") or {}
        shipment_id = shipping.get("id")
        if not shipment_id:
            return self.env["mercadolibre.shipment"]
        return self.component(
            usage="record.importer",
            model_name="mercadolibre.shipment",
        ).run(shipment_id, sale_binding=binding, payload=payload)

    def _apply_fiscal_position(self, sale_order):
        """Copy the backend fiscal position after the shipping address compute."""
        if sale_order.state not in ("draft", "sent"):
            return
        sale_order.fiscal_position_id = self.backend_record.fiscal_position_id

    def _assign_receiver(self, sale_order, shipment):
        if sale_order.state not in ("draft", "sent"):
            return
        receiver = shipment.receiver_partner_id
        if receiver:
            sale_order.partner_shipping_id = receiver

    def _unmapped_logistic(self, shipment):
        backend = self.backend_record
        if not shipment or not backend.export_stock:
            return False
        if shipment.logistic_type not in SELLER_LOGISTIC_TYPES:
            return False
        mappings = backend.warehouse_mapping_ids.filtered(
            lambda mapping: mapping.stock_type != "fulfillment"
        )
        return not mappings


class MercadoLibreSaleBatchImporter(Component):
    _name = "mercadolibre.sale.batch.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "batch.importer"

    def run(self):
        since = self._since()
        order_ids = self.component(usage="backend.adapter").search_orders(since=since)
        backend = self.backend_record
        for order_id in order_ids:
            backend._enqueue_order_import(order_id)
        backend.last_order_sync_at = fields.Datetime.now()

    def _since(self):
        backend = self.backend_record
        moment = backend.last_order_sync_at or backend.import_orders_since
        if not moment:
            return None
        text = fields.Datetime.to_string(moment)
        return text.replace(" ", "T") + ".000Z"


class MercadoLibreShipmentImporter(Component):
    _name = "mercadolibre.shipment.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.shipment"
    _usage = "record.importer"

    def run(self, shipment_id, sale_binding=None, payload=None):
        if payload is None:
            payload = self.component(usage="backend.adapter").read_shipment(shipment_id)
        binding = self.component(usage="binder").to_internal(shipment_id)
        values = self._values(payload)
        if binding:
            binding.write(values)
        else:
            values["backend_id"] = self.backend_record.id
            values["external_id"] = str(shipment_id)
            binding = self.model.create(values)
        if sale_binding:
            sale_binding.shipment_id = binding
        self._link_picking(binding)
        self._ensure_receiver(binding, payload, sale_binding)
        binding.mark_synced()
        return binding

    def _values(self, payload):
        return {
            "logistic_type": payload.get("logistic_type") or False,
            "mode": payload.get("mode") or False,
            "status": payload.get("status") or False,
            "tracking_number": payload.get("tracking_number") or False,
        }

    def _link_picking(self, binding):
        if binding.picking_id:
            return
        for sale_binding in binding.sale_binding_ids:
            picking = sale_binding.odoo_id.picking_ids.filtered(
                lambda row: row.state != "cancel"
            )[:1]
            if picking:
                binding.picking_id = picking
                picking.mercadolibre_shipment_id = binding
                return

    def _ensure_receiver(self, binding, payload, sale_binding):
        address = payload.get("receiver_address") or {}
        if not address:
            return
        buyer = sale_binding.odoo_id.partner_id if sale_binding else False
        if not buyer:
            buyer = binding.sale_binding_ids[:1].odoo_id.partner_id
        if not buyer:
            return
        partner = binding.receiver_partner_id or self.env["res.partner"].create(
            {"parent_id": buyer.id, "type": "delivery", "name": buyer.name}
        )
        partner.write(self._receiver_values(address, buyer))
        binding.receiver_partner_id = partner

    def _receiver_values(self, address, buyer):
        street_name = address.get("street_name") or ""
        number = address.get("street_number") or ""
        city = address.get("city") or {}
        country = address.get("country") or {}
        country_id = False
        if country.get("id"):
            found = self.env["res.country"].search(
                [("code", "=", country["id"])],
                limit=1,
            )
            country_id = found.id
        return {
            "name": address.get("receiver_name") or buyer.name,
            "street": " ".join(part for part in (street_name, str(number)) if part),
            "zip": address.get("zip_code") or False,
            "city": city.get("name") if isinstance(city, dict) else False,
            "country_id": country_id,
            "type": "delivery",
            "parent_id": buyer.id,
            "company_id": buyer.company_id.id,
        }


class MercadoLibrePaymentImporter(Component):
    _name = "mercadolibre.payment.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.sale.order"
    _usage = "payment.importer"

    def run(self, resource):
        payload = self.component(usage="backend.adapter").read_payment(resource)
        status_mapper = self.component(usage="status.mapper")
        order_id = status_mapper.order_id(payload)
        if not order_id:
            return self.model.browse()
        binding = self.component(usage="binder").to_internal(order_id)
        if not binding:
            return binding
        status_mapper.apply(binding, payload)
        binding.mark_synced()
        return binding
