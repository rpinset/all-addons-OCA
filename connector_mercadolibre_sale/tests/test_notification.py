# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import MercadoLibreSaleCommon, Transport


class TestMercadoLibreSaleNotification(MercadoLibreSaleCommon):
    def test_duplicate_orders_notification_imports_once(self):
        transport = Transport(
            self._responses(self.order_paid, self.billing_info, self.shipment_me2)
        )
        first = self._notify(self.notification_orders, transport)
        second = self._notify(self.notification_orders, transport)
        bindings = self.env["mercadolibre.sale.order"].search(
            [("external_id", "=", "1001")]
        )
        self.assertEqual(first, second)
        self.assertEqual(first.state, "done")
        self.assertEqual(len(bindings), 1)
        self.assertEqual(
            self.env["sale.order"].search_count(
                [("mercadolibre_order_id", "=", "1001")]
            ),
            1,
        )
        self.assertEqual(bindings.odoo_id.workflow_process_id, self.workflow)

    def test_payment_notification_updates_status_without_a_new_order(self):
        self._import_sale(self.order_paid, self._paid_responses())
        transport = Transport(self._responses(self.payment_refunded))
        notification = self._notify(self.notification_payments, transport)
        binding = self.env["mercadolibre.sale.order"].search(
            [("external_id", "=", "1001")]
        )
        self.assertEqual(notification.state, "done")
        self.assertEqual(binding.payment_status, "refunded")
        self.assertEqual(binding.order_status, "paid")
        self.assertEqual(binding.odoo_id.state, "draft")
        self.assertEqual(
            self.env["sale.order"].search_count(
                [("mercadolibre_order_id", "=", "1001")]
            ),
            1,
        )

    def test_payment_without_an_order_does_not_create_one(self):
        transport = Transport(self._responses(self.payment_refunded))
        notification = self._notify(self.notification_payments, transport)
        self.assertEqual(notification.state, "done")
        self.assertFalse(
            self.env["sale.order"].search([("mercadolibre_order_id", "!=", False)])
        )
        self.assertFalse(self.env["mercadolibre.sale.order"].search([]))
