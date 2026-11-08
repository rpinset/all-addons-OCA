# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from types import SimpleNamespace
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import new_test_user

from odoo.addons.connector_mercadolibre_sale.components.notification_handler import (
    _resource_id,
)
from odoo.addons.connector_mercadolibre_sale.components.sale_adapter import (
    MercadoLibreSaleAdapter,
)
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError

from .common import FakeResponse, MercadoLibreSaleCommon, Transport

USER = "base.group_user,connector_mercadolibre.group_mercadolibre_user"
MANAGER = "base.group_user,connector_mercadolibre.group_mercadolibre_manager"


class TestMercadoLibreSaleEdges(MercadoLibreSaleCommon):
    def _user(self, login, groups):
        return new_test_user(self.env, login=login, groups=groups)

    def test_order_import_requires_a_workflow_only_when_enabled(self):
        backend = self.env["mercadolibre.backend"].create(
            {
                "name": "No workflow",
                "site_id": "MLA",
                "client_id": "plain",
                "client_secret": "plain-secret",
                "redirect_uri": "https://example.com/mercadolibre/oauth/callback",
            }
        )
        self.assertFalse(backend.import_orders)
        with self.assertRaises(ValidationError):
            backend.import_orders = True

    def test_catalog_buttons_enqueue_jobs_for_a_manager(self):
        user = self._user("ml_sale_user", USER)
        binding = self._import_sale(self.order_paid, self._paid_responses())
        shipment = binding.shipment_id
        with self.assertRaises(AccessError):
            self.backend.with_user(user).button_import_orders()
        with self.assertRaises(AccessError):
            binding.with_user(user).button_import()
        with self.assertRaises(AccessError):
            shipment.with_user(user).button_import()
        manager = self._user("ml_sale_manager", MANAGER)
        managed = self.backend.with_user(manager)
        managed.button_import_orders()
        binding.with_user(manager).button_import()
        shipment.with_user(manager).button_import()
        managed._enqueue_shipment_import(shipment.external_id)
        managed._enqueue_payment_import("/payments/9001")
        self.assertTrue(
            self.env["queue.job"].search([("identity_key", "like", "meli:")])
        )
        self.backend.with_context(
            mercadolibre_transport=Transport(
                [FakeResponse(200, {"paging": {"total": 0}, "results": []})]
            )
        )._job_import_orders()
        self.env["mercadolibre.backend"].cron_import_orders()
        self.backend.import_orders = False
        self.assertIsNone(self.backend._job_import_orders())
        self.env["mercadolibre.backend"].cron_import_orders()

    def test_jobs_read_order_shipment_and_payment(self):
        self.backend.with_context(
            mercadolibre_transport=Transport(
                self._responses(self.order_paid, self.billing_info, self.shipment_me2)
            )
        )._job_import_order("1001")
        self.backend.with_context(
            mercadolibre_transport=Transport(self._responses(self.shipment_me2))
        )._job_import_shipment("4001")
        self.backend.with_context(
            mercadolibre_transport=Transport(self._responses(self.payment_refunded))
        )._job_import_payment("payments/9001")
        binding = self.env["mercadolibre.sale.order"].search(
            [("external_id", "=", "1001")]
        )
        self.assertEqual(binding.payment_status, "refunded")
        binding.with_context(
            mercadolibre_transport=Transport(
                self._responses(self.order_paid, self.billing_info, self.shipment_me2)
            )
        )._job_import()
        shipment = binding.shipment_id
        shipment.with_context(
            mercadolibre_transport=Transport(self._responses(self.shipment_me2))
        )._job_import()
        empty = self.backend.with_context(
            mercadolibre_transport=Transport(
                [FakeResponse(200, {"id": 1, "status": "approved"})]
            )
        )._job_import_payment("/payments/1")
        self.assertFalse(empty)

    def test_search_orders_pages_and_exports_tracking(self):
        since = "2024-01-01T00:00:00.000Z"
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {
                        "paging": {"total": 3},
                        "results": [{"id": 1}, {"id": None}, "2", None],
                    },
                ),
                FakeResponse(200, {"results": []}),
                FakeResponse(200, {"paging": {"total": 2}, "results": [{"id": 3}]}),
                FakeResponse(200, {"results": ["4"]}),
                FakeResponse(200, {"id": 9, "status": "approved"}),
            ]
        )
        backend = self.backend.with_context(mercadolibre_transport=transport)
        with backend.work_on("mercadolibre.sale.order") as work:
            adapter = work.component(usage="backend.adapter")
            self.assertEqual(adapter.search_orders(since=since), ["1", "2"])
            self.assertEqual(adapter.search_orders(), ["3", "4"])
            self.assertEqual(adapter.read_payment("payments/9")["id"], 9)
        export = Transport([FakeResponse(200, {})])
        with self.backend.with_context(mercadolibre_transport=export).work_on(
            "mercadolibre.shipment"
        ) as work:
            work.component(usage="backend.adapter").export_tracking("4001", "TRACK")
        self.assertEqual(export.calls[0]["method"], "PUT")

    def test_batch_since_uses_the_last_sync_or_the_configured_date(self):
        self.backend.last_order_sync_at = False
        self.backend.import_orders_since = False
        with self.backend.work_on("mercadolibre.sale.order") as work:
            batch = work.component(usage="batch.importer")
            self.assertIsNone(batch._since())
            self.backend.import_orders_since = "2024-01-15 12:00:00"
            self.assertTrue(batch._since().startswith("2024-01-15T"))
            self.backend.last_order_sync_at = fields.Datetime.now()
            self.assertIn("T", batch._since())

    def test_binder_unwraps_records_and_an_empty_match(self):
        binding = self._import_sale(self.order_paid, self._paid_responses())
        with self.backend.work_on("mercadolibre.sale.order") as work:
            binder = work.component(usage="binder")
            self.assertEqual(binder.to_internal("1001", unwrap=True), binding.odoo_id)
            self.assertFalse(binder.to_internal("missing", unwrap=True))
            self.assertFalse(binder.to_internal("missing"))
        with self.backend.work_on("mercadolibre.res.partner") as work:
            binder = work.component(usage="binder")
            self.assertFalse(binder.to_internal("missing", unwrap=True))
        with self.backend.work_on("mercadolibre.shipment") as work:
            binder = work.component(usage="binder")
            self.assertFalse(
                binder.to_internal(binding.shipment_id.external_id, unwrap=True)
            )

    def test_partner_billing_covers_documents_and_failures(self):
        with self.backend.work_on("mercadolibre.res.partner") as work:
            importer = work.component(usage="record.importer")
            importer._apply_billing(self.env["mercadolibre.res.partner"], False)
            self.assertEqual(importer._document("nope"), (False, False))
            self.assertEqual(
                importer._document(
                    {
                        "buyer": {
                            "billing_info": {
                                "identification": {"type": "DNI", "number": "1"}
                            }
                        }
                    }
                ),
                ("DNI", "1"),
            )
            self.assertEqual(
                importer._document(
                    {"buyer": {"billing_info": {"identification": "nope"}}}
                ),
                (False, False),
            )
        buyer = {"id": 777, "nickname": "NICK"}
        transport = Transport(
            [
                FakeResponse(
                    200,
                    {"billing_info": {"doc_type": "CUIT", "doc_number": "20"}},
                )
            ]
        )
        with self.backend.with_context(mercadolibre_transport=transport).work_on(
            "mercadolibre.res.partner"
        ) as work:
            binding = work.component(usage="record.importer").run(
                buyer, order_id="1001"
            )
        self.assertEqual(binding.odoo_id.vat, "20")
        self.assertEqual(binding.odoo_id.name, "NICK")
        with self.backend.work_on("mercadolibre.res.partner") as work:
            importer = work.component(usage="record.importer")
            with patch.object(
                MercadoLibreSaleAdapter,
                "read_billing_info",
                side_effect=RetryableJobError("later"),
            ):
                with self.assertRaises(RetryableJobError):
                    importer.run(buyer, order_id="1001")
            with patch.object(
                MercadoLibreSaleAdapter,
                "read_billing_info",
                side_effect=FailedJobError("billing"),
            ):
                failed = importer.run(buyer, order_id="1001")
            self.assertFalse(failed.raw_billing)
            again = importer.run({"id": 777, "nickname": "NICK2"}, order_id=False)
        self.assertEqual(again.nickname, "NICK2")
        partner = again.odoo_id
        counts = (partner | self.env.user.partner_id).mapped("mercadolibre_bind_count")
        self.assertEqual(counts, [1, 0])
        action = partner.action_view_mercadolibre_bindings()
        self.assertEqual(action["domain"], [("odoo_id", "in", partner.ids)])
        self.env["res.partner"].browse()._compute_mercadolibre_bind_count()

    def test_sale_import_keeps_retryable_errors_and_records_failures(self):
        with self.backend.work_on("mercadolibre.sale.order") as work:
            importer = work.component(usage="record.importer")
            with patch.object(
                type(importer),
                "_import_order",
                side_effect=RetryableJobError("later"),
            ):
                with self.assertRaises(RetryableJobError):
                    importer.run("1001", order={"id": 1001})
            with patch.object(
                type(importer), "_import_order", side_effect=RuntimeError("boom")
            ):
                with self.assertRaises(FailedJobError):
                    importer.run("1001", order={"id": 1001})
        binding = self._import_sale(self.order_paid, self._paid_responses())
        with self.backend.work_on("mercadolibre.sale.order") as work:
            importer = work.component(usage="record.importer")
            with (
                patch.object(type(binding), "browse", return_value=binding),
                patch.object(
                    type(importer), "_import_order", side_effect=FailedJobError("nope")
                ),
            ):
                try:
                    importer.run("1001", order=self.order_paid)
                except FailedJobError as error:
                    self.assertIn("nope", str(error))
                else:
                    self.fail("a failed import must be re-raised")
        self.assertEqual(binding.state, "error")

    def test_sale_values_include_team_pricelist_and_unmapped_logistics(self):
        team = self.env["crm.team"].create({"name": "Mercado Libre"})
        self.env["product.pricelist"].create({"name": "Public", "company_id": False})
        self.backend.team_id = team
        order = dict(self.order_paid)
        order.pop("date_created", None)
        binding = self._import_sale(order, self._paid_responses())
        self.assertEqual(binding.odoo_id.team_id, team)
        self.assertTrue(binding.odoo_id.pricelist_id)
        with self.backend.work_on("mercadolibre.sale.order") as work:
            importer = work.component(usage="record.importer")
            mapper = work.component(usage="import.mapper")
            self.assertFalse(mapper._currency_id(False))
            self.assertFalse(mapper._currency_id("ZZZ"))
            empty = self.env["mercadolibre.shipment"]
            self.assertFalse(importer._unmapped_logistic(empty))
            shipment = binding.shipment_id
            self.assertFalse(importer._unmapped_logistic(shipment))
            self.backend.export_stock = True
            shipment.logistic_type = "fulfillment"
            self.assertFalse(importer._unmapped_logistic(shipment))
            shipment.logistic_type = "drop_off"
            self.assertTrue(importer._unmapped_logistic(shipment))
            self._mapping()
            self.assertFalse(importer._unmapped_logistic(shipment))
            partner = binding.odoo_id.partner_id
            with patch.object(
                type(importer),
                "_pricelist",
                return_value=self.env["product.pricelist"],
            ):
                values = importer._sale_values(
                    partner, {"external_id": "1001", "date_order": False}
                )
            self.assertNotIn("pricelist_id", values)
            confirmed = SimpleNamespace(state="sale")
            importer._assign_receiver(confirmed, shipment)
            importer._update_sale_order(confirmed, partner, {})
            shipment.receiver_partner_id = False
            importer._assign_receiver(SimpleNamespace(state="draft"), shipment)
            builders = work.many_components(usage="sale.order.line.builder")
        product_builder = next(
            builder
            for builder in builders
            if builder._name == "mercadolibre.sale.line.builder.product"
        )
        self.assertFalse(product_builder._product({}))
        fee_builder = next(
            builder
            for builder in builders
            if builder._name == "mercadolibre.sale.line.builder.fee"
        )
        self.assertFalse(
            fee_builder.add_lines(binding, binding.odoo_id, {"order_items": []})
        )
        self.backend.fee_product_id = False
        self.assertFalse(
            fee_builder.add_lines(binding, binding.odoo_id, self.order_paid)
        )
        shipping_builder = next(
            builder
            for builder in builders
            if builder._name == "mercadolibre.sale.line.builder.shipping"
        )
        self.assertEqual(shipping_builder._amount({"shipping": {"cost": 12}}), 12)
        self.assertEqual(
            shipping_builder._amount({"_shipment": {"shipping_option": {"cost": 9}}}),
            9,
        )
        self.assertEqual(shipping_builder._amount({}), 0.0)

    def _mapping(self):
        return self.env["mercadolibre.warehouse.mapping"].create(
            {
                "backend_id": self.backend.id,
                "warehouse_id": self._warehouse().id,
                "stock_type": "seller_warehouse",
            }
        )

    def test_status_mapper_and_cancellation_edges(self):
        with self.backend.work_on("mercadolibre.sale.order") as work:
            mapper = work.component(usage="status.mapper")
        self.assertFalse(mapper.payment_status("nope"))
        self.assertFalse(mapper.payment_status({}))
        self.assertEqual(
            mapper.payment_status({"order": {"id": 1}, "status": "approved"}),
            "approved",
        )
        self.assertFalse(mapper.order_id("nope"))
        self.assertEqual(mapper.order_id({"order": {"id": 8}}), "8")
        self.assertFalse(mapper.order_id({"order": "x"}))
        self.assertEqual(mapper.sale_fee({"order_items": [{}]}), 0.0)
        binding = self._import_sale(self.order_paid, self._paid_responses())
        order = binding.odoo_id
        mapper._cancel_sale_order(self.env["sale.order"])
        order.action_cancel()
        mapper._cancel_sale_order(order)
        self.assertEqual(order.state, "cancel")
        mapper.apply(binding, {})
        mapper.apply(binding, {"status": "paid"})
        self.assertEqual(binding.order_status, "paid")

        class _Pickings:
            def __init__(self, found):
                self.found = found

            def filtered(self, func):
                return self.found

        mapper._cancel_sale_order(
            SimpleNamespace(state="sale", picking_ids=_Pickings(True))
        )
        mapper._cancel_sale_order(
            SimpleNamespace(state="done", picking_ids=_Pickings(False))
        )

    def test_shipment_import_links_a_picking_and_skips_a_blank_address(self):
        binding = self._import_sale(self.order_paid, self._paid_responses())
        shipment = binding.shipment_id
        shipment.picking_id = False
        with self.backend.work_on("mercadolibre.shipment") as work:
            importer = work.component(usage="record.importer")
            importer._link_picking(shipment)
            self.assertFalse(shipment.picking_id)
            warehouse = self._warehouse()
            picking = self.env["stock.picking"].create(
                {
                    "picking_type_id": warehouse.out_type_id.id,
                    "location_id": warehouse.lot_stock_id.id,
                    "location_dest_id": self.env.ref(
                        "stock.stock_location_customers"
                    ).id,
                    "sale_id": binding.odoo_id.id,
                }
            )
            self.assertEqual(shipment.picking_id, picking)
            self.assertEqual(picking.mercadolibre_shipment_id, shipment)
            importer._link_picking(shipment)
            shipment.picking_id = False
            importer._link_picking(shipment)
            self.assertEqual(shipment.picking_id, picking)
            importer._ensure_receiver(shipment, {}, binding)
            importer._ensure_receiver(shipment, {}, None)
            values = importer._receiver_values(
                {"street_name": "Florida", "city": "CABA"},
                binding.odoo_id.partner_id,
            )
            found = importer._receiver_values(
                {"country": {"id": "AR"}, "city": {"name": "CABA"}},
                binding.odoo_id.partner_id,
            )
            self.assertTrue(found["country_id"])
        self.assertFalse(values["country_id"])
        self.assertFalse(values["city"])
        self.backend.with_context(
            mercadolibre_transport=Transport(self._responses(self.shipment_me2))
        )._job_import_shipment("4001")

    def test_tracking_export_uses_the_picking_reference(self):
        shipment = self._import_shipment(self.shipment_custom)
        picking = self._picking(shipment)
        picking.carrier_tracking_ref = "CUSTOM-1"
        transport = Transport([FakeResponse(200, {})])
        exported = shipment.with_context(
            mercadolibre_transport=transport
        )._job_export_tracking()
        self.assertTrue(exported)
        self.assertEqual(shipment.state, "synced")
        self.assertTrue(transport.calls[0]["url"].endswith("/shipments/6001"))
        picking.carrier_tracking_ref = False
        shipment.tracking_number = False
        self.assertFalse(shipment._job_export_tracking())
        shipment.logistic_type = "fulfillment"
        shipment.tracking_number = "SKIP"
        self.assertFalse(shipment._job_export_tracking())
        picking.with_context(connector_no_export=True).write({"state": "done"})

    def test_order_page_actions_and_pack_count(self):
        binding = self._import_sale(self.order_paid, self._paid_responses())
        order = binding.odoo_id
        self.assertEqual(order.mercadolibre_pack_count, 0)
        self.assertEqual(order.mercadolibre_payment_status, binding.payment_status)
        self.assertEqual(
            order.mercadolibre_logistic_type, binding.shipment_id.logistic_type
        )
        action = order.action_open_mercadolibre_binding()
        self.assertEqual(action["res_id"], binding.id)
        pack = order.action_view_mercadolibre_pack()
        self.assertEqual(pack["domain"][0][2], order.mercadolibre_pack_id)
        binding.pack_id = "PACK"
        viewed = binding.action_view_pack()
        self.assertEqual(viewed["domain"][0][2], "PACK")
        self.assertEqual(order.mercadolibre_pack_count, 0)
        bare = self.env["sale.order"].create(
            {"partner_id": self.env.user.partner_id.id}
        )
        self.assertFalse(bare.mercadolibre_order_id)
        self.assertEqual(bare.mercadolibre_pack_count, 0)
        self.assertFalse(bare.mercadolibre_shipment_status)

    def test_notifications_without_an_id_are_errors(self):
        self.assertEqual(_resource_id("/orders", "orders"), "orders")
        self.assertEqual(_resource_id("", "orders"), "")
        missing = {
            "user_id": 123456789,
            "application_id": 1,
            "attempts": 1,
            "sent": "2024-01-16T12:00:00.000Z",
            "resource": "",
        }
        orders = self._notify(
            dict(missing, topic="orders_v2"),
            Transport([]),
        )
        payments = self._notify(
            dict(missing, topic="payments", sent="2024-01-16T12:01:00.000Z"),
            Transport([]),
        )
        shipments = self._notify(
            dict(missing, topic="shipments", sent="2024-01-16T12:02:00.000Z"),
            Transport([]),
        )
        self.assertEqual(orders.state, "error")
        self.assertEqual(payments.state, "error")
        self.assertEqual(shipments.state, "error")
        done = self._notify(
            {
                "resource": "/shipments/4001",
                "user_id": 123456789,
                "topic": "shipments",
                "application_id": 1,
                "attempts": 1,
                "sent": "2024-01-16T12:03:00.000Z",
            },
            Transport(self._responses(self.shipment_me2)),
        )
        self.assertEqual(done.state, "done")
