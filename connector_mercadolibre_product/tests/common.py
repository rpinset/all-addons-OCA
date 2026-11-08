# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from copy import deepcopy
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
class MercadoLibreProductCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env["mercadolibre.backend"].create(
            {
                "name": "MLA Seller",
                "site_id": "MLA",
                "client_id": "app-client",
                "client_secret": "app-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
            }
        )
        cls.backend.write(
            {
                "seller_id": "123456789",
                "access_token": "test-access",
                "state": "connected",
            }
        )
        cls.item_legacy = cls._load("item_legacy.json")
        cls.item_user_product = cls._load("item_user_product.json")
        cls.item_fulfillment = cls._load("item_fulfillment.json")
        cls.notification_items = cls._load("notification_items.json")
        cls.notification_stock = cls._load("notification_stock_location.json")
        cls.stock_payload = cls._load("stock_user_product.json")
        cls.error_429 = cls._load("error_429.json")

    @classmethod
    def _load(cls, name):
        path = Path(__file__).parent / "fixtures" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def _copy_item(self, item, **updates):
        copied = deepcopy(item)
        copied.update(updates)
        return copied

    def _product(self, code, price=10.0):
        return (
            self.env["product.product"]
            .with_context(connector_no_export=True)
            .create(
                {
                    "name": code,
                    "default_code": code,
                    "type": "consu",
                    "is_storable": True,
                    "list_price": price,
                }
            )
        )

    def _import_item(self, item):
        with self.backend.work_on("mercadolibre.product.product") as work:
            return work.component(usage="record.importer").run(item["id"], item=item)

    def _warehouse(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.backend.company_id.id)],
            limit=1,
        )
        self.assertTrue(warehouse)
        return warehouse

    def _mapping(self, stock_type="seller_warehouse", warehouse=None):
        warehouse = warehouse or self._warehouse()
        return self.env["mercadolibre.warehouse.mapping"].create(
            {
                "backend_id": self.backend.id,
                "warehouse_id": warehouse.id,
                "stock_type": stock_type,
                "store_id": "STORE1",
                "network_node_id": "NODE1",
            }
        )

    def _set_qty(self, product, quantity, warehouse=None):
        warehouse = warehouse or self._warehouse()
        self.env["stock.quant"]._update_available_quantity(
            product,
            warehouse.lot_stock_id,
            quantity,
        )
        return warehouse

    def _quant_qty(self, product):
        quants = self.env["stock.quant"].search([("product_id", "=", product.id)])
        return sum(quants.mapped("quantity"))

    def _jobs(self, identity_key):
        return self.env["queue.job"].search([("identity_key", "=", identity_key)])
