# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import FakeResponse, MercadoLibreProductCommon, Transport


class TestMercadoLibreProductNotification(MercadoLibreProductCommon):
    def _notify(self, payload, transport):
        context = dict(
            self.env.context,
            queue_job__no_delay=True,
            mercadolibre_transport=transport,
        )
        env = self.env(context=context)
        backend = env["mercadolibre.backend"].browse(self.backend.id)
        return env["mercadolibre.notification"].create_from_payload(backend, payload)

    def test_items_notification_imports_the_listing(self):
        product = self._product("SKU-LEGACY")
        transport = Transport([FakeResponse(200, self.item_legacy)])
        notification = self._notify(self.notification_items, transport)
        binding = self.env["mercadolibre.product.product"].search(
            [("external_id", "=", "MLA100")]
        )
        self.assertEqual(notification.state, "done")
        self.assertEqual(binding.odoo_id, product)
        self.assertEqual(transport.calls[0]["method"], "GET")
        self.assertTrue(transport.calls[0]["url"].endswith("/items/MLA100"))

    def test_stock_location_updates_marketplace_qty_only(self):
        product = self._product("SKU-UP")
        binding = self._import_item(self.item_user_product)
        self._set_qty(product, 5)
        before = self._quant_qty(product)
        self.assertEqual(before, 5)
        transport = Transport([FakeResponse(200, self.stock_payload)])
        notification = self._notify(self.notification_stock, transport)
        binding.invalidate_recordset()
        self.assertEqual(notification.state, "done")
        self.assertEqual(binding.marketplace_qty, 14)
        self.assertEqual(binding.state, "synced")
        self.assertEqual(self._quant_qty(product), before)
        self.assertTrue(
            transport.calls[0]["url"].endswith("/user-products/MLAU200/stock")
        )

    def test_stock_location_without_binding_is_skipped(self):
        transport = Transport([FakeResponse(200, self.stock_payload)])
        notification = self._notify(self.notification_stock, transport)
        self.assertEqual(notification.state, "skipped")
        self.assertFalse(self.env["mercadolibre.product.product"].search([]))
