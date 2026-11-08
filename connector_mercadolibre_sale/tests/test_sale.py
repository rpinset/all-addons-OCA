# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import MercadoLibreSaleCommon, Transport


class TestMercadoLibreSale(MercadoLibreSaleCommon):
    def test_paid_order_creates_sale_partner_and_lines(self):
        binding = self._import_sale(self.order_paid, self._paid_responses())
        again = self._import_sale(self.order_paid, self._paid_responses())
        order = binding.odoo_id
        partner = self.env["mercadolibre.res.partner"].search(
            [("external_id", "=", "555")]
        )
        self.assertEqual(binding, again)
        self.assertEqual(len(order), 1)
        self.assertEqual(len(partner), 1)
        self.assertEqual(partner.odoo_id.name, "Ana Perez")
        self.assertFalse(partner.odoo_id.vat)
        self.assertEqual(partner.billing_doc_type, "DNI")
        self.assertEqual(order.workflow_process_id, self.workflow)
        self.assertEqual(order.fiscal_position_id, self.fiscal_position)
        self.assertEqual(order.partner_shipping_id.zip, "1000")
        self.assertEqual(binding.payment_status, "approved")
        self.assertEqual(binding.sale_fee, 300)
        self.assertEqual(binding.shipment_id.tracking_number, "ME2-TRACK")
        products = order.order_line.mapped("product_id")
        self.assertIn(self.product, products)
        self.assertIn(self.shipping_product, products)
        self.assertIn(self.fee_product, products)
        product_line = order.order_line.filtered(
            lambda line: line.product_id == self.product
        )
        self.assertEqual(product_line.product_uom_qty, 2)
        self.assertEqual(
            self.env["sale.order"].search_count(
                [("mercadolibre_order_id", "=", "1001")]
            ),
            1,
        )
        missing_sku = self.env.ref("connector_mercadolibre_sale.exception_missing_sku")
        self.assertNotIn(missing_sku, order.exception_ids)

    def test_pack_links_two_orders_and_one_shipment(self):
        binding_a = self._import_sale(self.order_pack_a, self._pack_responses())
        binding_b = self._import_sale(self.order_pack_b, self._pack_responses())
        self.assertEqual(binding_a.odoo_id.mercadolibre_pack_id, "PACK9")
        self.assertEqual(binding_b.odoo_id.mercadolibre_pack_id, "PACK9")
        self.assertNotEqual(binding_a.odoo_id, binding_b.odoo_id)
        self.assertEqual(binding_a.shipment_id, binding_b.shipment_id)
        self.assertEqual(
            self.env["mercadolibre.shipment"].search_count(
                [("external_id", "=", "5001")]
            ),
            1,
        )
        self.assertEqual(
            self.env["mercadolibre.res.partner"].search_count(
                [("external_id", "=", "555")]
            ),
            1,
        )

    def test_unknown_sku_blocks_confirmation(self):
        binding = self._import_sale(
            self.order_unknown,
            self._responses(self.billing_info),
        )
        order = binding.odoo_id
        note = order.order_line.filtered("mercadolibre_unmatched")
        rule = self.env.ref("connector_mercadolibre_sale.exception_missing_sku")
        self.assertTrue(note)
        self.assertFalse(note.product_id)
        self.assertEqual(note.display_type, "line_note")
        self.assertIn(rule, order.exception_ids)
        order.action_confirm()
        self.assertEqual(order.state, "draft")

    def test_cancel_one_pack_order_leaves_the_sibling(self):
        binding_a = self._import_sale(self.order_pack_a, self._pack_responses())
        binding_b = self._import_sale(self.order_pack_b, self._pack_responses())
        binding_a.odoo_id.action_confirm()
        binding_b.odoo_id.action_confirm()
        self.assertEqual(binding_a.odoo_id.state, "sale")
        self.assertEqual(binding_b.odoo_id.state, "sale")
        self._import_sale(self.order_cancelled, self._pack_responses())
        self.assertEqual(binding_a.odoo_id.state, "cancel")
        self.assertEqual(binding_b.odoo_id.state, "sale")

    def test_me2_done_picking_does_not_export_tracking(self):
        shipment = self._import_shipment(self.shipment_me2)
        self.assertEqual(shipment.tracking_number, "ME2-TRACK")
        self.assertFalse(shipment._seller_provides_tracking())
        picking = self._picking(shipment)
        picking.write({"state": "done", "carrier_tracking_ref": "IGNORED"})
        self.assertFalse(self._tracking_jobs(shipment))

    def test_done_custom_picking_enqueues_one_tracking_export(self):
        shipment = self._import_shipment(self.shipment_custom)
        picking = self._picking(shipment)
        picking.write({"state": "done", "carrier_tracking_ref": "CUSTOM-1"})
        picking.write({"state": "done"})
        jobs = self._tracking_jobs(shipment)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs.method_name, "_job_export_tracking")
        self.assertEqual(jobs.state, "pending")

    def test_fulfillment_shipment_does_not_export_tracking(self):
        payload = dict(self.shipment_custom, id=7001, logistic_type="fulfillment")
        shipment = self._import_shipment(payload)
        self.assertFalse(shipment._seller_provides_tracking())
        picking = self._picking(shipment)
        picking.write({"state": "done", "carrier_tracking_ref": "SKIP"})
        self.assertFalse(self._tracking_jobs(shipment))

    def test_reconciliation_shares_the_order_job(self):
        self.backend._enqueue_order_import("1001")
        page = {"paging": {"total": 1}, "results": [{"id": 1001}]}
        backend = self.backend.with_context(
            mercadolibre_transport=Transport(self._responses(page))
        )
        with backend.work_on("mercadolibre.sale.order") as work:
            work.component(usage="batch.importer").run()
        jobs = self.env["queue.job"].search(
            [("identity_key", "=", f"meli:order:{self.backend.id}:1001")]
        )
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs.method_name, "_job_import_order")
        self.assertEqual(jobs.state, "pending")
        self.assertTrue(self.backend.last_order_sync_at)
