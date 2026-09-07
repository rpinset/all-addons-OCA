# pylint: disable=consider-merging-classes-inherited

from datetime import datetime, timezone

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command

from ..graphql.customer import (
    CATALOGS_QUERY,
    COMPANIES_QUERY,
    CUSTOMER_BY_ID_QUERY,
    CUSTOMER_UPDATE_MUTATION,
    CUSTOMERS_BULK_QUERY,
    PRICE_LIST_PRICES_QUERY,
)
from ..lib.bulk import ShopifyBulkRunner
from ..lib.client import ShopifyUserError
from ..lib.customer import (
    normalize_bulk_customers,
    normalize_customer_payload,
    normalize_email,
    normalize_phone,
    phone_search_suffix,
)
from .webhook_event import WEBHOOK_HANDLERS

PHONE_MATCH_CANDIDATE_LIMIT = 200


def _utc_datetime(value):
    if not value:
        return False
    parsed = (
        value
        if isinstance(value, datetime)
        else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    )
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


class ShopifyInstanceCustomerSync(models.Model):
    _inherit = "shopify.instance"

    @api.model
    def _cron_reconcile_customers(self):
        for instance in self.search(
            [("active", "=", True), ("state", "=", "connected")]
        ):
            instance.with_delay(
                description=self.env._(
                    "Reconcile Shopify customers for %s", instance.name
                ),
                identity_key=(f"shopify.customers.reconcile.{instance.id}"),
            )._job_fetch_customers_bulk()
            instance._write_log(
                entity="drift_customers",
                direction="import",
                level="info",
                message=self.env._("Weekly customer drift reconciliation queued."),
                record=instance,
            )

    def action_import_customers(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        self.with_delay(
            description=self.env._("Import Shopify customers for %s", self.name),
            identity_key=f"shopify.customers.bulk.{self.id}",
        )._job_fetch_customers_bulk()
        return self._customer_notification(
            self.env._("Customer import queued"),
            self.env._("Shopify customers will be imported in the background."),
        )

    def _job_fetch_customers_bulk(self):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return 0
        records = ShopifyBulkRunner(self._shopify_client()).run(CUSTOMERS_BULK_QUERY)
        customers = normalize_bulk_customers(records)
        for customer in customers:
            self.env["shopify.customer"].with_delay(
                description=self.env._("Import Shopify customer %s", customer["id"]),
                identity_key=(f"shopify.customer.import.{self.id}.{customer['id']}"),
            )._job_import_customer(
                self.id,
                customer,
                payload_normalized=True,
                complete_snapshot=True,
            )
        self._write_log(
            entity="customer",
            direction="import",
            level="info",
            message=self.env._(
                "%s Shopify customers queued for import.", len(customers)
            ),
            record=self,
        )
        return len(customers)

    def action_import_b2b(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        if not self.b2b_import_enabled:
            raise UserError(self.env._("Enable Shopify B2B import first."))
        self.with_delay(
            description=self.env._("Import Shopify B2B data for %s", self.name),
            identity_key=f"shopify.b2b.import.{self.id}",
        )._job_import_b2b()
        return self._customer_notification(
            self.env._("B2B import queued"),
            self.env._(
                "Shopify companies and catalogs will be checked in the background."
            ),
        )

    def _job_import_b2b(self):
        self = self.sudo()
        self.ensure_one()
        if not self.active or not self.b2b_import_enabled:
            return 0
        client = self._shopify_client()
        after = None
        company_count = 0
        try:
            while True:
                data = client.execute(COMPANIES_QUERY, {"after": after})
                connection = data.get("companies") or {}
                self.shopify_plus_state = "available"
                for payload in connection.get("nodes") or []:
                    self.env["shopify.company"]._import_company(self, payload)
                    company_count += 1
                page_info = connection.get("pageInfo") or {}
                if not page_info.get("hasNextPage"):
                    break
                after = page_info.get("endCursor")
                if not after:
                    raise UserError(
                        self.env._("Shopify returned an invalid company page cursor.")
                    )
        except ShopifyUserError:
            self.write(
                {
                    "shopify_plus_state": "unavailable",
                    "b2b_import_enabled": False,
                }
            )
            self._write_log(
                entity="company",
                direction="import",
                level="info",
                message=self.env._(
                    "Shopify B2B is unavailable for this shop; import disabled."
                ),
                record=self,
            )
            return 0
        catalog_count = self._import_catalogs(client)
        self._write_log(
            entity="company",
            direction="import",
            level="info",
            message=self.env._(
                "Imported %(companies)s B2B companies and %(catalogs)s catalogs.",
                companies=company_count,
                catalogs=catalog_count,
            ),
            record=self,
        )
        return company_count + catalog_count

    def _import_catalogs(self, client):
        after = None
        count = 0
        while True:
            data = client.execute(CATALOGS_QUERY, {"after": after})
            connection = data.get("catalogs") or {}
            for payload in connection.get("nodes") or []:
                if payload.get("priceList"):
                    self._complete_catalog_prices(client, payload)
                    self.env["shopify.catalog"]._import_catalog(self, payload)
                    count += 1
            page_info = connection.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            if not after:
                raise UserError(
                    self.env._("Shopify returned an invalid catalog page cursor.")
                )
        return count

    def _complete_catalog_prices(self, client, catalog):
        price_list = catalog["priceList"]
        prices = price_list.get("prices") or {}
        nodes = list(prices.get("nodes") or [])
        page_info = prices.get("pageInfo") or {}
        after = page_info.get("endCursor")
        while page_info.get("hasNextPage"):
            if not after:
                raise UserError(
                    self.env._("Shopify returned an invalid price-list page cursor.")
                )
            data = client.execute(
                PRICE_LIST_PRICES_QUERY,
                {"id": price_list["id"], "after": after},
            )
            page = (data.get("priceList") or {}).get("prices") or {}
            nodes.extend(page.get("nodes") or [])
            page_info = page.get("pageInfo") or {}
            after = page_info.get("endCursor")
        price_list["prices"] = {"nodes": nodes, "pageInfo": page_info}

    def _customer_notification(self, title, message):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": "success",
                "sticky": False,
            },
        }


