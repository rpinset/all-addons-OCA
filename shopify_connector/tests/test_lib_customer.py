from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.customer import (
    ShopifyCustomerPayloadError,
    diff_customer_addresses,
    normalize_customer_payload,
    normalize_email,
    normalize_phone,
    phone_search_suffix,
)


class TestShopifyLibCustomer(TransactionCase):
    def test_email_normalization_is_case_insensitive_and_trimmed(self):
        assert (
            normalize_email("  Alice.Example@SHOP.test ") == "alice.example@shop.test"
        )
        assert normalize_email(None) == ""

    def test_phone_normalization_handles_common_e164_edges_1(self):
        raw, country, expected = ("+1 (415) 555-2671", None, "+14155552671")
        assert normalize_phone(raw, country) == expected

    def test_phone_normalization_handles_common_e164_edges_2(self):
        raw, country, expected = ("0044 20 7946 0958", None, "+442079460958")
        assert normalize_phone(raw, country) == expected

    def test_phone_normalization_handles_common_e164_edges_3(self):
        raw, country, expected = ("0812-3456-7890", "62", "+6281234567890")
        assert normalize_phone(raw, country) == expected

    def test_phone_normalization_handles_common_e164_edges_4(self):
        raw, country, expected = ("+33 1 42 68 53 00 ext. 9", None, "+33142685300")
        assert normalize_phone(raw, country) == expected

    def test_phone_normalization_handles_common_e164_edges_5(self):
        raw, country, expected = ("555-0123", None, "5550123")
        assert normalize_phone(raw, country) == expected

    def test_phone_normalization_handles_common_e164_edges_6(self):
        raw, country, expected = ("", "62", "")
        assert normalize_phone(raw, country) == expected

    def test_phone_search_suffix_is_selective_and_format_independent(self):
        assert phone_search_suffix("+62 812 3456-7890") == "7890"
        assert phone_search_suffix("+14155552671", digits=7) == "5552671"
        assert phone_search_suffix("123") == ""

    def test_customer_normalization_handles_webhook_shape_and_default_address(self):
        customer = normalize_customer_payload(
            {
                "id": 42,
                "first_name": "Alice",
                "last_name": "Ng",
                "email": "Alice@Example.COM",
                "phone": "+62 812 3456 7890",
                "tags": "VIP, Retail, VIP",
                "tax_exempt": True,
                "email_marketing_consent": {"state": "subscribed"},
                "default_address": {"id": 9},
                "addresses": [
                    {"id": 9, "address1": "Main Street", "country_code": "id"}
                ],
            }
        )
        assert customer["id"] == "gid://shopify/Customer/42"
        assert customer["email"] == "alice@example.com"
        assert customer["marketing_state"] == "SUBSCRIBED"
        assert customer["tags"] == ["Retail", "VIP"]
        assert customer["addresses"][0]["id"] == "gid://shopify/MailingAddress/9"
        assert customer["addresses"][0]["is_default"] is True

    def test_address_diff_is_idempotent_and_reports_changes(self):
        existing = [
            {
                "id": "address-1",
                "address1": "Old",
                "city": "Jakarta",
                "is_default": True,
            },
            {"id": "address-stale", "address1": "Remove"},
        ]
        incoming = [
            {
                "id": "address-1",
                "address1": "New",
                "city": "Jakarta",
                "is_default": True,
            },
            {"id": "address-2", "address1": "Create"},
        ]
        diff = diff_customer_addresses(existing, incoming)
        assert len(diff["create"]) == 1
        assert len(diff["update"]) == 1
        assert len(diff["delete"]) == 1
        assert diff_customer_addresses(incoming, incoming) == {
            "create": [],
            "update": [],
            "delete": [],
        }

    def test_customer_without_id_is_rejected(self):
        with self.assertRaises(ShopifyCustomerPayloadError):
            normalize_customer_payload({"email": "missing@example.com"})
