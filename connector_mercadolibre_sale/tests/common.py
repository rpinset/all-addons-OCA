# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from pathlib import Path

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


class FakeResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.reason = "error"
        if payload is None:
            self.content = b""
            self._payload = None
        else:
            self._payload = payload
            self.content = b"{}"

    def json(self):
        if self._payload is None:
            raise ValueError("response has no JSON body")
        return self._payload


class Transport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        if not self.responses:
            raise AssertionError(f"unexpected call {method} {url}")
        return self.responses.pop(0)


@tagged("post_install", "-at_install")
class MercadoLibreSaleCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.workflow = cls.env["sale.workflow.process"].create(
            {
                "name": "Mercado Libre paid",
                "validate_order": True,
                "create_invoice": False,
                "register_payment": False,
            }
        )
        cls.fiscal_position = cls.env["account.fiscal.position"].create(
            {"name": "Mercado Libre"}
        )
        cls.shipping_product = cls._service("Mercado Libre shipping")
        cls.fee_product = cls._service("Mercado Libre fee")
        cls.product = (
            cls.env["product.product"]
            .with_context(connector_no_export=True)
            .create(
                {
                    "name": "Legacy kettle",
                    "default_code": "SKU-LEGACY",
                    "type": "consu",
                    "is_storable": False,
                    "list_price": 1500,
                }
            )
        )
        cls.backend = cls.env["mercadolibre.backend"].create(
            {
                "name": "MLA Seller",
                "site_id": "MLA",
                "client_id": "app-client",
                "client_secret": "app-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
                "import_orders": True,
                "workflow_process_id": cls.workflow.id,
                "fiscal_position_id": cls.fiscal_position.id,
                "shipping_product_id": cls.shipping_product.id,
                "fee_product_id": cls.fee_product.id,
            }
        )
        cls.backend.write(
            {
                "seller_id": "123456789",
                "access_token": "test-access",
                "state": "connected",
            }
        )
        cls.env["mercadolibre.product.product"].create(
            {
                "backend_id": cls.backend.id,
                "external_id": "MLA100",
                "odoo_id": cls.product.id,
                "seller_sku": "SKU-LEGACY",
            }
        )
        cls.order_paid = cls._load("order_paid.json")
        cls.order_pack_a = cls._load("order_pack_a.json")
        cls.order_pack_b = cls._load("order_pack_b.json")
        cls.order_cancelled = cls._load("order_cancelled.json")
        cls.order_unknown = cls._load("order_unknown_sku.json")
        cls.billing_info = cls._load("billing_info.json")
        cls.shipment_me2 = cls._load("shipment_me2.json")
        cls.shipment_custom = cls._load("shipment_custom.json")
        cls.shipment_pack = cls._load("shipment_pack.json")
        cls.notification_orders = cls._load("notification_orders_v2.json")
        cls.notification_payments = cls._load("notification_payments.json")
        cls.payment_refunded = cls._load("payment_refunded.json")

    @classmethod
    def _service(cls, name):
        return (
            cls.env["product.product"]
            .with_context(connector_no_export=True)
            .create({"name": name, "type": "service", "list_price": 0.0})
        )

    @classmethod
    def _load(cls, name):
        path = Path(__file__).parent / "fixtures" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def _responses(self, *payloads):
        return [FakeResponse(200, payload) for payload in payloads]

    def _import_sale(self, order, responses):
        transport = Transport(responses)
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.sale.order") as work:
            return work.component(usage="record.importer").run(
                str(order["id"]),
                order=order,
            )

    def _import_shipment(self, payload):
        with self.backend.work_on("mercadolibre.shipment") as work:
            return work.component(usage="record.importer").run(
                payload["id"],
                payload=payload,
            )

    def _paid_responses(self):
        return self._responses(self.billing_info, self.shipment_me2)

    def _pack_responses(self):
        return self._responses(self.billing_info, self.shipment_pack)

    def _warehouse(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.backend.company_id.id)],
            limit=1,
        )
        self.assertTrue(warehouse)
        return warehouse

    def _picking(self, shipment):
        warehouse = self._warehouse()
        return self.env["stock.picking"].create(
            {
                "picking_type_id": warehouse.out_type_id.id,
                "location_id": warehouse.lot_stock_id.id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
                "mercadolibre_shipment_id": shipment.id,
            }
        )

    def _tracking_jobs(self, shipment):
        return self.env["queue.job"].search(
            [
                (
                    "identity_key",
                    "=",
                    f"meli:tracking:{self.backend.id}:{shipment.id}",
                )
            ]
        )

    def _notify(self, payload, transport):
        context = dict(
            self.env.context,
            queue_job__no_delay=True,
            mercadolibre_transport=transport,
        )
        env = self.env(context=context)
        backend = env["mercadolibre.backend"].browse(self.backend.id)
        return env["mercadolibre.notification"].create_from_payload(backend, payload)
