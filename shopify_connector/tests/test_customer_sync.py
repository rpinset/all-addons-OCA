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

    def test_failed_first_import_still_seeds_the_new_partner_on_retry(self):
        mapping = self.instance.field_mapping_ids.filtered(
            lambda item: item.field == "customer_addresses"
        )
        if mapping:
            mapping.owner = "odoo"
        else:
            self.env["shopify.field.mapping"].create(
                {
                    "instance_id": self.instance.id,
                    "field": "customer_addresses",
                    "owner": "odoo",
                }
            )
        payload = self._payload(
            5,
            addressesV2={
                "nodes": [
                    {
                        "id": "gid://shopify/MailingAddress/50",
                        "firstName": "Seed",
                        "lastName": "Address",
                        "address1": "Seed Street",
                        "city": "Jakarta",
                        "countryCodeV2": "ID",
                    }
                ]
            },
        )
        customer_class = type(self.customer_model)
        sync_tags = customer_class._sync_tags

        # The first import creates the partner, then fails before seeding.
        with patch.object(
            customer_class, "_sync_tags", side_effect=ValueError("Tag failure")
        ):
            self.assertFalse(
                self.customer_model._job_import_customer(self.instance.id, payload)
            )
        binding = self.customer_model.search(
            [("shopify_id", "=", "gid://shopify/Customer/5")]
        )
        self.assertEqual(binding.state, "error")
        self.assertTrue(binding.initial_seed_pending)

        with patch.object(customer_class, "_sync_tags", sync_tags):
            self.customer_model._job_import_customer(self.instance.id, payload)

        # Odoo owns addresses, yet the new partner gets them once from Shopify.
        self.assertEqual(binding.state, "synced")
        self.assertFalse(binding.initial_seed_pending)
        self.assertEqual(binding.address_binding_ids.odoo_id.street, "Seed Street")

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

    def test_removed_address_used_by_an_order_is_archived(self):
        def address(address_id, street):
            return {
                "id": f"gid://shopify/MailingAddress/{address_id}",
                "firstName": "Alice",
                "lastName": "Address",
                "address1": street,
                "city": "Jakarta",
                "countryCodeV2": "ID",
            }

        payload = self._payload(
            5,
            defaultAddress={"id": "gid://shopify/MailingAddress/50"},
            addressesV2={
                "nodes": [address(50, "First Street"), address(51, "Old Street")]
            },
        )
        binding_id = self.customer_model._job_import_customer(self.instance.id, payload)
        binding = self.customer_model.browse(binding_id)
        old_address = binding.address_binding_ids.filtered(
            lambda item: item.shopify_id.endswith("/51")
        ).odoo_id
        self.env["sale.order"].create(
            {
                "partner_id": binding.odoo_id.id,
                "partner_shipping_id": old_address.id,
            }
        )

        payload["addressesV2"] = {"nodes": [address(50, "First Street")]}
        payload["lastName"] = "Renamed"
        self.customer_model._job_import_customer(self.instance.id, payload)

        self.assertEqual(binding.state, "synced", binding.error_message)
        self.assertEqual(binding.odoo_id.name, "Shopify Renamed")
        self.assertEqual(len(binding.address_binding_ids), 1)
        self.assertFalse(old_address.active)

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

    def test_company_contact_roles_come_from_location_role_assignments(self):
        contact_id = "gid://shopify/CompanyContact/1"
        assignment_id = "gid://shopify/CompanyContactRoleAssignment/1"
        binding = self.env["shopify.company"]._import_company(
            self.instance,
            {
                "id": "gid://shopify/Company/1",
                "name": "Acme Wholesale",
                "locations": {
                    "nodes": [
                        {
                            "id": "gid://shopify/CompanyLocation/1",
                            "name": "Acme HQ",
                            "roleAssignments": {
                                "nodes": [
                                    {
                                        "id": assignment_id,
                                        "role": {
                                            "id": "gid://shopify/CompanyContactRole/1",
                                            "name": "Ordering only",
                                        },
                                        "companyContact": {"id": contact_id},
                                    }
                                ]
                            },
                        }
                    ]
                },
                "contacts": {
                    "nodes": [
                        {
                            "id": contact_id,
                            "title": "Buyer",
                            "customer": {
                                "id": "gid://shopify/Customer/900",
                                "displayName": "Jane Buyer",
                                "email": "jane.buyer@example.com",
                                "phone": "",
                            },
                        }
                    ]
                },
            },
        )

        self.assertEqual(binding.contact_binding_ids.roles, "Ordering only")