class ShopifyCustomerSync(models.Model):
    _inherit = "shopify.customer"

    @api.model
    def _job_import_customer(
        self,
        instance_id,
        payload,
        *,
        payload_normalized=False,
        complete_snapshot=True,
    ):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        customer = (
            payload if payload_normalized else normalize_customer_payload(payload)
        )
        self.env.cr.execute(
            "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
            (instance.id, customer["id"]),
        )
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", customer["id"]),
            ],
            limit=1,
        )
        is_new_partner = False
        if binding:
            partner = binding.odoo_id
        else:
            company_contact = self.env["shopify.company.contact"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("customer_shopify_id", "=", customer["id"]),
                ],
                limit=1,
            )
            partner = company_contact.odoo_id or self._match_partner(instance, customer)
            if not partner:
                partner = (
                    self.env["res.partner"]
                    .with_context(shopify_customer_import=True)
                    .create(self._new_partner_values(instance, customer))
                )
                is_new_partner = True
            binding = self.create(
                {
                    "instance_id": instance.id,
                    "shopify_id": customer["id"],
                    "odoo_id": partner.id,
                }
            )
        try:
            with self.env.cr.savepoint():
                self._apply_customer(
                    binding,
                    customer,
                    seed_all=is_new_partner,
                    complete_snapshot=complete_snapshot,
                )
        except Exception as exc:
            binding.write({"state": "error", "error_message": str(exc)})
            instance._write_log(
                entity="customer",
                direction="import",
                level="error",
                message=self.env._("Customer import failed: %s", exc),
                record=binding,
            )
            return False
        binding.write(
            {
                "email_marketing_state": customer["marketing_state"],
                "tags": ", ".join(customer["tags"]),
                "tax_exempt": customer["tax_exempt"],
                "external_updated_at": _utc_datetime(customer["updated_at"]),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        instance._write_log(
            entity="customer",
            direction="import",
            level="info",
            message=self.env._("Imported Shopify customer %s.", customer["id"]),
            record=binding,
        )
        return binding.id

    @api.model
    def _job_import_customer_from_api(self, instance_id, customer_id):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        data = instance._shopify_client().execute(
            CUSTOMER_BY_ID_QUERY, {"id": customer_id}
        )
        customer = data.get("customer")
        if not customer:
            return False
        return self._job_import_customer(instance.id, customer)

    def _match_partner(self, instance, customer):
        partner_model = self.env["res.partner"].with_context(active_test=False)
        domain = [
            ("parent_id", "=", False),
            "|",
            ("company_id", "=", False),
            ("company_id", "=", instance.company_id.id),
        ]
        email = normalize_email(customer["email"])
        if email:
            candidates = partner_model.search([("email", "ilike", email), *domain])
            for candidate in candidates:
                if normalize_email(candidate.email) == email and not self.search(
                    [
                        ("instance_id", "=", instance.id),
                        ("odoo_id", "=", candidate.id),
                    ],
                    limit=1,
                ):
                    return candidate
        phone = normalize_phone(
            customer["phone"], instance.company_id.country_id.phone_code
        )
        suffix = phone_search_suffix(phone)
        if phone and suffix:
            phone_fields = [
                field_name
                for field_name in ("phone", "mobile")
                if field_name in partner_model._fields
            ]
            phone_domain = [
                (field_name, "ilike", suffix) for field_name in phone_fields
            ]
            if len(phone_domain) > 1:
                phone_domain.insert(0, "|")
            candidates = partner_model.search(
                [
                    *domain,
                    *phone_domain,
                ],
                limit=PHONE_MATCH_CANDIDATE_LIMIT,
            )
            for candidate in candidates:
                candidate_phones = {
                    normalize_phone(
                        candidate[field_name],
                        instance.company_id.country_id.phone_code,
                    )
                    for field_name in phone_fields
                }
                if phone in candidate_phones and not self.search(
                    [
                        ("instance_id", "=", instance.id),
                        ("odoo_id", "=", candidate.id),
                    ],
                    limit=1,
                ):
                    return candidate
        return partner_model

    def _new_partner_values(self, instance, customer):
        return {
            "name": customer["name"]
            or customer["email"]
            or customer["phone"]
            or self.env._("Shopify Customer"),
            "email": customer["email"] or False,
            "phone": customer["phone"] or False,
            "is_company": False,
            "company_id": instance.company_id.id,
            "customer_rank": 1,
        }

    def _apply_customer(self, binding, customer, *, seed_all, complete_snapshot):
        instance = binding.instance_id
        owners = instance._customer_field_owners()
        values = {"is_company": False, "customer_rank": 1}
        if seed_all or owners["customer_name"] == "shopify":
            values["name"] = (
                customer["name"]
                or customer["email"]
                or customer["phone"]
                or self.env._("Shopify Customer")
            )
        if seed_all or owners["customer_email"] == "shopify":
            values["email"] = customer["email"] or False
        if seed_all or owners["customer_phone"] == "shopify":
            values["phone"] = customer["phone"] or False
        binding.odoo_id.with_context(shopify_customer_import=True).write(values)
        self._sync_tags(binding, customer["tags"])
        if seed_all or owners["customer_addresses"] == "shopify":
            self._sync_addresses(
                binding,
                customer["addresses"],
                complete_snapshot=complete_snapshot,
            )

    def _sync_tags(self, binding, tags):
        categories = self.env["res.partner.category"]
        for tag in tags:
            category = categories.search(
                [
                    ("name", "=", tag),
                    (
                        "shopify_company_id",
                        "=",
                        binding.instance_id.company_id.id,
                    ),
                ],
                limit=1,
            )
            if not category:
                category = categories.create(
                    {
                        "name": tag,
                        "shopify_company_id": (binding.instance_id.company_id.id),
                    }
                )
            categories |= category
        preserved = binding.odoo_id.category_id - binding.tag_category_ids
        binding.odoo_id.with_context(shopify_customer_import=True).write(
            {"category_id": [Command.set((preserved | categories).ids)]}
        )
        binding.tag_category_ids = [Command.set(categories.ids)]

    def _sync_addresses(self, binding, addresses, *, complete_snapshot=True):
        imported_ids = set()
        for address in addresses:
            if not address["id"]:
                continue
            imported_ids.add(address["id"])
            address_binding = self.env["shopify.customer.address"].search(
                [
                    ("instance_id", "=", binding.instance_id.id),
                    ("shopify_id", "=", address["id"]),
                ],
                limit=1,
            )
            values = self._address_partner_values(binding, address)
            if address_binding:
                address_binding.odoo_id.with_context(
                    shopify_customer_import=True
                ).write(values)
                address_binding.write(
                    {
                        "is_default": address["is_default"],
                        "last_sync_date": fields.Datetime.now(),
                        "state": "synced",
                    }
                )
            else:
                partner = self._match_unbound_address(binding, address)
                if partner:
                    partner.with_context(shopify_customer_import=True).write(values)
                else:
                    partner = (
                        self.env["res.partner"]
                        .with_context(shopify_customer_import=True)
                        .create(values)
                    )
                self.env["shopify.customer.address"].create(
                    {
                        "instance_id": binding.instance_id.id,
                        "shopify_id": address["id"],
                        "customer_binding_id": binding.id,
                        "odoo_id": partner.id,
                        "is_default": address["is_default"],
                        "last_sync_date": fields.Datetime.now(),
                        "state": "synced",
                    }
                )
        if complete_snapshot:
            stale = binding.address_binding_ids.filtered(
                lambda item: item.shopify_id not in imported_ids
            )
            stale.mapped("odoo_id").with_context(shopify_customer_import=True).unlink()

    def _match_unbound_address(self, binding, address):
        if not any(address[field] for field in ("address1", "city", "zip")):
            return self.env["res.partner"]
        bound_partner_ids = binding.address_binding_ids.odoo_id.ids
        candidates = binding.odoo_id.child_ids.filtered(
            lambda partner: (
                partner.id not in bound_partner_ids
                and partner.type in ("delivery", "invoice")
            )
        )
        country_code = address["country"].casefold()
        for partner in candidates:
            if (
                (partner.street or "").strip().casefold()
                == address["address1"].strip().casefold()
                and (partner.city or "").strip().casefold()
                == address["city"].strip().casefold()
                and (partner.zip or "").strip().casefold()
                == address["zip"].strip().casefold()
                and (partner.country_id.code or "").casefold() == country_code
            ):
                return partner
        return self.env["res.partner"]

    def _address_partner_values(self, binding, address):
        country = self.env["res.country"]
        if address["country"]:
            country = country.search([("code", "=", address["country"])], limit=1)
        state = self.env["res.country.state"]
        if country and address["province"]:
            state = state.search(
                [
                    ("country_id", "=", country.id),
                    "|",
                    ("code", "=ilike", address["province"]),
                    ("name", "=ilike", address["province"]),
                ],
                limit=1,
            )
        name = " ".join(
            part for part in (address["first_name"], address["last_name"]) if part
        )
        return {
            "parent_id": binding.odoo_id.id,
            "company_id": binding.instance_id.company_id.id,
            "type": "invoice" if address["is_default"] else "delivery",
            "name": name or address["company"] or binding.odoo_id.name,
            "street": address["address1"] or False,
            "street2": address["address2"] or False,
            "city": address["city"] or False,
            "state_id": state.id or False,
            "country_id": country.id or False,
            "zip": address["zip"] or False,
            "phone": address["phone"] or False,
        }

    def _enqueue_customer_export(self):
        for binding in self:
            instance = binding.instance_id
            if not instance.active or not instance.customer_export_enabled:
                continue
            binding.with_delay(
                description=self.env._(
                    "Export Shopify customer %s", binding.odoo_id.display_name
                ),
                identity_key=(f"shopify.customer.export.{instance.id}.{binding.id}"),
            )._job_export_customer()

    def _job_export_customer(self):
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active or not self.instance_id.customer_export_enabled:
            return False
        values = {"id": self.shopify_id}
        owners = self.instance_id._customer_field_owners()
        partner = self.odoo_id
        if owners["customer_name"] == "odoo":
            names = (partner.name or "").strip().rsplit(" ", 1)
            values["firstName"] = names[0] if names else ""
            values["lastName"] = names[1] if len(names) > 1 else ""
        if owners["customer_email"] == "odoo":
            values["email"] = partner.email or None
        if owners["customer_phone"] == "odoo":
            values["phone"] = partner.phone or partner.mobile or None
        if owners["customer_addresses"] == "odoo":
            values["addresses"] = [
                self._export_address_values(child)
                for child in partner.child_ids.filtered(
                    lambda item: item.type in ("delivery", "invoice")
                )
            ]
        if len(values) == 1:
            return False
        try:
            self.instance_id._shopify_client().execute(
                CUSTOMER_UPDATE_MUTATION, {"input": values}
            )
        except Exception as exc:
            self.write({"state": "error", "error_message": str(exc)})
            self.instance_id._write_log(
                entity="customer",
                direction="export",
                level="error",
                message=self.env._("Customer export failed: %s", exc),
                record=self,
            )
            raise
        self.write(
            {
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        self.instance_id._write_log(
            entity="customer",
            direction="export",
            level="info",
            message=self.env._("Exported Shopify customer %s.", self.shopify_id),
            record=self,
        )
        return True

    def _export_address_values(self, partner):
        binding = self.address_binding_ids.filtered(
            lambda item: item.odoo_id == partner
        )[:1]
        names = (partner.name or "").strip().rsplit(" ", 1)
        values = {
            "firstName": names[0] if names else "",
            "lastName": names[1] if len(names) > 1 else "",
            "address1": partner.street or "",
            "address2": partner.street2 or "",
            "city": partner.city or "",
            "provinceCode": partner.state_id.code or "",
            "countryCode": partner.country_id.code or "",
            "zip": partner.zip or "",
            "phone": partner.phone or "",
        }
        if binding:
            values["id"] = binding.shopify_id
        return values


class ShopifyCompanySync(models.Model):
    _inherit = "shopify.company"

    @api.model
    def _import_company(self, instance, payload):
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", payload["id"]),
            ],
            limit=1,
        )
        if binding:
            partner = binding.odoo_id
        else:
            partner = self.env["res.partner"].create(
                {
                    "name": payload.get("name") or self.env._("Shopify Company"),
                    "is_company": True,
                    "company_id": instance.company_id.id,
                    "customer_rank": 1,
                }
            )
            binding = self.create(
                {
                    "instance_id": instance.id,
                    "shopify_id": payload["id"],
                    "odoo_id": partner.id,
                }
            )
        partner.with_context(shopify_customer_import=True).write(
            {
                "name": payload.get("name") or partner.name,
                "is_company": True,
                "customer_rank": 1,
            }
        )
        binding.write(
            {
                "external_id": payload.get("externalId") or False,
                "external_updated_at": _utc_datetime(payload.get("updatedAt")),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        self._sync_company_locations(binding, payload.get("locations") or {})
        self._sync_company_contacts(binding, payload)
        return binding

    def _sync_company_locations(self, binding, connection):
        for payload in connection.get("nodes") or []:
            location = self.env["shopify.company.location"].search(
                [
                    ("instance_id", "=", binding.instance_id.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            )
            shipping = payload.get("shippingAddress") or {}
            billing = payload.get("billingAddress") or {}
            values = {
                "parent_id": binding.odoo_id.id,
                "company_id": binding.instance_id.company_id.id,
                "type": "delivery",
                "name": payload.get("name") or binding.odoo_id.name,
                "phone": payload.get("phone") or False,
                **self._company_address_values(shipping or billing),
            }
            if location:
                location.odoo_id.with_context(shopify_customer_import=True).write(
                    values
                )
            else:
                partner = (
                    self.env["res.partner"]
                    .with_context(shopify_customer_import=True)
                    .create(values)
                )
                location = self.env["shopify.company.location"].create(
                    {
                        "instance_id": binding.instance_id.id,
                        "shopify_id": payload["id"],
                        "company_binding_id": binding.id,
                        "odoo_id": partner.id,
                    }
                )
            if billing:
                billing_values = {
                    "parent_id": binding.odoo_id.id,
                    "company_id": binding.instance_id.company_id.id,
                    "type": "invoice",
                    "name": self.env._(
                        "%s Billing", (payload.get("name") or binding.odoo_id.name)
                    ),
                    "phone": payload.get("phone") or False,
                    **self._company_address_values(billing),
                }
                if location.billing_odoo_id:
                    location.billing_odoo_id.with_context(
                        shopify_customer_import=True
                    ).write(billing_values)
                else:
                    location.billing_odoo_id = (
                        self.env["res.partner"]
                        .with_context(shopify_customer_import=True)
                        .create(billing_values)
                    )
            location.write(
                {
                    "last_sync_date": fields.Datetime.now(),
                    "state": "synced",
                }
            )

    def _company_address_values(self, address):
        country = self.env["res.country"]
        country_code = address.get("countryCode")
        if country_code:
            country = country.search([("code", "=", country_code)], limit=1)
        state = self.env["res.country.state"]
        province = address.get("province")
        if country and province:
            state = state.search(
                [
                    ("country_id", "=", country.id),
                    "|",
                    ("code", "=ilike", province),
                    ("name", "=ilike", province),
                ],
                limit=1,
            )
        return {
            "street": address.get("address1") or False,
            "street2": address.get("address2") or False,
            "city": address.get("city") or False,
            "state_id": state.id or False,
            "country_id": country.id or False,
            "zip": address.get("zip") or False,
        }

    def _sync_company_contacts(self, binding, company_payload):
        roles_by_contact = {}
        for location in (company_payload.get("locations") or {}).get("nodes") or []:
            for assignment in (location.get("roleAssignments") or {}).get(
                "nodes"
            ) or []:
                contact = assignment.get("contact") or {}
                role = assignment.get("role") or {}
                if contact.get("id") and role.get("name"):
                    roles_by_contact.setdefault(contact["id"], set()).add(role["name"])
        for payload in (company_payload.get("contacts") or {}).get("nodes") or []:
            customer = payload.get("customer") or {}
            contact_binding = self.env["shopify.company.contact"].search(
                [
                    ("instance_id", "=", binding.instance_id.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            )
            partner = contact_binding.odoo_id if contact_binding else False
            if not partner and customer.get("id"):
                customer_binding = self.env["shopify.customer"].search(
                    [
                        ("instance_id", "=", binding.instance_id.id),
                        ("shopify_id", "=", customer["id"]),
                    ],
                    limit=1,
                )
                partner = customer_binding.odoo_id
            values = {
                "parent_id": binding.odoo_id.id,
                "company_id": binding.instance_id.company_id.id,
                "type": "contact",
                "is_company": False,
                "name": customer.get("displayName")
                or customer.get("email")
                or self.env._("Shopify Company Contact"),
                "email": customer.get("email") or False,
                "phone": customer.get("phone") or False,
            }
            if partner:
                partner.with_context(shopify_customer_import=True).write(values)
            else:
                partner = (
                    self.env["res.partner"]
                    .with_context(shopify_customer_import=True)
                    .create(values)
                )
            binding_values = {
                "company_binding_id": binding.id,
                "odoo_id": partner.id,
                "customer_shopify_id": customer.get("id") or False,
                "title": payload.get("title") or False,
                "roles": ", ".join(sorted(roles_by_contact.get(payload["id"], set()))),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
            }
            if contact_binding:
                contact_binding.write(binding_values)
            else:
                self.env["shopify.company.contact"].create(
                    {
                        **binding_values,
                        "instance_id": binding.instance_id.id,
                        "shopify_id": payload["id"],
                    }
                )


class ShopifyCatalogSync(models.Model):
    _inherit = "shopify.catalog"

    @api.model
    def _import_catalog(self, instance, payload):
        price_list = payload["priceList"]
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", payload["id"]),
            ],
            limit=1,
        )
        currency = (
            self.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", price_list["currency"])], limit=1)
        )
        if not currency:
            instance._write_log(
                entity="catalog",
                direction="import",
                level="error",
                message=self.env._(
                    "Unsupported catalog currency %s.", price_list["currency"]
                ),
            )
            return False
        if binding:
            pricelist = binding.odoo_pricelist_id
            pricelist.write(
                {
                    "name": price_list.get("name") or payload["title"],
                    "currency_id": currency.id,
                }
            )
        else:
            pricelist = self.env["product.pricelist"].create(
                {
                    "name": price_list.get("name") or payload["title"],
                    "currency_id": currency.id,
                    "company_id": instance.company_id.id,
                }
            )
            binding = self.create(
                {
                    "instance_id": instance.id,
                    "shopify_id": payload["id"],
                    "title": payload["title"],
                    "price_list_shopify_id": price_list["id"],
                    "odoo_pricelist_id": pricelist.id,
                }
            )
        retained_items = self.env["product.pricelist.item"]
        for price in (price_list.get("prices") or {}).get("nodes") or []:
            variant_id = (price.get("variant") or {}).get("id")
            amount = (price.get("price") or {}).get("amount")
            variant = self.env["shopify.product.variant"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "=", variant_id),
                    ("state", "=", "synced"),
                    ("template_binding_id.remote_deleted", "=", False),
                ],
                limit=1,
            )
            if not variant or amount is None:
                continue
            item = self.env["product.pricelist.item"].search(
                [
                    ("pricelist_id", "=", pricelist.id),
                    ("product_id", "=", variant.odoo_id.id),
                    ("applied_on", "=", "0_product_variant"),
                ],
                limit=1,
            )
            values = {
                "pricelist_id": pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": variant.odoo_id.id,
                "compute_price": "fixed",
                "fixed_price": amount,
                "min_quantity": 0,
            }
            if item:
                item.write(values)
            else:
                item = self.env["product.pricelist.item"].create(values)
            retained_items |= item
        stale = pricelist.item_ids.filtered(
            lambda item: (
                item.applied_on == "0_product_variant" and item not in retained_items
            )
        )
        stale.unlink()
        binding.write(
            {
                "title": payload["title"],
                "status": payload.get("status") or False,
                "price_list_shopify_id": price_list["id"],
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
        )
        return binding


class ShopifyWebhookCustomerHandlers(models.Model):
    _inherit = "shopify.webhook.event"

    def _handle_customer_upsert(self):
        self.ensure_one()
        customer = normalize_customer_payload(self.payload)
        self.env["shopify.customer"].with_delay(
            description=self.env._(
                "Import Shopify customer webhook %s", customer["id"]
            ),
            identity_key=(
                f"shopify.customer.import.{self.instance_id.id}.{customer['id']}"
            ),
        )._job_import_customer_from_api(self.instance_id.id, customer["id"])


WEBHOOK_HANDLERS.update(
    {
        "customers/create": "_handle_customer_upsert",
        "customers/update": "_handle_customer_upsert",
    }
)


class ResPartnerShopifyCustomer(models.Model):
    _inherit = "res.partner"

    shopify_customer_binding_ids = fields.One2many(
        "shopify.customer",
        "odoo_id",
        string="Shopify Customer Bindings",
    )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        if self.env.context.get("shopify_customer_import"):
            return partners
        for partner in partners.filtered("parent_id"):
            for binding in partner.parent_id.sudo().shopify_customer_binding_ids:
                if binding.instance_id._is_customer_field_owned_by(
                    "customer_addresses", "odoo"
                ):
                    binding._enqueue_customer_export()
        return partners

    def write(self, values):
        result = super().write(values)
        if self.env.context.get("shopify_customer_import"):
            return result
        customer_fields = {
            "name": "customer_name",
            "email": "customer_email",
            "phone": "customer_phone",
            "mobile": "customer_phone",
            "street": "customer_addresses",
            "street2": "customer_addresses",
            "city": "customer_addresses",
            "state_id": "customer_addresses",
            "country_id": "customer_addresses",
            "zip": "customer_addresses",
            "parent_id": "customer_addresses",
            "type": "customer_addresses",
        }
        changed = {
            owner_field
            for partner_field, owner_field in customer_fields.items()
            if partner_field in values
        }
        if not changed:
            return result
        for partner in self:
            partner_changed = changed
            if (
                partner.parent_id
                and {
                    "name",
                    "email",
                    "phone",
                    "mobile",
                    "street",
                    "street2",
                    "city",
                    "state_id",
                    "country_id",
                    "zip",
                    "parent_id",
                    "type",
                }
                & values.keys()
            ):
                partner_changed = {"customer_addresses"}
            bindings = partner.sudo().shopify_customer_binding_ids
            bindings |= (
                partner.parent_id.sudo().shopify_customer_binding_ids
                if partner.parent_id
                else self.env["shopify.customer"]
            )
            address_bindings = (
                self.env["shopify.customer.address"]
                .sudo()
                .search([("odoo_id", "=", partner.id)])
            )
            bindings |= address_bindings.mapped("customer_binding_id")
            for binding in bindings:
                owners = binding.instance_id._customer_field_owners()
                if any(owners[field] == "odoo" for field in partner_changed):
                    binding._enqueue_customer_export()
        return result

    def unlink(self):
        if self.env.context.get("shopify_customer_import"):
            return super().unlink()
        bindings = self.env["shopify.customer"]
        for partner in self.filtered("parent_id"):
            bindings |= partner.parent_id.sudo().shopify_customer_binding_ids
        result = super().unlink()
        for binding in bindings.exists():
            if binding.instance_id._is_customer_field_owned_by(
                "customer_addresses", "odoo"
            ):
                binding._enqueue_customer_export()
        return result
