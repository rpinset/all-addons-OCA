from odoo.tests.common import TransactionCase


class TestShopifyPosImport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "POS Shop",
                "shop_url": "pos-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.currency = cls.instance.company_id.currency_id
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.instance.company_id.id)],
            limit=1,
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "POS Widget",
                "default_code": "POS-WIDGET",
                "type": "consu",
                "is_storable": True,
                "company_id": cls.instance.company_id.id,
            }
        )
        template_binding = cls.env["shopify.product.template"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Product/801",
                "odoo_id": cls.product.product_tmpl_id.id,
                "status": "ACTIVE",
                "state": "synced",
            }
        )
        cls.variant_binding = cls.env["shopify.product.variant"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/ProductVariant/802",
                "template_binding_id": template_binding.id,
                "odoo_id": cls.product.id,
                "state": "synced",
            }
        )
        cls.location = cls.env["shopify.location"].create(
            {
                "instance_id": cls.instance.id,
                "shopify_id": "gid://shopify/Location/803",
                "legacy_resource_id": "803",
                "name": "Retail Store",
                "active": True,
                "warehouse_id": cls.warehouse.id,
                "odoo_location_id": cls.warehouse.lot_stock_id.id,
                "state": "synced",
            }
        )

    def _bag(self, amount):
        return {
            "shopMoney": {
                "amount": amount,
                "currencyCode": self.currency.name,
            },
            "presentmentMoney": {
                "amount": amount,
                "currencyCode": self.currency.name,
            },
        }

    def _payload(self, order_id):
        return {
            "id": f"gid://shopify/Order/{order_id}",
            "name": f"POS-{order_id}",
            "createdAt": "2026-07-25T10:00:00Z",
            "updatedAt": "2026-07-25T10:00:00Z",
            "sourceName": "pos",
            "sourceIdentifier": f"receipt-{order_id}",
            "retailLocation": {"id": self.location.shopify_id},
            "currencyCode": self.currency.name,
            "presentmentCurrencyCode": self.currency.name,
            "displayFinancialStatus": "PAID",
            "displayFulfillmentStatus": "FULFILLED",
            "currentSubtotalPriceSet": self._bag("10.00"),
            "currentTotalDiscountsSet": self._bag("0.00"),
            "currentShippingPriceSet": self._bag("0.00"),
            "currentTotalTaxSet": self._bag("0.00"),
            "currentTotalPriceSet": self._bag("10.00"),
            "totalCashRoundingAdjustment": {
                "paymentSet": self._bag("0.00"),
                "refundSet": self._bag("0.00"),
            },
            "lineItems": {
                "nodes": [
                    {
                        "id": f"gid://shopify/LineItem/{order_id}",
                        "name": self.product.name,
                        "sku": self.product.default_code,
                        "quantity": 1,
                        "currentQuantity": 1,
                        "refundableQuantity": 1,
                        "variant": {
                            "id": self.variant_binding.shopify_id,
                        },
                        "product": {
                            "id": (self.variant_binding.template_binding_id.shopify_id),
                        },
                        "originalUnitPriceSet": self._bag("10.00"),
                        "discountedUnitPriceAfterAllDiscountsSet": self._bag("10.00"),
                        "discountedTotalSet": self._bag("10.00"),
                        "taxLines": [],
                        "discountAllocations": [],
                    }
                ]
            },
            "shippingLines": {"nodes": []},
            "transactions": [],
            "refunds": {"nodes": []},
            "returns": {"nodes": []},
            "tags": [],
            "discountCodes": [],
        }

    def test_disabled_pos_import_stays_pending(self):
        self.instance.pos_enabled = False

        binding_id = self.env["shopify.order"]._job_import_order(
            self.instance.id, self._payload(810)
        )
        binding = self.env["shopify.order"].browse(binding_id)

        self.assertEqual(binding.state, "pending")
        self.assertEqual(binding.source, "pos")
        self.assertFalse(binding.odoo_id)

        self.instance.write(
            {
                "pos_enabled": True,
                "pos_auto_confirm": False,
                "pos_auto_fulfill": False,
            }
        )
        rerun_id = self.env["shopify.order"]._job_import_order(
            self.instance.id, self._payload(810)
        )
        rerun = self.env["shopify.order"].browse(rerun_id)

        self.assertEqual(rerun, binding)
        self.assertEqual(rerun.state, "synced")
        self.assertTrue(rerun.odoo_id)

    def test_enabled_pos_import_routes_and_confirms_independently(self):
        self.instance.write(
            {
                "pos_enabled": True,
                "pos_auto_confirm": True,
                "pos_auto_fulfill": False,
                "order_confirmation_policy": "quotation",
            }
        )

        binding_id = self.env["shopify.order"]._job_import_order(
            self.instance.id, self._payload(811)
        )
        binding = self.env["shopify.order"].browse(binding_id)

        self.assertEqual(binding.state, "synced")
        self.assertEqual(binding.pos_location_id, self.location)
        self.assertEqual(binding.odoo_id.warehouse_id, self.warehouse)
        self.assertEqual(binding.odoo_id.state, "sale")

    def test_pos_delivery_is_validated_immediately_from_mapped_stock(self):
        self.instance.write(
            {
                "pos_enabled": True,
                "pos_auto_confirm": True,
                "pos_auto_fulfill": True,
            }
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.warehouse.lot_stock_id, 1
        )

        binding_id = self.env["shopify.order"]._job_import_order(
            self.instance.id, self._payload(812)
        )
        order = self.env["shopify.order"].browse(binding_id).odoo_id

        self.assertTrue(order.shopify_pos_order)
        self.assertTrue(order.picking_ids)
        self.assertTrue(all(picking.state == "done" for picking in order.picking_ids))

    def test_pos_walk_in_uses_instance_guest_partner(self):
        self.instance.write(
            {
                "pos_enabled": True,
                "pos_auto_confirm": False,
                "pos_auto_fulfill": False,
            }
        )

        binding_id = self.env["shopify.order"]._job_import_order(
            self.instance.id, self._payload(813)
        )
        order = self.env["shopify.order"].browse(binding_id).odoo_id

        self.assertEqual(order.partner_id, self.instance.guest_partner_id)
