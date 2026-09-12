from decimal import Decimal

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.order import normalize_order_payload
from odoo.addons.shopify_connector_pos.lib.pos import (
    adjusted_pos_total,
    exchange_origin_gid,
    selected_cash_rounding,
)


def _bag(amount, currency="CHF"):
    return {
        "shopMoney": {"amount": amount, "currencyCode": currency},
        "presentmentMoney": {"amount": amount, "currencyCode": currency},
    }


class TestShopifyLibPos(TransactionCase):
    def test_pos_location_and_cash_rounding_normalize_exactly(self):
        order = normalize_order_payload(
            {
                "id": 81,
                "name": "#81",
                "source_name": "pos",
                "currency": "CHF",
                "retail_location": {"id": 91},
                "total_price_set": _bag("10.02"),
                "total_cash_rounding_adjustment": {
                    "payment_set": _bag("0.03"),
                    "refund_set": _bag("-0.01"),
                },
            }
        )
        assert order["source"] == "pos"
        assert order["retail_location_id"] == "gid://shopify/Location/91"
        assert selected_cash_rounding(order, use_presentment=False) == Decimal("0.03")
        assert adjusted_pos_total(order, use_presentment=False) == Decimal("10.05")

    def test_exchange_origin_accepts_graphql_and_webhook_shapes(self):
        assert (
            exchange_origin_gid(
                {"exchangeOriginOrder": {"id": "gid://shopify/Order/10"}}
            )
            == "gid://shopify/Order/10"
        )
        assert (
            exchange_origin_gid({"original_order_id": 11}) == "gid://shopify/Order/11"
        )
        assert exchange_origin_gid({}) == ""
