from datetime import timedelta
from unittest.mock import Mock, patch

from odoo import Command, fields
from odoo.tests.common import TransactionCase

from odoo.addons.queue_job.exception import RetryableJobError
from odoo.addons.queue_job.job import Job


class TestShopifyInventory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Inventory Shop",
                "shop_url": "inventory-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
                "inventory_import_enabled": True,
            }
        )
        cls.instance.state = "connected"
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.instance.company_id.id)], limit=1
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Inventory Product",
                "default_code": "INV-1",
                "company_id": cls.instance.company_id.id,
                "is_storable": True,
            }
        )
        cls.template_binding = cls.env["shopify.product.template"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Product/100",
                "odoo_id": cls.product.product_tmpl_id.id,
                "state": "synced",
            }
        )
        cls.variant_binding = cls.env["shopify.product.variant"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/ProductVariant/101",
                "template_binding_id": cls.template_binding.id,
                "odoo_id": cls.product.id,
                "inventory_item_shopify_id": ("gid://shopify/InventoryItem/201"),
                "inventory_tracked": True,
                "state": "synced",
            }
        )

    def _location_binding(self, *, mapped=True):
        values = {
            "instance_id": self.instance.id,
            "shopify_id": "gid://shopify/Location/301",
            "legacy_resource_id": "301",
            "name": "Main Location",
            "active": True,
            "state": "synced",
        }
        if mapped:
            values.update(
                {
                    "warehouse_id": self.warehouse.id,
                    "odoo_location_id": self.warehouse.lot_stock_id.id,
                }
            )
        return self.env["shopify.location"].create(values)

    def test_unmapped_location_refuses_inventory_write_and_logs(self):
        location = self._location_binding(mapped=False)

        result = self.variant_binding._inventory_mapping_or_log(location)

        self.assertFalse(result)
        self.assertTrue(
            self.env["shopify.log"].search(
                [
                    ("instance_id", "=", self.instance.id),
                    ("entity", "=", "inventory"),
                    ("level", "=", "error"),
                ],
                limit=1,
            )
        )

    def _inventory_item_response(self, level):
        return {
            "inventoryItem": {
                "id": "gid://shopify/InventoryItem/201",
                "tracked": True,
                "inventoryLevel": level,
            }
        }

    def test_read_shopify_quantity_returns_available_from_stocked_level(self):
        location = self._location_binding()
        client = Mock()
        client.execute.return_value = self._inventory_item_response(
            {
                "id": "gid://shopify/InventoryLevel/1",
                "quantities": [{"name": "available", "quantity": 7}],
            }
        )

        quantity = self.variant_binding._read_shopify_inventory_quantity(
            client, location
        )

        self.assertEqual(quantity, 7)

    def test_read_shopify_quantity_is_none_when_item_not_stocked_at_location(self):
        location = self._location_binding()
        client = Mock()
        client.execute.return_value = self._inventory_item_response(None)

        quantity = self.variant_binding._read_shopify_inventory_quantity(
            client, location
        )

        self.assertIsNone(quantity)

    def test_quant_change_enqueues_location_scoped_delta_job(self):
        location = self._location_binding()
        delayed = Mock()
        binding_model_class = type(self.variant_binding)

        with patch.object(
            binding_model_class,
            "with_delay",
            autospec=True,
            return_value=delayed,
        ) as with_delay:
            self.env["stock.quant"].create(
                {
                    "product_id": self.product.id,
                    "location_id": self.warehouse.lot_stock_id.id,
                    "quantity": 2,
                }
            )

        self.assertIn(
            f".{self.variant_binding.id}.{location.id}",
            with_delay.call_args.kwargs["identity_key"],
        )
        delayed._job_push_inventory_level.assert_called_once_with(location.id)

    def test_matching_recent_webhook_is_ignored_as_echo(self):
        location = self._location_binding()
        self.env["shopify.inventory.state"].create(
            {
                "instance_id": self.instance.id,
                "variant_binding_id": self.variant_binding.id,
                "location_binding_id": location.id,
                "last_pushed_quantity": 5,
                "last_pushed_at": fields.Datetime.now(),
            }
        )
        event = self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": "inventory-webhook-1",
                "topic": "inventory_levels/update",
                "payload": {
                    "inventory_item_id": 201,
                    "location_id": 301,
                    "available": 5,
                },
            }
        )

        event._handle_inventory_level_update()

        log = self.env["shopify.log"].search(
            [
                ("instance_id", "=", self.instance.id),
                ("entity", "=", "inventory"),
            ],
            order="id desc",
            limit=1,
        )
        self.assertIn("echo", log.message.lower())

    # An order placed in Shopify lowers its available quantity, and Odoo
    # lowers its own stock when the order's delivery is validated. Before,
    # the inventory webhook set Odoo to Shopify's available quantity as well,
    # so each sale was taken out of Odoo twice.

    def _stock(self):
        self.env.invalidate_all()
        return self.product.with_context(
            location=self.warehouse.lot_stock_id.id
        ).qty_available

    def _set_stock(self, quantity):
        self.env["stock.quant"].with_context(
            skip_shopify_inventory_export=True
        )._update_available_quantity(
            self.product, self.warehouse.lot_stock_id, quantity - self._stock()
        )

    def _webhook(self, number, available, level, received_ago=None):
        client = Mock()
        client.execute.return_value = self._inventory_item_response(
            {
                "id": "gid://shopify/InventoryLevel/1",
                "quantities": [
                    {"name": name, "quantity": value} for name, value in level.items()
                ],
            }
        )
        event = self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": f"inventory-webhook-order-{number}",
                "topic": "inventory_levels/update",
                "payload": {
                    "inventory_item_id": 201,
                    "location_id": 301,
                    "available": available,
                },
            }
        )
        if received_ago:
            self.env.cr.execute(
                "UPDATE shopify_webhook_event SET create_date = %s WHERE id = %s",
                (fields.Datetime.now() - received_ago, event.id),
            )
            event.invalidate_recordset(["create_date"])
        with patch.object(
            type(self.instance), "_shopify_client", autospec=True, return_value=client
        ):
            event._handle_inventory_level_update()

    def _snapshot(self, location, on_hand):
        return self.env["shopify.inventory.state"].create(
            {
                "instance_id": self.instance.id,
                "variant_binding_id": self.variant_binding.id,
                "location_binding_id": location.id,
                "last_shopify_on_hand": on_hand,
                "shopify_snapshot_at": fields.Datetime.now(),
            }
        )

    def _fulfilled(self, location, quantity):
        # What the connector records when it pushes or imports a fulfillment.
        self.env["shopify.inventory.state"]._record_fulfilled_quantities(
            self.instance,
            location.shopify_id,
            {self.variant_binding.shopify_id: quantity},
        )

    def test_a_shopify_sale_delivered_from_odoo_is_taken_out_once(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)

        # A first order is placed in Shopify: one unit moves to committed.
        self._webhook(1, 7, {"available": 7, "on_hand": 8})
        self.assertEqual(self._stock(), 8)

        # Its delivery is validated in Odoo and fulfilled in Shopify, which
        # sends no inventory webhook for a fulfillment.
        self._set_stock(7)
        self._fulfilled(location, 1)

        # The next order's webhook comes after that fulfillment.
        self._webhook(2, 6, {"available": 6, "on_hand": 7})
        self.assertEqual(self._stock(), 7)

    def test_a_receipt_after_a_fulfillment_is_applied_whole(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)
        self._set_stock(7)
        self._fulfilled(location, 1)

        # Five units received in Shopify.
        self._webhook(3, 12, {"available": 12, "on_hand": 12})

        self.assertEqual(self._stock(), 12)

    def test_a_count_with_a_cancelled_order_is_applied_whole(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)

        # An order is cancelled, which gives its unit back to available, and
        # two units are counted out in the same interval.
        self._webhook(4, 6, {"available": 6, "on_hand": 6})

        self.assertEqual(self._stock(), 6)

    def test_a_count_made_in_shopify_reaches_odoo(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)

        self._webhook(5, 10, {"available": 10, "on_hand": 10})

        self.assertEqual(self._stock(), 10)

    def test_the_first_webhook_brings_odoo_to_shopifys_on_hand_stock(self):
        location = self._location_binding()
        self._set_stock(5)

        self._webhook(6, 7, {"available": 7, "on_hand": 8})

        self.assertEqual(self._stock(), 8)
        state = self.env["shopify.inventory.state"].search(
            [("location_binding_id", "=", location.id)]
        )
        self.assertEqual(state.last_shopify_on_hand, 8)

    def test_a_fulfillment_is_recorded_only_once_shopify_was_read(self):
        location = self._location_binding()
        self._fulfilled(location, 1)
        self.assertFalse(
            self.env["shopify.inventory.state"].search(
                [("location_binding_id", "=", location.id)]
            )
        )

        state = self._snapshot(location, on_hand=8)
        self._fulfilled(location, 2)

        self.assertEqual(state.last_shopify_on_hand, 6)

    def _delivery_pushing(self, product):
        # A delivery validated in Odoo whose fulfillment is being pushed.
        stock = self.warehouse.lot_stock_id
        customers = self.env.ref("stock.stock_location_customers")
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.warehouse.out_type_id.id,
                "location_id": stock.id,
                "location_dest_id": customers.id,
                "move_ids": [
                    Command.create(
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "product_uom": product.uom_id.id,
                            "location_id": stock.id,
                            "location_dest_id": customers.id,
                        }
                    )
                ],
            }
        )
        push = Job(
            self.instance._job_import_locations,
            channel="root.shopify.export",
            identity_key=f"shopify.fulfillment.push.{self.instance.id}.1.{picking.id}",
        )
        push.store()
        return push

    def test_a_change_waits_for_the_fulfillments_being_recorded(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)
        # Odoo has delivered one unit, and its fulfillment is being pushed.
        self._set_stock(7)
        push = self._delivery_pushing(self.product)

        # An order placed meanwhile leaves the on-hand stock alone.
        self._webhook(7, 6, {"available": 6, "on_hand": 8})
        self.assertEqual(self._stock(), 7)

        # Shopify has fulfilled the delivery before the push recorded it.
        with self.assertRaises(RetryableJobError):
            self._webhook(8, 5, {"available": 5, "on_hand": 7})
        self.assertEqual(self._stock(), 7)

        # The push records it and ends; the webhook runs again.
        self._fulfilled(location, 1)
        push.db_record().state = "done"
        self._webhook(9, 5, {"available": 5, "on_hand": 7})
        self.assertEqual(self._stock(), 7)

    def test_a_change_waits_only_for_fulfillments_of_its_variant(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)
        other = self.env["product.product"].create(
            {"name": "Other Inventory Product", "is_storable": True}
        )
        self._delivery_pushing(other)
        for number, variant_id in ((10, 999), (11, 101)):
            self.env["shopify.webhook.event"].create(
                {
                    "instance_id": self.instance.id,
                    "webhook_id": f"fulfillment-webhook-{number}",
                    "topic": "fulfillments/create",
                    "state": "queued",
                    "payload": {
                        "location_id": 302 if variant_id == 101 else 301,
                        "line_items": [{"variant_id": variant_id, "quantity": 1}],
                    },
                }
            )

        # Two units counted out in Shopify.
        self._webhook(12, 6, {"available": 6, "on_hand": 6})
        self.assertEqual(self._stock(), 6)

        # A fulfillment of this variant at this location, not imported yet.
        self.env["shopify.webhook.event"].create(
            {
                "instance_id": self.instance.id,
                "webhook_id": "fulfillment-webhook-14",
                "topic": "fulfillments/create",
                "state": "queued",
                "payload": {
                    "location_id": 301,
                    "line_items": [{"variant_id": 101, "quantity": 1}],
                },
            }
        )
        with self.assertRaises(RetryableJobError):
            self._webhook(15, 5, {"available": 5, "on_hand": 5})
        self.assertEqual(self._stock(), 6)

    def test_a_change_is_applied_once_it_has_waited_too_long(self):
        location = self._location_binding()
        self._set_stock(8)
        self._snapshot(location, on_hand=8)
        self._delivery_pushing(self.product)

        self._webhook(
            13, 6, {"available": 6, "on_hand": 6}, received_ago=timedelta(minutes=11)
        )

        self.assertEqual(self._stock(), 6)
        self.assertTrue(
            self.env["shopify.log"].search(
                [
                    ("instance_id", "=", self.instance.id),
                    ("entity", "=", "inventory"),
                    ("level", "=", "warning"),
                ],
                limit=1,
            )
        )
