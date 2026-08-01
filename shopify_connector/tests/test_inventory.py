from unittest.mock import Mock, patch

from odoo import fields
from odoo.tests.common import TransactionCase


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
