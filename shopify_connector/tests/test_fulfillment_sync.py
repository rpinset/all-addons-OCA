from unittest.mock import MagicMock, patch

from odoo.tests.common import TransactionCase

from ..lib.fulfillment import (
    FulfillmentAllocationError,
    allocate_fulfillment_lines,
)


class TestShopifyFulfillmentSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Fulfillment Shop",
                "shop_url": "fulfillment-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.product = cls.env["product.product"].create(
            {
                "name": "Fulfilled Widget",
                "type": "consu",
                "is_storable": True,
                "company_id": cls.instance.company_id.id,
            }
        )
        template_binding = cls.env["shopify.product.template"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Product/600",
                "odoo_id": cls.product.product_tmpl_id.id,
                "status": "ACTIVE",
                "state": "synced",
            }
        )
        cls.variant_binding = cls.env["shopify.product.variant"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/ProductVariant/601",
                "template_binding_id": template_binding.id,
                "odoo_id": cls.product.id,
                "state": "synced",
            }
        )
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.instance.company_id.id)],
            limit=1,
        )
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Fulfillment Customer",
                "company_id": cls.instance.company_id.id,
            }
        )
        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.customer.id,
                "company_id": cls.instance.company_id.id,
                "warehouse_id": cls.warehouse.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 10,
                        },
                    )
                ],
            }
        )
        cls.order_binding = cls.env["shopify.order"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Order/610",
                "odoo_id": cls.sale.id,
                "order_name": "#610",
                "state": "synced",
            }
        )
        cls.line_binding = cls.env["shopify.order.line"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/LineItem/611",
                "order_binding_id": cls.order_binding.id,
                "odoo_id": cls.sale.order_line.id,
                "variant_shopify_id": cls.variant_binding.shopify_id,
                "state": "synced",
            }
        )

    def test_picking_validation_enqueues_fulfillment_job(self):
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.warehouse.lot_stock_id, 1
        )
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        picking.action_assign()
        picking.move_ids.quantity = 1

        with (
            patch.object(
                type(self.order_binding),
                "with_delay",
                return_value=self.order_binding,
            ) as with_delay,
            patch.object(
                type(self.order_binding),
                "_job_push_picking_fulfillment",
                return_value=True,
            ) as push,
        ):
            picking.button_validate()

        self.assertEqual(picking.state, "done")
        with_delay.assert_called_once()
        self.assertEqual(
            with_delay.call_args.kwargs["identity_key"],
            (
                f"shopify.fulfillment.push.{self.instance.id}."
                f"{self.order_binding.id}.{picking.id}"
            ),
        )
        push.assert_called_once_with(picking.id)

    def test_partial_allocation_uses_only_delivered_quantity(self):
        allocation = allocate_fulfillment_lines(
            [
                {
                    "move_id": 1,
                    "line_id": self.line_binding.shopify_id,
                    "quantity": 2,
                }
            ],
            [
                {
                    "id": "gid://shopify/FulfillmentOrder/620",
                    "location_id": "gid://shopify/Location/1",
                    "status": "OPEN",
                    "line_items": [
                        {
                            "id": "gid://shopify/FulfillmentOrderLineItem/621",
                            "line_id": self.line_binding.shopify_id,
                            "remaining_quantity": 5,
                        }
                    ],
                }
            ],
            target_location_id="gid://shopify/Location/1",
        )

        self.assertEqual(allocation["groups"][0]["line_items"][0]["quantity"], 2)

    def test_location_mismatch_without_move_action_is_clear(self):
        with self.assertRaisesRegex(FulfillmentAllocationError, "cannot be fulfilled"):
            allocate_fulfillment_lines(
                [
                    {
                        "move_id": 1,
                        "line_id": self.line_binding.shopify_id,
                        "quantity": 1,
                    }
                ],
                [
                    {
                        "id": "gid://shopify/FulfillmentOrder/630",
                        "location_id": "gid://shopify/Location/2",
                        "status": "OPEN",
                        "supported_actions": [],
                        "line_items": [
                            {
                                "id": ("gid://shopify/FulfillmentOrderLineItem/631"),
                                "line_id": self.line_binding.shopify_id,
                                "remaining_quantity": 1,
                            }
                        ],
                    }
                ],
                target_location_id="gid://shopify/Location/1",
            )

    def test_connector_fulfillment_webhook_is_echo_guarded(self):
        fulfillment = self.env["shopify.fulfillment"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": "gid://shopify/Fulfillment/640",
                "order_binding_id": self.order_binding.id,
                "origin": "odoo",
                "state": "synced",
            }
        )
        client = MagicMock()
        client.execute.return_value = {
            "fulfillment": {
                "id": fulfillment.shopify_id,
                "status": "SUCCESS",
                "order": {"id": self.order_binding.shopify_id},
                "location": {"id": "gid://shopify/Location/1"},
                "trackingInfo": {},
                "fulfillmentLineItems": {"nodes": []},
            }
        }

        with (
            patch.object(
                type(self.instance),
                "_shopify_client",
                return_value=client,
            ),
            patch.object(
                type(fulfillment),
                "_auto_validate_external",
            ) as auto_validate,
        ):
            result = self.env["shopify.fulfillment"]._job_import_from_shopify(
                self.instance.id,
                fulfillment.shopify_id,
                {"order_id": 610, "status": "success"},
            )

        self.assertEqual(result, fulfillment.id)
        self.assertEqual(fulfillment.fulfillment_status, "SUCCESS")
        auto_validate.assert_not_called()
