from decimal import Decimal

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.order import (
    ShopifyOrderPayloadError,
    allocate_amount,
    allocate_refund,
    line_diffs,
    normalize_order_payload,
    normalize_refund_payload,
    selected_money,
)


def bag(shop, presentment, shop_currency="USD", presentment_currency="EUR"):
    return {
        "shopMoney": {"amount": shop, "currencyCode": shop_currency},
        "presentmentMoney": {
            "amount": presentment,
            "currencyCode": presentment_currency,
        },
    }


class TestShopifyLibOrder(TransactionCase):
    def test_money_sets_keep_both_currencies_and_select_without_conversion(self):
        order = normalize_order_payload(
            {
                "id": "gid://shopify/Order/1",
                "name": "#1001",
                "currencyCode": "EUR",
                "currentTotalPriceSet": bag("12.34", "11.37"),
            }
        )
        assert selected_money(order["total"], False) == {
            "amount": "12.34",
            "currency": "USD",
        }
        assert selected_money(order["total"], True) == {
            "amount": "11.37",
            "currency": "EUR",
        }

    def test_rest_webhook_uses_current_quantity_and_exact_discounted_total(self):
        order = normalize_order_payload(
            {
                "id": 10,
                "name": "#10",
                "currency": "USD",
                "total_price_set": {
                    "shop_money": {"amount": "20.00", "currency_code": "USD"}
                },
                "line_items": [
                    {
                        "id": 20,
                        "variant_id": 30,
                        "quantity": 3,
                        "current_quantity": 2,
                        "price_set": {
                            "shop_money": {"amount": "12.00", "currency_code": "USD"}
                        },
                        "total_discount_set": {
                            "shop_money": {"amount": "4.00", "currency_code": "USD"}
                        },
                    }
                ],
            }
        )
        line = order["lines"][0]
        assert line["id"] == "gid://shopify/LineItem/20"
        assert line["variant_id"] == "gid://shopify/ProductVariant/30"
        assert line["quantity"] == 2
        assert line["original_quantity"] == 3
        assert line["discounted_total"]["shop"]["amount"] == "20.00"

    def test_largest_remainder_allocation_is_exact_and_deterministic(self):
        assert allocate_amount("0.05", ["1", "1", "1"], "0.01") == [
            Decimal("0.02"),
            Decimal("0.02"),
            Decimal("0.01"),
        ]
        assert sum(allocate_amount("-10.00", ["1", "2", "3"], "0.01")) == Decimal(
            "-10.00"
        )

    def test_partial_refund_allocation_obeys_remaining_values(self):
        result = allocate_refund(
            "7.01",
            [
                {"id": "a", "refundable_amount": "5.00"},
                {"id": "b", "refundable_amount": "10.00"},
            ],
            "0.01",
        )
        assert [item["allocated_amount"] for item in result] == [
            Decimal("2.34"),
            Decimal("4.67"),
        ]
        assert sum(item["allocated_amount"] for item in result) == Decimal("7.01")

    def test_refund_allocation_rejects_an_overallocation(self):
        with self.assertRaises(ShopifyOrderPayloadError):
            allocate_refund("20.00", [{"id": "a", "refundable_amount": "1.00"}], "0.01")

    def test_line_diff_detects_add_remove_and_current_quantity_edit(self):
        result = line_diffs(
            [{"id": "a", "quantity": 1}, {"id": "b", "quantity": 2}],
            [{"id": "b", "quantity": 3}, {"id": "c", "quantity": 1}],
        )
        assert [line["id"] for line in result["add"]] == ["c"]
        assert [line["id"] for line in result["remove"]] == ["a"]
        assert result["update"][0]["before"]["quantity"] == 2
        assert result["update"][0]["after"]["quantity"] == 3

    def test_refund_webhook_normalizes_restock_and_shipping(self):
        order_id, refund = normalize_refund_payload(
            {
                "id": 99,
                "order_id": 10,
                "currency": "USD",
                "refund_line_items": [
                    {
                        "id": 5,
                        "line_item_id": 20,
                        "quantity": 1,
                        "restock_type": "return",
                        "subtotal": "9.99",
                        "total_tax": "1.00",
                    }
                ],
                "order_adjustments": [
                    {"id": 6, "amount": "2.00", "reason": "shipping_refund"}
                ],
            }
        )
        assert order_id == "gid://shopify/Order/10"
        assert refund["id"] == "gid://shopify/Refund/99"
        assert refund["lines"][0]["restock_type"] == "RETURN"
        assert refund["adjustments"][0]["amount"]["shop"]["amount"] == "2.00"

    def test_return_and_exchange_lifecycle_is_preserved(self):
        order = normalize_order_payload(
            {
                "id": "gid://shopify/Order/1",
                "currencyCode": "USD",
                "currentTotalPriceSet": bag("10.00", "10.00", "USD", "USD"),
                "returns": {
                    "nodes": [
                        {
                            "id": "gid://shopify/Return/2",
                            "name": "#R1",
                            "status": "OPEN",
                            "totalQuantity": 1,
                            "returnLineItems": {
                                "nodes": [
                                    {
                                        "id": "gid://shopify/ReturnLineItem/3",
                                        "quantity": 1,
                                        "refundableQuantity": 1,
                                        "refundedQuantity": 0,
                                        "fulfillmentLineItem": {
                                            "lineItem": {
                                                "id": "gid://shopify/LineItem/4"
                                            }
                                        },
                                    }
                                ]
                            },
                            "exchangeLineItems": {
                                "nodes": [
                                    {
                                        "id": "gid://shopify/ExchangeLineItem/5",
                                        "quantity": 1,
                                        "variantId": "gid://shopify/ProductVariant/6",
                                        "lineItem": {"id": "gid://shopify/LineItem/7"},
                                    }
                                ]
                            },
                        }
                    ]
                },
            }
        )
        assert order["returns"][0]["status"] == "OPEN"
        assert order["returns"][0]["lines"][0]["line_id"].endswith("/4")
        assert order["returns"][0]["exchange_lines"][0]["variant_id"].endswith("/6")
