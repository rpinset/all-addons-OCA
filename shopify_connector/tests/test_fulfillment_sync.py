from unittest.mock import MagicMock, patch

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase, new_test_user

from ..graphql.fulfillment import (
    FULFILLMENT_BY_ID_QUERY,
    FULFILLMENT_CREATE_MUTATION,
    ORDER_FULFILLMENT_ORDERS_QUERY,
    ORDER_FULFILLMENTS_QUERY,
)
from ..lib.fulfillment import (
    FulfillmentAllocationError,
    allocate_fulfillment_lines,
)

LOCATION_ID = "gid://shopify/Location/650"


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

    def test_stock_user_can_validate_picking_of_shopify_order(self):
        stock_user = new_test_user(
            self.env,
            login="shopify_validate_stock_user",
            groups="stock.group_stock_user",
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.warehouse.lot_stock_id, 1
        )
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        picking.action_assign()
        picking.move_ids.quantity = 1
        # A request starts with a cold cache: the order bindings must be fetched
        # with the user's access rights, which do not cover shopify.order.
        self.env.invalidate_all()

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
            picking.with_user(stock_user).button_validate()

        self.assertEqual(picking.state, "done")
        with_delay.assert_called_once()
        push.assert_called_once_with(picking.id)
        self.env.invalidate_all()
        with self.assertRaises(AccessError):
            self.sale.with_user(stock_user).shopify_binding_ids.mapped("shopify_id")

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

    def test_stock_user_can_cancel_picking_with_fulfillment(self):
        stock_user = new_test_user(
            self.env,
            login="shopify_cancel_stock_user",
            groups="stock.group_stock_user",
        )
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        fulfillment = self.env["shopify.fulfillment"].create(
            {
                "instance_id": self.instance.id,
                "order_binding_id": self.order_binding.id,
                "picking_id": picking.id,
                "shopify_id": "gid://shopify/Fulfillment/620",
            }
        )
        # A request starts with a cold cache: the fulfillments must be fetched
        # with the user's access rights, which do not cover shopify.fulfillment.
        self.env.invalidate_all()

        picking.with_user(stock_user).action_cancel()

        self.assertEqual(picking.state, "cancel")
        log = self.env["shopify.log"].search(
            [
                ("res_model", "=", "shopify.fulfillment"),
                ("res_id", "=", fulfillment.id),
                ("level", "=", "warning"),
            ]
        )
        self.assertEqual(len(log), 1)
        self.assertIn(picking.name, log.message)
        self.env.invalidate_all()
        with self.assertRaises(AccessError):
            picking.with_user(stock_user).shopify_fulfillment_ids.mapped("shopify_id")

    def _delivered_picking(self):
        self.env["shopify.location"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": LOCATION_ID,
                "legacy_resource_id": "650",
                "name": "Fulfillment Location",
                "active": True,
                "state": "synced",
                "warehouse_id": self.warehouse.id,
                "odoo_location_id": self.warehouse.lot_stock_id.id,
            }
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.warehouse.lot_stock_id, 1
        )
        self.sale.action_confirm()
        picking = self.sale.picking_ids
        picking.action_assign()
        picking.move_ids.quantity = 1
        picking.with_context(skip_shopify_fulfillment_push=True).button_validate()
        self.assertEqual(picking.state, "done")
        return picking

    def _unconfirmed_attempt(self, picking):
        # A push whose fulfillmentCreate response was lost: Shopify may or may
        # not have created the fulfillment.
        return self.env["shopify.fulfillment"].create(
            {
                "instance_id": self.instance.id,
                "order_binding_id": self.order_binding.id,
                "picking_id": picking.id,
                "idempotency_key": f"picking:{picking.id}",
                "origin": "odoo",
                "location_shopify_id": LOCATION_ID,
                "state": "error",
                "error_message": "Read timed out.",
            }
        )

    def _shopify_fulfillment(self, number, *, quantity=1):
        return {
            "id": f"gid://shopify/Fulfillment/{number}",
            "status": "SUCCESS",
            "createdAt": fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updatedAt": fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "order": {"id": self.order_binding.shopify_id},
            "location": {"id": LOCATION_ID},
            "trackingInfo": [],
            "fulfillmentLineItems": {
                "nodes": [
                    {
                        "quantity": quantity,
                        "lineItem": {"id": self.line_binding.shopify_id},
                    }
                ]
            },
        }

    def _client(self, fulfillments, remaining_quantity=0):
        fulfillment_order = {
            "id": "gid://shopify/FulfillmentOrder/660",
            "status": "OPEN" if remaining_quantity else "CLOSED",
            "assignedLocation": {"location": {"id": LOCATION_ID, "name": "Main"}},
            "supportedActions": [],
            "fulfillmentHolds": [],
            "lineItems": {
                "nodes": [
                    {
                        "id": "gid://shopify/FulfillmentOrderLineItem/661",
                        "totalQuantity": 1,
                        "remainingQuantity": remaining_quantity,
                        "lineItem": {"id": self.line_binding.shopify_id},
                    }
                ]
            },
        }

        def execute(query, variables=None):
            if query == ORDER_FULFILLMENTS_QUERY:
                return {
                    "order": {
                        "id": self.order_binding.shopify_id,
                        "fulfillments": fulfillments,
                    }
                }
            if query == ORDER_FULFILLMENT_ORDERS_QUERY:
                return {
                    "order": {
                        "id": self.order_binding.shopify_id,
                        "fulfillmentOrders": {"nodes": [fulfillment_order]},
                        "fulfillments": [{"id": item["id"]} for item in fulfillments],
                    }
                }
            if query == FULFILLMENT_BY_ID_QUERY:
                return {
                    "fulfillment": next(
                        item for item in fulfillments if item["id"] == variables["id"]
                    )
                }
            if query == FULFILLMENT_CREATE_MUTATION:
                return {
                    "fulfillmentCreate": {
                        "fulfillment": {
                            "id": "gid://shopify/Fulfillment/690",
                            "status": "SUCCESS",
                        },
                        "userErrors": [],
                    }
                }
            raise AssertionError(f"Unexpected Shopify query: {query}")

        client = MagicMock()
        client.execute.side_effect = execute
        return client

    def _executed(self, client, query):
        return [call for call in client.execute.call_args_list if call.args[0] == query]

    def test_unconfirmed_push_binds_the_fulfillment_shopify_created(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        client = self._client([self._shopify_fulfillment(670)])

        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            result = self.order_binding._job_push_picking_fulfillment(picking.id)

        self.assertEqual(result, attempt.id)
        self.assertEqual(attempt.shopify_id, "gid://shopify/Fulfillment/670")
        self.assertEqual(attempt.state, "synced")
        self.assertFalse(attempt.error_message)
        self.assertFalse(self._executed(client, FULFILLMENT_CREATE_MUTATION))

    def test_unconfirmed_push_is_sent_again_when_shopify_has_nothing(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        # An older fulfillment of the order, created before the attempt, is
        # not a candidate.
        older = self._shopify_fulfillment(671)
        older["createdAt"] = "2020-01-01T00:00:00Z"
        client = self._client([older], remaining_quantity=1)

        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            result = self.order_binding._job_push_picking_fulfillment(picking.id)

        self.assertFalse(attempt.exists())
        binding = self.env["shopify.fulfillment"].browse(result)
        self.assertEqual(binding.shopify_id, "gid://shopify/Fulfillment/690")
        self.assertEqual(binding.picking_id, picking)
        self.assertEqual(binding.state, "synced")
        self.assertEqual(len(self._executed(client, FULFILLMENT_CREATE_MUTATION)), 1)

    def test_unconfirmed_push_with_several_candidates_stays_blocked(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        client = self._client(
            [self._shopify_fulfillment(672), self._shopify_fulfillment(673)]
        )

        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            self.assertRaisesRegex(UserError, "Fulfillment/672.*Fulfillment/673"),
        ):
            self.order_binding._job_push_picking_fulfillment(picking.id)

        self.assertFalse(attempt.shopify_id)
        self.assertFalse(self._executed(client, FULFILLMENT_CREATE_MUTATION))

    def test_unconfirmed_push_adopts_its_webhook_import(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        payload = self._shopify_fulfillment(674)
        # The webhook arrived first and imported the push as external.
        imported = self.env["shopify.fulfillment"].create(
            {
                "instance_id": self.instance.id,
                "order_binding_id": self.order_binding.id,
                "shopify_id": payload["id"],
                "origin": "shopify",
                "state": "synced",
            }
        )
        client = self._client([payload])

        with patch.object(type(self.instance), "_shopify_client", return_value=client):
            result = self.order_binding._job_push_picking_fulfillment(picking.id)

        self.assertEqual(result, imported.id)
        self.assertFalse(attempt.exists())
        self.assertEqual(imported.origin, "odoo")
        self.assertEqual(imported.picking_id, picking)
        self.assertEqual(imported.idempotency_key, f"picking:{picking.id}")
        self.assertFalse(self._executed(client, FULFILLMENT_CREATE_MUTATION))

    def test_missed_fulfillment_import_recognises_an_unconfirmed_push(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        client = self._client([self._shopify_fulfillment(676)])
        fulfillment_model = self.env["shopify.fulfillment"]

        # The refresh queues the import of fulfillments Odoo does not know;
        # run that import right away.
        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            patch.object(
                type(fulfillment_model), "with_delay", return_value=fulfillment_model
            ),
            patch.object(
                type(fulfillment_model), "_auto_validate_external"
            ) as auto_validate,
        ):
            self.order_binding._job_refresh_fulfillment_orders()

        self.assertEqual(attempt.shopify_id, "gid://shopify/Fulfillment/676")
        self.assertEqual(attempt.origin, "odoo")
        self.assertEqual(attempt.state, "synced")
        self.assertEqual(
            fulfillment_model.search_count(
                [("shopify_id", "=", "gid://shopify/Fulfillment/676")]
            ),
            1,
        )
        auto_validate.assert_not_called()

    def test_webhook_of_unconfirmed_push_is_treated_as_echo(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)
        payload = self._shopify_fulfillment(675)
        client = MagicMock()
        client.execute.return_value = {"fulfillment": payload}

        with (
            patch.object(type(self.instance), "_shopify_client", return_value=client),
            patch.object(
                type(attempt),
                "_auto_validate_external",
            ) as auto_validate,
        ):
            result = self.env["shopify.fulfillment"]._job_import_from_shopify(
                self.instance.id,
                payload["id"],
                {"order_id": 610, "status": "success"},
            )

        self.assertEqual(result, attempt.id)
        self.assertEqual(attempt.shopify_id, payload["id"])
        self.assertEqual(attempt.origin, "odoo")
        self.assertEqual(attempt.state, "synced")
        auto_validate.assert_not_called()

    def test_retry_of_unconfirmed_push_queues_the_push(self):
        picking = self._delivered_picking()
        attempt = self._unconfirmed_attempt(picking)

        with (
            patch.object(
                type(self.order_binding),
                "with_delay",
                return_value=self.order_binding,
            ),
            patch.object(
                type(self.order_binding),
                "_job_push_picking_fulfillment",
                return_value=True,
            ) as push,
        ):
            attempt.action_retry_sync()

        push.assert_called_once_with(picking.id)
