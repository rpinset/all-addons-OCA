from unittest.mock import MagicMock, patch

from odoo.tests.common import TransactionCase

from odoo.addons.queue_job.tests.common import trap_jobs


class TestShopifyInboundFulfillment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Inbound Fulfillment Shop",
                "shop_url": "inbound-fulfillment.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
                "fulfillment_auto_validate_webhook": True,
            }
        )
        cls.instance.state = "connected"
        cls.company = cls.instance.company_id
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )
        cls.widget = cls._create_product("Inbound Widget")
        cls.gadget = cls._create_product("Inbound Gadget")
        cls.carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Inbound Express",
                "delivery_type": "fixed",
                "product_id": cls.env["product.product"]
                .create({"name": "Inbound Express Shipping", "type": "service"})
                .id,
            }
        )
        cls.env["shopify.carrier.mapping"].create(
            {
                "instance_id": cls.instance.id,
                "carrier_id": cls.carrier.id,
                "tracking_company": "FedEx",
            }
        )
        cls.customer = cls.env["res.partner"].create(
            {"name": "Inbound Customer", "company_id": cls.company.id}
        )
        cls.sale, cls.order_binding, line_bindings = cls._create_order(
            810, [(cls.widget, 2), (cls.gadget, 2)]
        )
        cls.widget_line, cls.gadget_line = line_bindings

    @classmethod
    def _create_product(cls, name, **values):
        return cls.env["product.product"].create(
            {
                "name": name,
                "type": "consu",
                "is_storable": True,
                "company_id": cls.company.id,
                **values,
            }
        )

    @classmethod
    def _create_order(cls, number, lines):
        sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.customer.id,
                "company_id": cls.company.id,
                "warehouse_id": cls.warehouse.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom_qty": quantity,
                            "price_unit": 10,
                        },
                    )
                    for product, quantity in lines
                ],
            }
        )
        order_binding = cls.env["shopify.order"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": f"gid://shopify/Order/{number}",
                "odoo_id": sale.id,
                "order_name": f"#{number}",
                "state": "synced",
            }
        )
        line_bindings = cls.env["shopify.order.line"]
        for index, sale_line in enumerate(sale.order_line, start=1):
            line_bindings |= cls.env["shopify.order.line"].create(
                {
                    "instance_id": cls.instance.id,
                    "shopify_id": f"gid://shopify/LineItem/{number}{index}",
                    "order_binding_id": order_binding.id,
                    "odoo_id": sale_line.id,
                    "state": "synced",
                }
            )
        return sale, order_binding, line_bindings

    def _stock(self, product, quantity, lot=None):
        self.env["stock.quant"]._update_available_quantity(
            product, self.warehouse.lot_stock_id, quantity, lot_id=lot
        )

    def _payload(self, number, lines, tracking=None, order_binding=None):
        return {
            "id": f"gid://shopify/Fulfillment/{number}",
            "status": "SUCCESS",
            "order": {"id": (order_binding or self.order_binding).shopify_id},
            "location": {"id": "gid://shopify/Location/80"},
            "trackingInfo": tracking or [],
            "fulfillmentLineItems": {
                "nodes": [
                    {
                        "id": f"gid://shopify/FulfillmentLineItem/{number}{index}",
                        "quantity": quantity,
                        "lineItem": {"id": line.shopify_id},
                    }
                    for index, (line, quantity) in enumerate(lines)
                ]
            },
        }

    def _import(self, payload):
        client = MagicMock()
        client.execute.return_value = {"fulfillment": payload}
        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            trap_jobs() as trap,
        ):
            binding_id = self.env["shopify.fulfillment"]._job_import_from_shopify(
                self.instance.id, payload["id"], {}
            )
        trap.assert_jobs_count(0)
        return self.env["shopify.fulfillment"].browse(binding_id)

    def _done_quantities(self, picking):
        return {
            move.product_id: move.quantity
            for move in picking.move_ids
            if move.state == "done"
        }

    def test_full_fulfillment_validates_the_delivery_with_its_tracking(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids

        fulfillment = self._import(
            self._payload(
                900,
                [(self.widget_line, 2), (self.gadget_line, 2)],
                tracking=[
                    {"company": "FedEx", "number": "7701", "url": ""},
                    {"company": "FedEx", "number": "7702", "url": ""},
                ],
            )
        )

        self.assertEqual(picking.state, "done")
        self.assertFalse(picking.backorder_ids)
        self.assertEqual(fulfillment.state, "synced")
        self.assertEqual(fulfillment.picking_id, picking)
        self.assertEqual(picking.carrier_id, self.carrier)
        self.assertEqual(picking.carrier_tracking_ref, "7701,7702")
        self.assertEqual(self.sale.order_line.mapped("qty_delivered"), [2, 2])

    def test_partial_fulfillment_ships_only_the_fulfilled_items(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        picking.action_assign()

        self._import(self._payload(901, [(self.widget_line, 1)]))

        self.assertEqual(picking.state, "done")
        self.assertEqual(self._done_quantities(picking), {self.widget: 1})
        backorder = picking.backorder_ids
        self.assertEqual(
            {move.product_id: move.product_uom_qty for move in backorder.move_ids},
            {self.widget: 1, self.gadget: 2},
        )
        self.assertEqual(backorder.state, "assigned")
        self.assertEqual(self.sale.order_line.mapped("qty_delivered"), [1, 0])

    def test_next_fulfillment_validates_the_backorder(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        self._import(self._payload(902, [(self.widget_line, 1)]))
        backorder = picking.backorder_ids

        fulfillment = self._import(
            self._payload(903, [(self.widget_line, 1), (self.gadget_line, 2)])
        )

        self.assertEqual(backorder.state, "done")
        self.assertFalse(backorder.backorder_ids)
        self.assertEqual(fulfillment.picking_id, backorder)
        self.assertEqual(self.sale.order_line.mapped("qty_delivered"), [2, 2])

    def test_fulfillment_update_only_refreshes_the_tracking(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        payload = self._payload(904, [(self.widget_line, 1)])
        fulfillment = self._import(payload)
        backorder = picking.backorder_ids

        payload["trackingInfo"] = [{"company": "FedEx", "number": "7799", "url": ""}]
        self._import(payload)

        self.assertEqual(fulfillment.picking_id, picking)
        self.assertEqual(picking.carrier_tracking_ref, "7799")
        self.assertEqual(picking.carrier_id, self.carrier)
        self.assertNotEqual(backorder.state, "done")
        self.assertEqual(self.sale.order_line.mapped("qty_delivered"), [1, 0])

    def test_fulfillment_ships_unreserved_stock_when_enabled(self):
        self.instance.fulfillment_validate_unreserved = True
        self.sale.action_confirm()
        picking = self.sale.picking_ids

        self._import(self._payload(905, [(self.widget_line, 2), (self.gadget_line, 2)]))

        self.assertEqual(picking.state, "done")
        self.assertEqual(
            self._done_quantities(picking), {self.widget: 2, self.gadget: 2}
        )

    def test_fulfillment_needs_reserved_stock_by_default(self):
        self._stock(self.widget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids

        fulfillment = self._import(
            self._payload(911, [(self.widget_line, 2), (self.gadget_line, 2)])
        )

        self.assertNotEqual(picking.state, "done")
        self.assertEqual(fulfillment.state, "error")
        self.assertIn(self.gadget.display_name, fulfillment.error_message)
        self.assertIn("Ship Unreserved Stock", fulfillment.error_message)

    def test_fulfillment_confirms_a_draft_order(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)

        fulfillment = self._import(
            self._payload(912, [(self.widget_line, 2), (self.gadget_line, 2)])
        )

        self.assertEqual(self.sale.state, "sale")
        self.assertEqual(fulfillment.state, "synced")
        self.assertEqual(fulfillment.picking_id, self.sale.picking_ids)
        self.assertEqual(self.sale.picking_ids.state, "done")
        self.assertEqual(self.sale.order_line.mapped("qty_delivered"), [2, 2])

    def test_fulfillment_validates_the_earlier_steps(self):
        self.warehouse.delivery_steps = "pick_ship"
        sale, order_binding, line_bindings = self._create_order(
            830, [(self.widget, 2), (self.gadget, 2)]
        )
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        sale.action_confirm()
        pick = sale.picking_ids

        fulfillment = self._import(
            self._payload(913, [(line_bindings[0], 1)], order_binding=order_binding)
        )

        ship = fulfillment.picking_id
        self.assertEqual(ship.picking_type_code, "outgoing")
        self.assertEqual(pick.state, "done")
        self.assertEqual(ship.state, "done")
        self.assertEqual(self._done_quantities(pick), {self.widget: 1})
        self.assertEqual(self._done_quantities(ship), {self.widget: 1})
        self.assertEqual(sale.order_line.mapped("qty_delivered"), [1, 0])

        self._import(
            self._payload(
                914,
                [(line_bindings[0], 1), (line_bindings[1], 2)],
                order_binding=order_binding,
            )
        )

        self.assertFalse(
            sale.picking_ids.filtered(lambda picking: picking.state != "done")
        )
        self.assertEqual(sale.order_line.mapped("qty_delivered"), [2, 2])

    def test_fulfillment_validates_pick_pack_and_ship(self):
        self.warehouse.delivery_steps = "pick_pack_ship"
        sale, order_binding, line = self._create_order(831, [(self.widget, 2)])
        self._stock(self.widget, 2)
        sale.action_confirm()

        fulfillment = self._import(
            self._payload(916, [(line, 1)], order_binding=order_binding)
        )

        self.assertEqual(fulfillment.state, "synced")
        self.assertEqual(fulfillment.picking_id.picking_type_code, "outgoing")
        self.assertEqual(
            sorted(
                sale.picking_ids.filtered(
                    lambda picking: picking.state == "done"
                ).picking_type_id.mapped("sequence_code")
            ),
            ["OUT", "PACK", "PICK"],
        )
        self.assertEqual(sale.order_line.qty_delivered, 1)

    def test_fulfillment_after_the_pick_was_validated_in_odoo(self):
        self.warehouse.delivery_steps = "pick_pack_ship"
        sale, order_binding, line = self._create_order(832, [(self.widget, 2)])
        self._stock(self.widget, 2)
        sale.action_confirm()
        pick = sale.picking_ids
        pick.action_assign()
        pick.button_validate()
        pack = sale.picking_ids - pick

        fulfillment = self._import(
            self._payload(917, [(line, 1)], order_binding=order_binding)
        )

        self.assertEqual(fulfillment.state, "synced")
        self.assertEqual(self._done_quantities(pick), {self.widget: 2})
        self.assertFalse(pick.backorder_ids)
        self.assertEqual(self._done_quantities(pack), {self.widget: 1})
        self.assertEqual(pack.backorder_ids.move_ids.product_uom_qty, 1)
        ship = fulfillment.picking_id
        self.assertEqual(ship.picking_type_code, "outgoing")
        self.assertEqual(self._done_quantities(ship), {self.widget: 1})
        self.assertEqual(sale.order_line.qty_delivered, 1)

    def test_fulfillment_ships_the_reserved_lots(self):
        product = self._create_product("Inbound Lot Product", tracking="lot")
        lot = self.env["stock.lot"].create(
            {
                "name": "INBOUND-LOT",
                "product_id": product.id,
                "company_id": self.company.id,
            }
        )
        self._stock(product, 2, lot=lot)
        sale, order_binding, line = self._create_order(840, [(product, 2)])
        sale.action_confirm()
        picking = sale.picking_ids

        fulfillment = self._import(
            self._payload(915, [(line, 1)], order_binding=order_binding)
        )

        self.assertEqual(fulfillment.state, "synced")
        self.assertEqual(picking.state, "done")
        self.assertEqual(picking.move_line_ids.lot_id, lot)
        self.assertEqual(picking.move_line_ids.quantity, 1)
        self.assertEqual(sale.order_line.qty_delivered, 1)

    def test_failed_validation_is_kept_and_retried_after_risk_release(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        self.sale.write({"shopify_risk_hold": True})
        picking.write({"shopify_risk_hold": True})

        fulfillment = self._import(
            self._payload(
                906,
                [(self.widget_line, 2), (self.gadget_line, 2)],
                tracking=[{"company": "FedEx", "number": "7703", "url": ""}],
            )
        )

        self.assertNotEqual(picking.state, "done")
        self.assertFalse(picking.carrier_tracking_ref)
        self.assertFalse(fulfillment.picking_id)
        self.assertEqual(fulfillment.state, "error")
        self.assertIn("high-risk hold", fulfillment.error_message)
        self.assertEqual(
            self.env["shopify.log"].search_count(
                [
                    ("res_model", "=", "shopify.fulfillment"),
                    ("res_id", "=", fulfillment.id),
                    ("level", "=", "error"),
                ]
            ),
            1,
        )
        with trap_jobs() as trap:
            self.sale.action_release_shopify_risk_hold()
        trap.assert_jobs_count(
            1, only=self.env["shopify.fulfillment"]._job_import_from_shopify
        )
        self.assertEqual(fulfillment.state, "pending")

    def test_fulfillment_of_a_delivered_order_is_not_an_error(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        picking.action_assign()
        picking.with_context(skip_shopify_fulfillment_push=True).button_validate()

        fulfillment = self._import(
            self._payload(907, [(self.widget_line, 2), (self.gadget_line, 2)])
        )

        self.assertEqual(fulfillment.state, "synced")
        self.assertFalse(fulfillment.picking_id)
        self.assertEqual(self.sale.picking_ids, picking)

    def test_fulfillment_without_an_open_delivery_is_an_error(self):
        self.sale.action_cancel()

        fulfillment = self._import(
            self._payload(908, [(self.widget_line, 2), (self.gadget_line, 2)])
        )

        self.assertEqual(fulfillment.state, "error")
        self.assertIn("No open Odoo delivery", fulfillment.error_message)

    def test_disabled_validation_only_records_the_fulfillment(self):
        self.instance.fulfillment_auto_validate_webhook = False
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids

        fulfillment = self._import(
            self._payload(909, [(self.widget_line, 2), (self.gadget_line, 2)])
        )

        self.assertEqual(fulfillment.state, "synced")
        self.assertNotEqual(picking.state, "done")

    def test_kit_fulfillment_ships_its_components(self):
        if "mrp.bom" not in self.env:
            self.skipTest("Kits need the Manufacturing app.")
        kit = self._create_product("Inbound Kit")
        self.env["mrp.bom"].create(
            {
                "product_tmpl_id": kit.product_tmpl_id.id,
                "type": "phantom",
                "bom_line_ids": [
                    (0, 0, {"product_id": self.widget.id, "product_qty": 2}),
                    (0, 0, {"product_id": self.gadget.id, "product_qty": 1}),
                ],
            }
        )
        self._stock(self.widget, 4)
        self._stock(self.gadget, 2)
        sale, order_binding, kit_line = self._create_order(820, [(kit, 2)])
        sale.action_confirm()
        picking = sale.picking_ids

        self._import(self._payload(910, [(kit_line, 1)], order_binding=order_binding))

        self.assertEqual(picking.state, "done")
        self.assertEqual(
            self._done_quantities(picking), {self.widget: 2, self.gadget: 1}
        )
        self.assertEqual(
            {
                move.product_id: move.product_uom_qty
                for move in picking.backorder_ids.move_ids
            },
            {self.widget: 2, self.gadget: 1},
        )
        self.assertEqual(sale.order_line.qty_delivered, 1)

    def test_order_import_applies_the_fulfillments_it_missed(self):
        self._stock(self.widget, 2)
        self._stock(self.gadget, 2)
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        payload = self._payload(911, [(self.widget_line, 2), (self.gadget_line, 2)])
        before_its_order = dict(payload, order={"id": "gid://shopify/Order/811"})
        self.assertFalse(self._import(before_its_order))
        client = MagicMock()
        client.execute.side_effect = [
            {
                "order": {
                    "id": self.order_binding.shopify_id,
                    "fulfillmentOrders": {"nodes": []},
                    "fulfillments": [{"id": payload["id"]}],
                }
            },
            {"fulfillment": payload},
        ]

        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            trap_jobs() as trap,
        ):
            self.order_binding._job_refresh_fulfillment_orders()
            trap.assert_jobs_count(1)
            trap.perform_enqueued_jobs()

        self.assertEqual(picking.state, "done")
        self.assertEqual(self.order_binding.fulfillment_ids.picking_id, picking)
