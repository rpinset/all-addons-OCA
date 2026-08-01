from unittest.mock import patch

from odoo.tests.common import TransactionCase

from ..models.customer_sync import PHONE_MATCH_CANDIDATE_LIMIT


class TestShopifyCustomerSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Customer Shop",
                "shop_url": "customer-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.customer_model = cls.env["shopify.customer"]

    def _payload(self, customer_id, **values):
        payload = {
            "id": f"gid://shopify/Customer/{customer_id}",
            "firstName": "Shopify",
            "lastName": "Customer",
            "email": f"customer-{customer_id}@example.com",
            "phone": "",
            "tags": [],
            "taxExempt": False,
            "addressesV2": {"nodes": []},
        }
        payload.update(values)
        return payload

    def test_first_link_deduplicates_by_normalized_email(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Existing Email",
                "email": "  MATCH@Example.COM ",
                "company_id": False,
            }
        )

        binding_id = self.customer_model._job_import_customer(
            self.instance.id,
            self._payload(1, email="match@example.com"),
        )

        self.assertEqual(self.customer_model.browse(binding_id).odoo_id, partner)

    def test_first_link_falls_back_to_normalized_phone(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Existing Phone",
                "phone": "+62 (812) 3456-7890",
                "company_id": False,
            }
        )

        binding_id = self.customer_model._job_import_customer(
            self.instance.id,
            self._payload(
                2,
                email="",
                phone="+6281234567890",
            ),
        )

        self.assertEqual(self.customer_model.browse(binding_id).odoo_id, partner)

    def test_phone_fallback_uses_filtered_bounded_partner_search(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Bounded Phone Candidate",
                "phone": "+62 811 2222-7890",
                "company_id": False,
            }
        )
        partner_model_class = type(self.env["res.partner"])
        original_search = partner_model_class.search
        calls = []

        def tracked_search(recordset, domain, *args, **kwargs):
            calls.append((domain, kwargs.get("limit")))
            return original_search(recordset, domain, *args, **kwargs)

        with patch.object(
            partner_model_class,
            "search",
            autospec=True,
            side_effect=tracked_search,
        ):
            binding_id = self.customer_model._job_import_customer(
                self.instance.id,
                self._payload(
                    20,
                    email="",
                    phone="+6281122227890",
                ),
            )

        phone_calls = [
            (domain, limit)
            for domain, limit in calls
            if ("phone", "ilike", "7890") in domain
        ]
        self.assertEqual(len(phone_calls), 1)
        self.assertEqual(phone_calls[0][1], PHONE_MATCH_CANDIDATE_LIMIT)
        self.assertEqual(self.customer_model.browse(binding_id).odoo_id, partner)

    def test_first_link_creates_partner_when_no_match_exists(self):
        before = self.env["res.partner"].search_count([])

        binding_id = self.customer_model._job_import_customer(
            self.instance.id, self._payload(3)
        )

        binding = self.customer_model.browse(binding_id)
        self.assertEqual(self.env["res.partner"].search_count([]), before + 1)
        self.assertEqual(binding.odoo_id.company_id, self.instance.company_id)
        self.assertFalse(binding.odoo_id.is_company)

    def test_address_import_is_idempotent_by_shopify_address_id(self):
        payload = self._payload(
            4,
            defaultAddress={"id": "gid://shopify/MailingAddress/40"},
            addressesV2={
                "nodes": [
                    {
                        "id": "gid://shopify/MailingAddress/40",
                        "firstName": "Alice",
                        "lastName": "Address",
                        "address1": "First Street",
                        "city": "Jakarta",
                        "countryCodeV2": "ID",
                    }
                ]
            },
        )

        binding_id = self.customer_model._job_import_customer(self.instance.id, payload)
        self.customer_model._job_import_customer(self.instance.id, payload)

        binding = self.customer_model.browse(binding_id)
        self.assertEqual(len(binding.address_binding_ids), 1)
        self.assertEqual(binding.address_binding_ids.odoo_id.street, "First Street")
        self.assertEqual(binding.address_binding_ids.odoo_id.type, "invoice")

    def test_tags_create_company_scoped_categories_without_duplicates(self):
        payload = self._payload(5, tags=["VIP", "Wholesale"])

        binding_id = self.customer_model._job_import_customer(self.instance.id, payload)
        self.customer_model._job_import_customer(self.instance.id, payload)

        binding = self.customer_model.browse(binding_id)
        self.assertEqual(
            set(binding.tag_category_ids.mapped("name")),
            {"VIP", "Wholesale"},
        )
        self.assertEqual(
            self.env["res.partner.category"].search_count(
                [
                    ("name", "in", ["VIP", "Wholesale"]),
                    (
                        "shopify_company_id",
                        "=",
                        self.instance.company_id.id,
                    ),
                ]
            ),
            2,
        )
