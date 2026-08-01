# pylint: disable=consider-merging-classes-inherited

import base64
import hashlib
from datetime import datetime, timezone
from decimal import Decimal

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command

from ..graphql.product import (
    COLLECTIONS_PAGE_QUERY,
    PRODUCT_BY_ID_QUERY,
    PRODUCT_CUSTOM_ID_DEFINITION_CREATE,
    PRODUCT_CUSTOM_ID_DEFINITION_QUERY,
    PRODUCT_SET_MUTATION,
    PRODUCT_VARIANT_APPEND_MEDIA_MUTATION,
    PRODUCT_VARIANT_DETACH_MEDIA_MUTATION,
    PRODUCT_VARIANT_MEDIA_QUERY,
    PRODUCTS_BULK_QUERY,
)
from ..lib.bulk import ShopifyBulkRunner
from ..lib.client import ShopifyUserError
from ..lib.product import (
    merge_owned_fields,
    normalize_bulk_products,
    normalize_product_payload,
    sign_product_image_path,
)
from .webhook_event import WEBHOOK_HANDLERS


def _utc_datetime(value):
    if not value:
        return False
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


class ShopifyInstanceProductSync(models.Model):
    _inherit = "shopify.instance"

    @api.model
    def _cron_reconcile_products(self):
        instances = self.search([("active", "=", True), ("state", "=", "connected")])
        for instance in instances:
            instance.with_delay(
                description=self.env._(
                    "Reconcile Shopify products for %s", instance.name
                ),
                identity_key=f"shopify.products.bulk.{instance.id}",
            )._job_fetch_products_bulk()
            instance._write_log(
                entity="drift_products",
                direction="import",
                level="info",
                message=self.env._("Daily product drift reconciliation queued."),
                record=instance,
            )

    def action_import_products(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before importing.")
            )
        self.with_delay(
            description=self.env._("Import Shopify products for %s", self.name),
            identity_key=f"shopify.products.bulk.{self.id}",
        )._job_fetch_products_bulk()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Product import queued"),
                "message": self.env._(
                    "The full Shopify product import is running in the background."
                ),
                "type": "success",
                "sticky": False,
            },
        }

    def _job_fetch_products_bulk(self):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return 0
        if self.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before importing.")
            )
        snapshot_started_at = fields.Datetime.now()
        try:
            records = ShopifyBulkRunner(self._shopify_client()).run(PRODUCTS_BULK_QUERY)
            products = normalize_bulk_products(records)
            imported_ids = {product["id"] for product in products}
            for product in products:
                self.env["shopify.product.template"].with_delay(
                    description=self.env._("Import Shopify product %s", product["id"]),
                    identity_key=(f"shopify.product.bulk.{self.id}.{product['id']}"),
                )._job_import_product(
                    self.id,
                    product,
                    complete_snapshot=True,
                    payload_normalized=True,
                    snapshot_started_at=fields.Datetime.to_string(snapshot_started_at),
                )
            stale_bindings = self.env["shopify.product.template"].search(
                [
                    ("instance_id", "=", self.id),
                    ("shopify_id", "not in", list(imported_ids)),
                    ("remote_deleted", "=", False),
                    "|",
                    ("last_sync_date", "=", False),
                    ("last_sync_date", "<=", snapshot_started_at),
                ]
            )
            for binding in stale_bindings:
                self.env["shopify.product.template"].with_delay(
                    description=self.env._(
                        "Archive missing Shopify product %s", binding.shopify_id
                    ),
                    identity_key=(
                        f"shopify.product.sync.{self.id}.{binding.shopify_id}"
                    ),
                )._job_reconcile_missing_product(self.id, binding.shopify_id)
            self._queue_collection_imports()
        except Exception as exc:
            self._write_log(
                entity="product",
                direction="import",
                level="error",
                message=self.env._("Bulk product import failed: %s", exc),
                record=self,
            )
            return False

        self._write_log(
            entity="product",
            direction="import",
            level="info",
            message=self.env._("%s Shopify products queued for import.", len(products)),
            record=self,
        )
        return len(products)

    def _queue_collection_imports(self):
        self.ensure_one()
        client = self._shopify_client()
        after = None
        imported_ids = set()
        while True:
            data = client.execute(
                COLLECTIONS_PAGE_QUERY,
                {"after": after},
            )
            connection = data.get("collections", {})
            for collection in connection.get("nodes", []):
                imported_ids.add(collection["id"])
                self.env["shopify.collection"].with_delay(
                    description=self.env._(
                        "Import Shopify collection %s", collection["id"]
                    ),
                    identity_key=(
                        f"shopify.collection.import.{self.id}.{collection['id']}"
                    ),
                )._job_import_collection(self.id, collection)
            page_info = connection.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            if not after:
                break
        stale_collections = self.env["shopify.collection"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "not in", list(imported_ids)),
                ("active", "=", True),
            ]
        )
        for collection in stale_collections:
            self.env["shopify.collection"].with_delay(
                description=self.env._(
                    "Archive missing Shopify collection %s", collection.shopify_id
                ),
                identity_key=(
                    f"shopify.collection.delete.{self.id}.{collection.shopify_id}"
                ),
            )._job_archive_collection(self.id, collection.shopify_id)


class ShopifyProductTemplateSync(models.Model):
    _inherit = "shopify.product.template"

    def write(self, values):
        result = super().write(values)
        if "odoo_status" in values and not self.env.context.get("shopify_import"):
            for binding in self.filtered(
                lambda item: item.instance_id._is_product_field_owned_by(
                    "status", "odoo"
                )
            ):
                binding.odoo_id.with_context(skip_shopify_export=True).active = (
                    values["odoo_status"] != "ARCHIVED"
                )
                self._enqueue_product_export(binding.instance_id, binding.odoo_id)
        return result

    @api.model
    def _job_import_product(
        self,
        instance_id,
        payload,
        complete_snapshot=True,
        payload_normalized=False,
        snapshot_started_at=None,
    ):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        if instance.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before importing.")
            )
        shopify_id = payload.get("id") or payload.get("admin_graphql_api_id")
        self.env.cr.execute(
            "SELECT pg_advisory_xact_lock(%s, hashtext(%s))",
            (instance.id, str(shopify_id)),
        )
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                (
                    "shopify_id",
                    "=",
                    (shopify_id),
                ),
            ],
            limit=1,
        )
        snapshot_at = fields.Datetime.to_datetime(snapshot_started_at)
        if (
            snapshot_at
            and binding
            and binding.last_sync_date
            and binding.last_sync_date > snapshot_at
        ):
            return binding.id
        recent_webhook = snapshot_at and self._has_product_webhook_since(
            instance, shopify_id, snapshot_at
        )
        if recent_webhook:
            current_payload = self._fetch_complete_product(
                instance._shopify_client(),
                shopify_id,
                missing_ok=True,
            )
            if current_payload is None:
                if binding:
                    return self._job_archive_deleted_product(instance_id, shopify_id)
                return False
            payload = current_payload
            payload_normalized = False
        normalized = (
            payload if payload_normalized else normalize_product_payload(payload)
        )
        created_template = False
        if binding:
            template = binding.odoo_id.with_context(active_test=False)
        else:
            template = self._match_odoo_template(instance, normalized)
            if not template and not instance.product_create_if_missing:
                instance._write_log(
                    entity="product",
                    direction="import",
                    level="warning",
                    message=self.env._(
                        "Skipped Shopify product %(gid)s because no barcode "
                        "or SKU match exists.",
                        gid=normalized["id"],
                    ),
                )
                return False
            if not template:
                template = (
                    self.env["product.template"]
                    .with_context(skip_shopify_export=True)
                    .create(self._new_template_values(instance, normalized))
                )
                created_template = True
            binding = self.search(
                [
                    ("instance_id", "=", instance.id),
                    ("odoo_id", "=", template.id),
                    ("remote_deleted", "=", True),
                ],
                limit=1,
            )
            binding_values = {
                "shopify_id": normalized["id"],
                "handle": normalized["handle"],
                "status": normalized["status"],
                "odoo_status": normalized["status"],
                "initial_seed_pending": created_template,
                "remote_deleted": False,
            }
            if binding:
                binding.variant_binding_ids.unlink()
                binding.image_binding_ids.mapped("odoo_id").with_context(
                    skip_shopify_export=True
                ).unlink()
                binding.with_context(shopify_import=True).write(binding_values)
            else:
                binding = self.create(
                    {
                        **binding_values,
                        "instance_id": instance.id,
                        "odoo_id": template.id,
                    }
                )

        seed_all = binding.initial_seed_pending
        try:
            with self.env.cr.savepoint():
                self._apply_product_import(
                    binding,
                    normalized,
                    seed_all=seed_all,
                    complete_snapshot=complete_snapshot,
                )
        except Exception as exc:
            binding.write({"state": "error", "error_message": str(exc)})
            instance._write_log(
                entity="product",
                direction="import",
                level="error",
                message=self.env._(
                    "Product %(gid)s import failed: %(error)s",
                    gid=normalized["id"],
                    error=exc,
                ),
                record=binding,
            )
            return False

        binding.write(
            {
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
                "external_updated_at": _utc_datetime(normalized["updated_at"]),
                "initial_seed_pending": False,
                "remote_deleted": False,
            }
        )
        if self._has_odoo_owned_drift(binding, normalized):
            self._enqueue_product_export(instance, binding.odoo_id)
        instance._write_log(
            entity="product",
            direction="import",
            level="info",
            message=self.env._("Imported Shopify product %s.", normalized["id"]),
            record=binding,
        )
        return binding.id

    def _has_odoo_owned_drift(self, binding, product):
        instance = binding.instance_id
        owners = instance._product_field_owners()
        template = binding.odoo_id.with_context(active_test=False)
        if owners["name"] == "odoo" and product["name"] != template.name:
            return True
        if owners["description"] == "odoo" and product["description"] != (
            template.description_sale or ""
        ):
            return True
        if owners["status"] == "odoo" and product["status"] != binding.odoo_status:
            return True
        if owners["price"] == "odoo":
            for payload in product["variants"]:
                variant = self._variant_for_options(
                    template, payload["selected_options"]
                )
                if variant and Decimal(payload["price"]) != Decimal(
                    self._export_price(instance, variant)
                ):
                    return True
        if owners["images"] == "odoo":
            incoming_ids = {image["id"] for image in product["images"] if image["id"]}
            bound_ids = set(binding.image_binding_ids.mapped("shopify_id"))
            bound_ids.update(binding.variant_binding_ids.mapped("image_shopify_id"))
            if binding.main_image_shopify_id:
                bound_ids.add(binding.main_image_shopify_id)
            if incoming_ids != {item for item in bound_ids if item}:
                return True
        return False

    @api.model
    def _has_product_webhook_since(self, instance, shopify_id, since):
        events = self.env["shopify.webhook.event"].search(
            [
                ("instance_id", "=", instance.id),
                (
                    "topic",
                    "in",
                    [
                        "products/create",
                        "products/update",
                        "products/delete",
                    ],
                ),
                ("create_date", ">=", since),
            ]
        )
        for event in events:
            payload_id = event.payload.get("admin_graphql_api_id") or event.payload.get(
                "id"
            )
            if payload_id and not str(payload_id).startswith("gid://"):
                payload_id = f"gid://shopify/Product/{payload_id}"
            if payload_id == shopify_id:
                return True
        return False

    @api.model
    def _job_import_product_from_api(self, instance_id, shopify_id):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        try:
            payload = self._fetch_complete_product(
                instance._shopify_client(),
                shopify_id,
                missing_ok=True,
            )
        except Exception as exc:
            binding = self.search(
                [
                    ("instance_id", "=", instance_id),
                    ("shopify_id", "=", shopify_id),
                ],
                limit=1,
            )
            if binding:
                binding.write({"state": "error", "error_message": str(exc)})
            instance._write_log(
                entity="product",
                direction="import",
                level="error",
                message=self.env._(
                    "Could not fetch product %(gid)s: %(error)s",
                    gid=shopify_id,
                    error=exc,
                ),
                record=binding or None,
            )
            return False
        if payload is None:
            return self._job_archive_deleted_product(instance_id, shopify_id)
        return self._job_import_product(
            instance_id,
            payload,
            complete_snapshot=True,
            payload_normalized=False,
        )

    @api.model
    def _fetch_complete_product(  # noqa: C901
        self, client, shopify_id, *, missing_ok=False
    ):
        cursors = {
            "variants": None,
            "media": None,
            "collections": None,
        }
        accumulated = {
            "variants": {},
            "media": {},
            "collections": {},
        }
        product = None
        while True:
            data = client.execute(
                PRODUCT_BY_ID_QUERY,
                {
                    "id": shopify_id,
                    "variantsAfter": cursors["variants"],
                    "mediaAfter": cursors["media"],
                    "collectionsAfter": cursors["collections"],
                },
            )
            page = data.get("product")
            if not isinstance(page, dict):
                if missing_ok:
                    return None
                raise UserError(
                    self.env._("Shopify product %s was not found.", shopify_id)
                )
            if product is None:
                product = {
                    key: value for key, value in page.items() if key not in accumulated
                }
            has_next = False
            for connection_name in accumulated:
                connection = page.get(connection_name) or {}
                for node in connection.get("nodes", []):
                    if node.get("id"):
                        accumulated[connection_name][node["id"]] = node
                page_info = connection.get("pageInfo") or {}
                if page_info.get("hasNextPage"):
                    has_next = True
                    cursor = page_info.get("endCursor")
                    if not cursor:
                        raise UserError(
                            self.env._("Shopify returned an invalid pagination cursor.")
                        )
                    cursors[connection_name] = cursor
            if not has_next:
                break
        for connection_name, nodes in accumulated.items():
            product[connection_name] = {"nodes": list(nodes.values())}
        for variant in product["variants"]["nodes"]:
            connection = variant.get("media") or {}
            media_by_id = {
                node["id"]: node
                for node in connection.get("nodes", [])
                if node.get("id")
            }
            page_info = connection.get("pageInfo") or {}
            after = page_info.get("endCursor")
            while page_info.get("hasNextPage"):
                if not after:
                    raise UserError(
                        self.env._("Shopify returned an invalid variant media cursor.")
                    )
                data = client.execute(
                    PRODUCT_VARIANT_MEDIA_QUERY,
                    {"id": variant["id"], "after": after},
                )
                connection = (data.get("productVariant") or {}).get("media") or {}
                for node in connection.get("nodes", []):
                    if node.get("id"):
                        media_by_id[node["id"]] = node
                page_info = connection.get("pageInfo") or {}
                after = page_info.get("endCursor")
            variant["media"] = {"nodes": list(media_by_id.values())}
        return product

    @api.model
    def _match_odoo_template(self, instance, product):
        product_model = self.env["product.product"].with_context(active_test=False)
        variants = product.get("variants") or []
        company_domain = [("company_id", "=", instance.company_id.id)]
        for field_name, payload_key in (
            ("barcode", "barcode"),
            ("default_code", "sku"),
        ):
            identifiers = [
                variant[payload_key] for variant in variants if variant.get(payload_key)
            ]
            for identifier in identifiers:
                candidates = product_model.search(
                    [(field_name, "=", identifier), *company_domain]
                )
                for candidate in candidates:
                    existing = self.search(
                        [
                            ("instance_id", "=", instance.id),
                            ("odoo_id", "=", candidate.product_tmpl_id.id),
                        ],
                        limit=1,
                    )
                    if not existing or existing.remote_deleted:
                        return candidate.product_tmpl_id
        return self.env["product.template"]

    @api.model
    def _new_template_values(self, instance, product):
        values = {
            "name": product["name"]
            or self.env._("Shopify Product %s", product["id"].rsplit("/", 1)[-1]),
            "company_id": instance.company_id.id,
            "description_sale": product["description"],
            "active": product["status"] != "ARCHIVED",
        }
        if product["variants"]:
            values["list_price"] = self._shopify_amount_to_company(
                instance, product["variants"][0]["price"]
            )
        return values

    @api.model
    def _shopify_amount_to_company(self, instance, amount):
        shop_currency = (
            instance.shop_currency_id or instance.product_pricelist_id.currency_id
        )
        company_currency = instance.company_id.currency_id
        if shop_currency == company_currency:
            return amount
        return shop_currency._convert(
            float(Decimal(str(amount))),
            company_currency,
            instance.company_id,
            fields.Date.context_today(self),
        )

    def _apply_product_import(
        self,
        binding,
        product,
        *,
        seed_all,
        complete_snapshot,
    ):
        instance = binding.instance_id
        owners = instance._product_field_owners()
        template = binding.odoo_id.with_context(
            active_test=False, skip_shopify_export=True
        )
        current = (
            {}
            if seed_all
            else {
                "name": template.name,
                "description": template.description_sale or "",
                "price": (str(template.list_price) if product["variants"] else "0"),
                "images": [],
                "status": "ACTIVE" if template.active else "ARCHIVED",
            }
        )
        incoming = {
            "name": product["name"] or template.name,
            "description": product["description"],
            "price": (product["variants"][0]["price"] if product["variants"] else "0"),
            "images": product["images"],
            "status": product["status"],
        }
        merged = merge_owned_fields(
            current,
            incoming,
            owners,
            source="shopify",
            seed_missing=seed_all,
        )
        values = {}
        if "name" in merged and merged.get("name") != current.get("name"):
            values["name"] = merged["name"]
        if "description" in merged and merged.get("description") != current.get(
            "description"
        ):
            values["description_sale"] = merged["description"]
        if (
            product["variants"]
            and "price" in merged
            and merged.get("price") != current.get("price")
        ):
            values["list_price"] = self._shopify_amount_to_company(
                instance, merged["price"]
            )
        if "status" in merged and merged.get("status") != current.get("status"):
            values["active"] = merged["status"] != "ARCHIVED"
        if values:
            template.write(values)
        binding_values = {
            "handle": product["handle"],
            "status": product["status"],
        }
        if seed_all or owners["status"] == "shopify":
            binding_values["odoo_status"] = product["status"]
        binding.with_context(shopify_import=True).write(binding_values)
        self._sync_options(template, product["options"], product["variants"])
        self._sync_variants(
            binding,
            product["variants"],
            seed_all=seed_all,
            prune=complete_snapshot,
        )
        self._sync_collections(
            binding,
            product["collections"],
            replace=complete_snapshot,
        )
        if seed_all or owners["images"] == "shopify":
            self._sync_images(
                binding,
                merged.get("images", []),
                product["variants"],
                prune=complete_snapshot,
            )

    @api.model
    def _sync_options(self, template, options, variants):
        real_options = options
        if (
            len(options) == 1
            and options[0]["name"].lower() == "title"
            and all(
                variant.get("selected_options")
                in ([], [{"name": "Title", "value": "Default Title"}])
                for variant in variants
            )
        ):
            real_options = []
        incompatible_lines = template.attribute_line_ids.filtered(
            lambda item: item.attribute_id.create_variant != "dynamic"
        )
        if incompatible_lines:
            incompatible_lines.with_context(skip_shopify_export=True).unlink()
        wanted_lines = self.env["product.template.attribute.line"]
        for option in sorted(real_options, key=lambda item: item.get("position") or 0):
            line = template.attribute_line_ids.filtered(
                lambda item, option=option: (
                    item.attribute_id.name == option["name"]
                    and item.attribute_id.create_variant == "dynamic"
                )
            )[:1]
            attribute = line.attribute_id or self.env["product.attribute"].search(
                [
                    ("name", "=", option["name"]),
                    ("create_variant", "=", "dynamic"),
                ],
                limit=1,
            )
            if not attribute:
                attribute = self.env["product.attribute"].create(
                    {
                        "name": option["name"],
                        "create_variant": "dynamic",
                    }
                )
            value_records = self.env["product.attribute.value"]
            for value_name in option["values"]:
                value = self.env["product.attribute.value"].search(
                    [
                        ("attribute_id", "=", attribute.id),
                        ("name", "=", value_name),
                    ],
                    limit=1,
                )
                if not value:
                    value = self.env["product.attribute.value"].create(
                        {
                            "attribute_id": attribute.id,
                            "name": value_name,
                        }
                    )
                value_records |= value
            if line:
                wanted_lines |= line
                if set(line.value_ids.ids) != set(value_records.ids):
                    line.with_context(skip_shopify_export=True).write(
                        {"value_ids": [Command.set(value_records.ids)]}
                    )
            else:
                template.with_context(skip_shopify_export=True).write(
                    {
                        "attribute_line_ids": [
                            Command.create(
                                {
                                    "attribute_id": attribute.id,
                                    "value_ids": [Command.set(value_records.ids)],
                                }
                            )
                        ]
                    }
                )
                wanted_lines |= template.attribute_line_ids.filtered(
                    lambda item, attribute=attribute: item.attribute_id == attribute
                )[:1]
        stale_lines = template.attribute_line_ids - wanted_lines
        if stale_lines:
            stale_lines.with_context(skip_shopify_export=True).unlink()

    def _sync_variants(self, template_binding, variants, *, seed_all, prune):
        instance = template_binding.instance_id
        price_owned = instance._is_product_field_owned_by("price", "shopify")
        imported_ids = set()
        for payload in variants:
            if not payload["id"]:
                continue
            imported_ids.add(payload["id"])
            variant_binding = self.env["shopify.product.variant"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            )
            variant = self._variant_for_options(
                template_binding.odoo_id,
                payload["selected_options"],
                create=True,
            )
            if not variant:
                raise UserError(
                    self.env._(
                        "No Odoo variant matches Shopify options for %(gid)s.",
                        gid=payload["id"],
                    )
                )
            values = {
                "default_code": payload["sku"] or False,
                "barcode": payload["barcode"] or False,
                "active": template_binding.odoo_id.active,
            }
            variant.with_context(skip_shopify_export=True).write(values)
            binding_values = {
                "template_binding_id": template_binding.id,
                "odoo_id": variant.id,
                "sku_snapshot": payload["sku"],
                "barcode_snapshot": payload["barcode"],
                "price_snapshot": payload["price"],
                "inventory_item_shopify_id": payload.get("inventory_item_id"),
                "inventory_tracked": payload.get("inventory_tracked", False),
                "external_updated_at": _utc_datetime(payload["updated_at"]),
                "last_sync_date": fields.Datetime.now(),
                "state": "synced",
                "error_message": False,
            }
            if variant_binding:
                variant_binding.write(binding_values)
            else:
                variant_binding = self.env["shopify.product.variant"].create(
                    {
                        **binding_values,
                        "instance_id": instance.id,
                        "shopify_id": payload["id"],
                    }
                )
            if price_owned or (seed_all and len(variants) > 1):
                self._sync_variant_price(
                    template_binding.instance_id,
                    variant_binding,
                    payload["price"],
                )
            elif len(variants) <= 1 and variant_binding.price_item_id:
                variant_binding.price_item_id.with_context(
                    skip_shopify_export=True
                ).unlink()
                variant_binding.price_item_id = False
        if prune:
            imported_variants = template_binding.variant_binding_ids.filtered(
                lambda item: item.shopify_id in imported_ids
            ).mapped("odoo_id")
            extra_variants = (
                template_binding.odoo_id.with_context(
                    active_test=False
                ).product_variant_ids
                - imported_variants
            )
            extra_variants.with_context(skip_shopify_export=True).write(
                {"active": False}
            )
            stale_bindings = template_binding.variant_binding_ids.filtered(
                lambda item: item.shopify_id not in imported_ids
            )
            stale_bindings.mapped("price_item_id").with_context(
                skip_shopify_export=True
            ).unlink()
            stale_bindings.unlink()

    @api.model
    def _sync_variant_price(self, instance, variant_binding, price):
        values = {
            "pricelist_id": instance.product_pricelist_id.id,
            "applied_on": "0_product_variant",
            "product_id": variant_binding.odoo_id.id,
            "compute_price": "fixed",
            "fixed_price": price,
            "min_quantity": 0,
        }
        price_item = variant_binding.price_item_id
        if not price_item:
            price_item = self.env["product.pricelist.item"].search(
                [
                    ("pricelist_id", "=", instance.product_pricelist_id.id),
                    ("product_id", "=", variant_binding.odoo_id.id),
                    ("applied_on", "=", "0_product_variant"),
                ],
                limit=1,
            )
        if price_item:
            price_item.with_context(skip_shopify_export=True).write(values)
        else:
            price_item = (
                self.env["product.pricelist.item"]
                .with_context(skip_shopify_export=True)
                .create(values)
            )
        variant_binding.price_item_id = price_item

    @api.model
    def _variant_for_options(self, template, selected_options, *, create=False):
        variants = template.with_context(active_test=False).product_variant_ids
        if not selected_options or selected_options == [
            {"name": "Title", "value": "Default Title"}
        ]:
            return variants[:1]
        wanted = {(option["name"], option["value"]) for option in selected_options}
        for variant in variants:
            actual = {
                (value.attribute_id.name, value.name)
                for value in variant.product_template_attribute_value_ids
            }
            if actual == wanted:
                return variant
        if create:
            combination = self.env["product.template.attribute.value"]
            for option in selected_options:
                line = template.attribute_line_ids.filtered(
                    lambda item, option=option: (
                        item.attribute_id.name == option["name"]
                    )
                )[:1]
                template_value = line.product_template_value_ids.filtered(
                    lambda item, option=option: item.name == option["value"]
                )[:1]
                if not template_value:
                    return self.env["product.product"]
                combination |= template_value
            return template._create_product_variant(combination)
        return self.env["product.product"]

    def _sync_collections(self, template_binding, collections, *, replace):
        collection_records = self.env["shopify.collection"]
        for payload in collections:
            if not payload["id"]:
                continue
            values = {
                "name": payload["name"],
                "handle": payload["handle"],
                "collection_type": payload["type"],
                "external_updated_at": _utc_datetime(payload.get("updated_at")),
                "active": True,
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
            }
            collection = self.env["shopify.collection"]._upsert_shopify_collection(
                template_binding.instance_id.id,
                payload["id"],
                values,
            )
            collection_records |= collection
        if replace:
            template_binding.collection_ids = [Command.set(collection_records.ids)]
        else:
            template_binding.collection_ids = [
                Command.link(collection_id) for collection_id in collection_records.ids
            ]

    def _sync_images(self, template_binding, images, variants, *, prune):
        imported_ids = {image["id"] for image in images if image.get("id")}
        variants_by_media = {}
        bindings_by_gid = {
            item.shopify_id: item for item in template_binding.variant_binding_ids
        }
        for variant in variants:
            variant_binding = bindings_by_gid.get(variant["id"])
            if variant_binding:
                for media_id in variant["media_ids"]:
                    variants_by_media.setdefault(
                        media_id, self.env["shopify.product.variant"]
                    )
                    variants_by_media[media_id] |= variant_binding
        for position, payload in enumerate(images, start=1):
            if not payload["id"] or not payload["url"]:
                continue
            image_binding = self.env["shopify.product.image"].search(
                [
                    ("instance_id", "=", template_binding.instance_id.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            )
            image_bytes = self._download_image(payload["url"])
            checksum = hashlib.sha256(image_bytes).hexdigest()
            image_values = {
                "name": payload["alt"]
                or self.env._(
                    "%(product)s image %(position)s",
                    product=template_binding.odoo_id.name,
                    position=position,
                ),
                "image_1920": base64.b64encode(image_bytes),
                "sequence": position * 10,
            }
            variant_bindings = variants_by_media.get(
                payload["id"], self.env["shopify.product.variant"]
            )
            variant_binding = variant_bindings[:1]
            if len(variant_bindings) == 1:
                image_values["product_variant_id"] = variant_binding.odoo_id.id
                image_values["product_tmpl_id"] = False
            else:
                image_values["product_tmpl_id"] = template_binding.odoo_id.id
                image_values["product_variant_id"] = False
            if image_binding:
                image_binding.odoo_id.with_context(skip_shopify_export=True).write(
                    image_values
                )
                image_binding.write(
                    {
                        "source_url": payload["url"],
                        "image_checksum": checksum,
                        "variant_binding_id": variant_binding.id
                        if variant_binding
                        else False,
                        "variant_binding_ids": [Command.set(variant_bindings.ids)],
                        "state": "synced",
                        "error_message": False,
                        "last_sync_date": fields.Datetime.now(),
                    }
                )
            else:
                image = (
                    self.env["product.image"]
                    .with_context(skip_shopify_export=True)
                    .create(image_values)
                )
                self.env["shopify.product.image"].create(
                    {
                        "instance_id": template_binding.instance_id.id,
                        "shopify_id": payload["id"],
                        "template_binding_id": template_binding.id,
                        "variant_binding_id": variant_binding.id
                        if variant_binding
                        else False,
                        "variant_binding_ids": [Command.set(variant_bindings.ids)],
                        "odoo_id": image.id,
                        "source_url": payload["url"],
                        "image_checksum": checksum,
                        "state": "synced",
                        "last_sync_date": fields.Datetime.now(),
                    }
                )
        if prune:
            stale_bindings = template_binding.image_binding_ids.filtered(
                lambda item: item.shopify_id not in imported_ids
            )
            stale_bindings.mapped("odoo_id").with_context(
                skip_shopify_export=True
            ).unlink()

    @api.model
    def _download_image(self, url):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content

    @api.model
    def _job_archive_deleted_product(self, instance_id, shopify_id):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        binding = self.search(
            [
                ("instance_id", "=", instance_id),
                ("shopify_id", "=", shopify_id),
            ],
            limit=1,
        )
        if not instance or not instance.active or not binding:
            return False
        if instance.product_delete_behavior == "archive":
            binding.odoo_id.with_context(skip_shopify_export=True).active = False
        binding.write(
            {
                "status": "ARCHIVED",
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
                "remote_deleted": True,
            }
        )
        instance._write_log(
            entity="product",
            direction="import",
            level="info",
            message=self.env._("Processed deletion of Shopify product %s.", shopify_id),
            record=binding,
        )
        return True

    @api.model
    def _job_reconcile_missing_product(self, instance_id, shopify_id):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        try:
            payload = self._fetch_complete_product(
                instance._shopify_client(),
                shopify_id,
                missing_ok=True,
            )
        except Exception as exc:
            instance._write_log(
                entity="product",
                direction="import",
                level="error",
                message=self.env._(
                    "Could not verify missing product %(gid)s: %(error)s",
                    gid=shopify_id,
                    error=exc,
                ),
            )
            return False
        if payload is None:
            return self._job_archive_deleted_product(instance_id, shopify_id)
        return self._job_import_product(instance_id, payload)

    @api.model
    def _enqueue_product_export(self, instance, template):
        if not instance.active:
            return False
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("odoo_id", "=", template.id),
            ],
            limit=1,
        )
        identity = binding.shopify_id if binding else f"odoo-{template.id}"
        self.with_delay(
            description=self.env._("Export %s to Shopify", template.display_name),
            identity_key=f"shopify.product.export.{instance.id}.{identity}",
        )._job_export_product(instance.id, template.id)

    @api.model
    def _job_export_product(self, instance_id, template_id):
        self = self.sudo()
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if instance:
            self = self.with_company(instance.company_id)
            instance = self.env["shopify.instance"].browse(instance_id)
        template = (
            self.env["product.template"]
            .with_context(active_test=False)
            .browse(template_id)
            .exists()
        )
        if not instance or not instance.active or not template:
            return False
        if instance.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before exporting.")
            )
        if template.company_id != instance.company_id:
            instance._write_log(
                entity="product",
                direction="export",
                level="error",
                message=self.env._(
                    "Product %(product)s belongs to a different company.",
                    product=template.display_name,
                ),
                record=template,
            )
            return False
        binding = self.search(
            [
                ("instance_id", "=", instance.id),
                ("odoo_id", "=", template.id),
            ],
            limit=1,
        )
        try:
            client = instance._shopify_client()
            recreate = False
            if not binding:
                self._ensure_product_custom_id_definition(client)
            existing_product = None
            preserved_file_ids = []
            if binding:
                existing_product = self._fetch_complete_product(
                    client, binding.shopify_id, missing_ok=True
                )
                if existing_product is None:
                    recreate = True
                    self._ensure_product_custom_id_definition(client)
            if existing_product and instance._is_product_field_owned_by(
                "images", "odoo"
            ):
                preserved_file_ids = [
                    media["id"]
                    for media in (existing_product.get("media", {}).get("nodes", []))
                    if media.get("id") and media.get("mediaContentType") != "IMAGE"
                ]
            product_input, file_targets = self._product_set_input(
                instance,
                template,
                binding,
                preserved_file_ids=preserved_file_ids,
                existing_product=existing_product,
                recreate=recreate,
            )
            identifier = (
                {"id": binding.shopify_id}
                if binding and not recreate
                else self._product_upsert_identifier(instance, template)
            )
            data = client.execute(
                PRODUCT_SET_MUTATION,
                {"identifier": identifier, "input": product_input},
            )
            product = data.get("productSet", {}).get("product")
            if not product:
                raise UserError(
                    self.env._("Shopify did not return the exported product.")
                )
            complete_product = self._fetch_complete_product(client, product["id"])
            with self.env.cr.savepoint():
                binding, append_media, detach_media = self._update_export_bindings(
                    instance,
                    template,
                    binding,
                    complete_product,
                    file_targets,
                )
            if detach_media:
                client.execute(
                    PRODUCT_VARIANT_DETACH_MEDIA_MUTATION,
                    {
                        "productId": complete_product["id"],
                        "variantMedia": detach_media,
                    },
                )
            if append_media:
                client.execute(
                    PRODUCT_VARIANT_APPEND_MEDIA_MUTATION,
                    {
                        "productId": complete_product["id"],
                        "variantMedia": append_media,
                    },
                )
        except Exception as exc:
            if binding:
                binding.write({"state": "error", "error_message": str(exc)})
            instance._write_log(
                entity="product",
                direction="export",
                level="error",
                message=self.env._("Product export failed: %s", exc),
                record=binding or template,
            )
            raise

        instance._write_log(
            entity="product",
            direction="export",
            level="info",
            message=self.env._(
                "Exported Odoo product %s to Shopify.", template.display_name
            ),
            record=binding,
        )
        return binding.id

    def _product_set_input(  # noqa: C901
        self,
        instance,
        template,
        binding,
        *,
        preserved_file_ids=(),
        existing_product=None,
        recreate=False,
    ):
        is_new = not binding or recreate
        owners = instance._product_field_owners()
        product_input = {}
        if is_new or owners["name"] == "odoo":
            product_input["title"] = template.name
        if is_new or owners["description"] == "odoo":
            product_input["descriptionHtml"] = template.description_sale or ""
        if is_new or owners["status"] == "odoo":
            product_input["status"] = (
                binding.odoo_status
                if binding
                else ("ACTIVE" if template.active else "ARCHIVED")
            )

        existing_options = {
            option.get("name"): option
            for option in (existing_product or {}).get("options", [])
        }
        variant_lines = template.attribute_line_ids.filtered(
            lambda line: line.attribute_id.create_variant != "no_variant"
        )
        options = []
        for position, line in enumerate(variant_lines, start=1):
            existing_option = existing_options.get(line.attribute_id.name) or {}
            existing_values = {
                value.get("name"): value
                for value in existing_option.get("optionValues", [])
            }
            option_input = {
                "name": line.attribute_id.name,
                "position": position,
                "values": [],
            }
            if existing_option.get("id"):
                option_input["id"] = existing_option["id"]
            for value in line.value_ids:
                value_input = {"name": value.name}
                existing_value = existing_values.get(value.name) or {}
                if existing_value.get("id"):
                    value_input["id"] = existing_value["id"]
                option_input["values"].append(value_input)
            options.append(option_input)
        if not options:
            existing_option = existing_options.get("Title") or {}
            existing_value = next(
                (
                    value
                    for value in existing_option.get("optionValues", [])
                    if value.get("name") == "Default Title"
                ),
                {},
            )
            option_input = {
                "name": "Title",
                "position": 1,
                "values": [{"name": "Default Title"}],
            }
            if existing_option.get("id"):
                option_input["id"] = existing_option["id"]
            if existing_value.get("id"):
                option_input["values"][0]["id"] = existing_value["id"]
            options = [option_input]
        product_input["productOptions"] = options

        variants = []
        export_variants = self._exportable_variants(template, binding)
        variant_bindings = (
            {item.odoo_id.id: item for item in binding.variant_binding_ids}
            if binding and not recreate
            else {}
        )
        for variant in export_variants:
            variant_binding = variant_bindings.get(variant.id)
            values = {
                "optionValues": [
                    {
                        "optionName": value.attribute_id.name,
                        "name": value.name,
                    }
                    for value in variant.product_template_attribute_value_ids
                ],
                "sku": variant.default_code or "",
                "barcode": variant.barcode or "",
            }
            if not values["optionValues"]:
                values["optionValues"] = [
                    {
                        "optionName": "Title",
                        "name": "Default Title",
                    }
                ]
            if variant_binding:
                values["id"] = variant_binding.shopify_id
            if is_new or owners["price"] == "odoo":
                values["price"] = self._export_price(instance, variant)
            variants.append(values)
        product_input["variants"] = variants

        custom_collections = (
            binding.collection_ids.filtered(
                lambda item: item.collection_type == "custom"
            )
            if binding
            else self.env["shopify.collection"]
        )
        if binding:
            product_input["collections"] = custom_collections.mapped("shopify_id")

        file_targets = []
        if is_new or owners["images"] == "odoo":
            files, file_targets = self._product_files(
                instance,
                template,
                binding if not recreate else False,
                export_variants,
                preserved_file_ids,
                (existing_product or {}).get("media", {}).get("nodes", []),
            )
            product_input["files"] = files
            file_by_variant = {}
            for file_input, target in zip(files, file_targets, strict=False):
                if target and target.get("variant_ids"):
                    for variant_id in target["variant_ids"]:
                        file_by_variant.setdefault(variant_id, file_input)
            for variant_input, variant in zip(
                variants,
                export_variants,
                strict=False,
            ):
                if variant.id in file_by_variant:
                    variant_input["file"] = file_by_variant[variant.id]
        return product_input, file_targets

    @api.model
    def _ensure_product_custom_id_definition(self, client):
        identifier = {
            "ownerType": "PRODUCT",
            "namespace": "$app",
            "key": "odoo_product_id",
        }
        data = client.execute(
            PRODUCT_CUSTOM_ID_DEFINITION_QUERY,
            {"identifier": identifier},
        )
        if data.get("metafieldDefinition"):
            return
        try:
            client.execute(
                PRODUCT_CUSTOM_ID_DEFINITION_CREATE,
                {
                    "definition": {
                        "name": "Odoo Product ID",
                        "namespace": "$app",
                        "key": "odoo_product_id",
                        "type": "id",
                        "ownerType": "PRODUCT",
                    }
                },
            )
        except ShopifyUserError:
            data = client.execute(
                PRODUCT_CUSTOM_ID_DEFINITION_QUERY,
                {"identifier": identifier},
            )
            if not data.get("metafieldDefinition"):
                raise

    @api.model
    def _product_upsert_identifier(self, instance, template):
        database_uuid = (
            self.env["ir.config_parameter"].sudo().get_param("database.uuid")
        )
        value = f"{database_uuid or self.env.cr.dbname}:{instance.id}:{template.id}"
        return {
            "customId": {
                "key": "odoo_product_id",
                "value": value,
            }
        }

    @api.model
    def _exportable_variants(self, template, binding=None):
        allowed_values = {
            line.attribute_id.id: set(line.value_ids.ids)
            for line in template.attribute_line_ids
            if line.attribute_id.create_variant != "no_variant"
        }

        def is_current_combination(variant):
            values = variant.product_template_attribute_value_ids
            if len(values) != len(allowed_values):
                return False
            return all(
                value.product_attribute_value_id.id
                in allowed_values.get(value.attribute_id.id, set())
                for value in values
            )

        variants = template.with_context(
            active_test=False
        ).product_variant_ids.filtered(is_current_combination)
        if template.active:
            return variants.filtered("active")
        if binding:
            bound_ids = set(binding.variant_binding_ids.odoo_id.ids)
            return variants.filtered(lambda variant: variant.id in bound_ids)
        return variants

    @api.model
    def _export_price(self, instance, variant):
        pricelist = instance.product_pricelist_id.with_company(instance.company_id)
        amount = (
            pricelist._get_product_price(variant, 1.0)
            if pricelist
            else variant.lst_price
        )
        rounded = instance.shop_currency_id.round(amount)
        return format(Decimal(str(rounded)), "f")

    def _product_files(
        self,
        instance,
        template,
        binding,
        variants,
        preserved_file_ids,
        existing_media,
    ):
        files = [{"id": media_id} for media_id in preserved_file_ids]
        targets = [None] * len(files)
        existing_media_by_alt = {
            media.get("alt"): media.get("id")
            for media in existing_media
            if media.get("alt") and media.get("id")
        }
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        if not base_url:
            raise UserError(self.env._("Configure the Odoo web base URL first."))

        if template.image_1920:
            checksum = self._binary_checksum(template.image_1920)
            media_id = binding.main_image_shopify_id if binding else False
            unchanged = binding and binding.main_image_checksum == checksum
            export_alt = self._export_image_alt(template.name, template, checksum)
            matched_media_id = (
                media_id
                if media_id and unchanged
                else existing_media_by_alt.get(export_alt)
            )
            files.append(
                {"id": matched_media_id}
                if matched_media_id
                else {
                    "originalSource": self._public_image_url(
                        base_url, instance, template, checksum
                    ),
                    "alt": export_alt,
                }
            )
            targets.append(
                {
                    "kind": "template",
                    "record": template,
                    "checksum": checksum,
                    "media_id": matched_media_id,
                    "alt": export_alt,
                }
            )

        variant_bindings = (
            {item.odoo_id.id: item for item in binding.variant_binding_ids}
            if binding
            else {}
        )
        for variant in variants:
            if not variant.image_variant_1920:
                continue
            checksum = self._binary_checksum(variant.image_variant_1920)
            variant_binding = variant_bindings.get(variant.id)
            media_id = variant_binding.image_shopify_id if variant_binding else False
            unchanged = variant_binding and variant_binding.image_checksum == checksum
            export_alt = self._export_image_alt(variant.display_name, variant, checksum)
            matched_media_id = (
                media_id
                if media_id and unchanged
                else existing_media_by_alt.get(export_alt)
            )
            files.append(
                {"id": matched_media_id}
                if matched_media_id
                else {
                    "originalSource": self._public_image_url(
                        base_url, instance, variant, checksum
                    ),
                    "alt": export_alt,
                }
            )
            targets.append(
                {
                    "kind": "variant",
                    "record": variant,
                    "variant_id": variant.id,
                    "variant_ids": [variant.id],
                    "checksum": checksum,
                    "media_id": matched_media_id,
                    "alt": export_alt,
                }
            )

        image_bindings = (
            {item.odoo_id.id: item for item in binding.image_binding_ids}
            if binding
            else {}
        )
        extra_images = (
            template.product_template_image_ids | variants.product_variant_image_ids
        )
        for image in extra_images:
            if not image.image_1920:
                continue
            checksum = self._binary_checksum(image.image_1920)
            image_binding = image_bindings.get(image.id)
            media_id = image_binding.shopify_id if image_binding else False
            unchanged = image_binding and image_binding.image_checksum == checksum
            export_alt = self._export_image_alt(image.name, image, checksum)
            matched_media_id = (
                media_id
                if media_id and unchanged
                else existing_media_by_alt.get(export_alt)
            )
            files.append(
                {"id": matched_media_id}
                if matched_media_id
                else {
                    "originalSource": self._public_image_url(
                        base_url, instance, image, checksum
                    ),
                    "alt": export_alt,
                }
            )
            targets.append(
                {
                    "kind": "extra",
                    "record": image,
                    "variant_id": image.product_variant_id.id,
                    "variant_ids": (
                        image_binding.variant_binding_ids.odoo_id.ids
                        if image_binding and image_binding.variant_binding_ids
                        else image.product_variant_id.ids
                    ),
                    "checksum": checksum,
                    "media_id": matched_media_id,
                    "alt": export_alt,
                }
            )
        return files, targets

    @api.model
    def _export_image_alt(self, label, record, checksum):
        return (
            f"{label or record.display_name} "
            f"[odoo:{record._name}:{record.id}:{checksum[:12]}]"
        )

    @api.model
    def _public_image_url(self, base_url, instance, record, checksum):
        signature = sign_product_image_path(
            instance.webhook_secret,
            instance.id,
            record._name,
            record.id,
            checksum,
        )
        return (
            f"{base_url.rstrip('/')}/shopify/product-image/"
            f"{instance.id}/{record._name}/{record.id}/{checksum}/{signature}"
        )

    @api.model
    def _binary_checksum(self, value):
        encoded = value.encode() if isinstance(value, str) else value
        raw = base64.b64decode(encoded)
        return hashlib.sha256(raw).hexdigest()

    def _update_export_bindings(  # noqa: C901
        self, instance, template, binding, product, file_targets
    ):
        normalized = normalize_product_payload(product)
        values = {
            "shopify_id": normalized["id"],
            "handle": normalized["handle"],
            "status": normalized["status"],
            "odoo_status": (binding.odoo_status if binding else normalized["status"]),
            "state": "synced",
            "error_message": False,
            "external_updated_at": _utc_datetime(normalized["updated_at"]),
            "last_sync_date": fields.Datetime.now(),
        }
        if binding:
            binding.with_context(shopify_import=True).write(values)
        else:
            binding = self.create(
                {
                    **values,
                    "instance_id": instance.id,
                    "odoo_id": template.id,
                }
            )

        exported_variant_ids = set()
        for payload in normalized["variants"]:
            exported_variant_ids.add(payload["id"])
            variant = self._variant_for_options(template, payload["selected_options"])
            if not variant:
                continue
            variant_binding = self.env["shopify.product.variant"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            ) or self.env["shopify.product.variant"].search(
                [
                    ("instance_id", "=", instance.id),
                    ("odoo_id", "=", variant.id),
                ],
                limit=1,
            )
            variant_values = {
                "template_binding_id": binding.id,
                "odoo_id": variant.id,
                "sku_snapshot": payload["sku"],
                "barcode_snapshot": payload["barcode"],
                "price_snapshot": payload["price"],
                "inventory_item_shopify_id": payload.get("inventory_item_id"),
                "inventory_tracked": payload.get("inventory_tracked", False),
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
            }
            if variant_binding:
                variant_binding.write({**variant_values, "shopify_id": payload["id"]})
            else:
                self.env["shopify.product.variant"].create(
                    {
                        **variant_values,
                        "instance_id": instance.id,
                        "shopify_id": payload["id"],
                    }
                )
        stale_variant_bindings = binding.variant_binding_ids.filtered(
            lambda item: item.shopify_id not in exported_variant_ids
        )
        stale_variant_bindings.mapped("price_item_id").with_context(
            skip_shopify_export=True
        ).unlink()
        stale_variant_bindings.unlink()

        desired_media_by_variant_id = {}
        media = normalized["images"]
        media_by_id = {item["id"]: item for item in media if item["id"]}
        media_by_alt = {item["alt"]: item for item in media if item["alt"]}
        for target in file_targets:
            if target is None:
                continue
            payload = media_by_id.get(target.get("media_id")) or media_by_alt.get(
                target.get("alt")
            )
            if not payload:
                raise UserError(
                    self.env._("Shopify has not finished processing an exported image.")
                )
            for variant_odoo_id in target.get("variant_ids", []):
                variant_binding = binding.variant_binding_ids.filtered(
                    lambda item, variant_odoo_id=variant_odoo_id: (
                        item.odoo_id.id == variant_odoo_id
                    )
                )[:1]
                if variant_binding and payload["id"]:
                    desired_media_by_variant_id.setdefault(
                        variant_binding.shopify_id, set()
                    ).add(payload["id"])
            if target["kind"] == "template":
                binding.write(
                    {
                        "main_image_shopify_id": payload["id"],
                        "main_image_checksum": target["checksum"],
                    }
                )
            elif target["kind"] == "variant":
                variant_binding = binding.variant_binding_ids.filtered(
                    lambda item, target=target: item.odoo_id == target["record"]
                )[:1]
                variant_binding.write(
                    {
                        "image_shopify_id": payload["id"],
                        "image_checksum": target["checksum"],
                    }
                )
            else:
                target_variant_bindings = binding.variant_binding_ids.filtered(
                    lambda item, target=target: (
                        item.odoo_id.id in target.get("variant_ids", [])
                    )
                )
                image_binding = self.env["shopify.product.image"].search(
                    [
                        ("instance_id", "=", instance.id),
                        ("odoo_id", "=", target["record"].id),
                    ],
                    limit=1,
                )
                image_values = {
                    "shopify_id": payload["id"],
                    "template_binding_id": binding.id,
                    "odoo_id": target["record"].id,
                    "source_url": payload["url"],
                    "image_checksum": target["checksum"],
                    "variant_binding_id": target_variant_bindings[:1].id,
                    "variant_binding_ids": [Command.set(target_variant_bindings.ids)],
                    "state": "synced",
                    "error_message": False,
                    "last_sync_date": fields.Datetime.now(),
                }
                if image_binding:
                    image_binding.write(image_values)
                else:
                    self.env["shopify.product.image"].create(
                        {
                            **image_values,
                            "instance_id": instance.id,
                        }
                    )
        if not instance._is_product_field_owned_by("images", "odoo"):
            return binding, [], []
        media_type_by_id = {item["id"]: item["media_content_type"] for item in media}
        current_media_by_variant_id = {
            variant["id"]: {
                media_id
                for media_id in variant["media_ids"]
                if media_type_by_id.get(media_id) == "IMAGE"
            }
            for variant in normalized["variants"]
        }
        append_media = []
        detach_media = []
        for variant_id, current_ids in current_media_by_variant_id.items():
            desired_ids = desired_media_by_variant_id.get(variant_id, set())
            to_append = desired_ids - current_ids
            to_detach = current_ids - desired_ids
            if to_append:
                append_media.append(
                    {"variantId": variant_id, "mediaIds": list(to_append)}
                )
            if to_detach:
                detach_media.append(
                    {"variantId": variant_id, "mediaIds": list(to_detach)}
                )
        return binding, append_media, detach_media


class ShopifyWebhookProductHandlers(models.Model):
    _inherit = "shopify.webhook.event"

    def _handle_product_upsert(self):
        self.ensure_one()
        product = normalize_product_payload(self.payload)
        self.env["shopify.product.template"].with_delay(
            description=self.env._("Import Shopify product webhook %s", product["id"]),
            identity_key=(
                f"shopify.product.sync.{self.instance_id.id}.{product['id']}"
            ),
        )._job_import_product_from_api(self.instance_id.id, product["id"])

    def _handle_product_delete(self):
        self.ensure_one()
        product = normalize_product_payload(self.payload)
        self.env["shopify.product.template"].with_delay(
            description=self.env._("Archive deleted Shopify product %s", product["id"]),
            identity_key=(
                f"shopify.product.sync.{self.instance_id.id}.{product['id']}"
            ),
        )._job_import_product_from_api(self.instance_id.id, product["id"])


WEBHOOK_HANDLERS.update(
    {
        "products/create": "_handle_product_upsert",
        "products/update": "_handle_product_upsert",
        "products/delete": "_handle_product_delete",
    }
)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shopify_binding_ids = fields.One2many(
        "shopify.product.template",
        "odoo_id",
        string="Shopify Bindings",
    )

    def write(self, values):
        result = super().write(values)
        if self.env.context.get("skip_shopify_export"):
            return result
        field_map = {
            "name": "name",
            "description_sale": "description",
            "list_price": "price",
            "image_1920": "images",
            "active": "status",
        }
        changed = {
            owner_field
            for odoo_field, owner_field in field_map.items()
            if odoo_field in values
        }
        structure_changed = "attribute_line_ids" in values
        for template in self:
            bindings = template.sudo().shopify_binding_ids.filtered(
                lambda item: item.instance_id.company_id in self.env.companies
            )
            for binding in bindings:
                owners = binding.instance_id._product_field_owners()
                if "active" in values and owners["status"] == "odoo":
                    owned_status = binding.odoo_status
                    if not template.active:
                        owned_status = "ARCHIVED"
                    elif owned_status == "ARCHIVED":
                        owned_status = "ACTIVE"
                    binding.with_context(shopify_import=True).odoo_status = owned_status
                if structure_changed or any(
                    owners[field_name] == "odoo" for field_name in changed
                ):
                    self.env["shopify.product.template"].sudo()._enqueue_product_export(
                        binding.instance_id, template
                    )
        return result

    def action_open_shopify_export_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Export to Shopify"),
            "res_model": "shopify.product.export.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_tmpl_ids": self.ids,
            },
        }


class ProductProduct(models.Model):
    _inherit = "product.product"

    shopify_variant_binding_ids = fields.One2many(
        "shopify.product.variant",
        "odoo_id",
        string="Shopify Variant Bindings",
    )

    def action_open_shopify_export_wizard(self):
        return self.product_tmpl_id.action_open_shopify_export_wizard()

    def write(self, values):
        result = super().write(values)
        if self.env.context.get("skip_shopify_export"):
            return result
        for variant in self:
            bindings = variant.sudo().shopify_variant_binding_ids.filtered(
                lambda item: item.instance_id.company_id in self.env.companies
            )
            for binding in bindings:
                owners = binding.instance_id._product_field_owners()
                should_export = bool(
                    {"default_code", "barcode", "active"} & values.keys()
                )
                should_export |= "lst_price" in values and owners["price"] == "odoo"
                should_export |= (
                    "image_variant_1920" in values and owners["images"] == "odoo"
                )
                if should_export:
                    self.env["shopify.product.template"].sudo()._enqueue_product_export(
                        binding.instance_id, variant.product_tmpl_id
                    )
        return result


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    def write(self, values):
        templates = self.mapped("product_tmpl_id")
        result = super().write(values)
        if "price_extra" not in values or self.env.context.get("skip_shopify_export"):
            return result
        templates |= self.mapped("product_tmpl_id")
        for template in templates:
            bindings = template.sudo().shopify_binding_ids.filtered(
                lambda item: (
                    item.instance_id.company_id in self.env.companies
                    and item.instance_id._is_product_field_owned_by("price", "odoo")
                )
            )
            for binding in bindings:
                self.env["shopify.product.template"].sudo()._enqueue_product_export(
                    binding.instance_id, template
                )
        return result


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    @api.model_create_multi
    def create(self, vals_list):
        items = super().create(vals_list)
        items._queue_shopify_price_exports()
        return items

    def write(self, values):
        previous_targets = self._shopify_export_targets()
        result = super().write(values)
        if not self.env.context.get("skip_shopify_export"):
            self._queue_shopify_price_exports(previous_targets)
        return result

    def unlink(self):
        targets = self._shopify_export_targets()
        result = super().unlink()
        if not self.env.context.get("skip_shopify_export"):
            self._queue_shopify_targets(targets)
        return result

    def _shopify_export_targets(self):
        targets = set()
        items = self.sudo().filtered("product_id")
        pricelist_ids = items.mapped("pricelist_id").ids
        instances = (
            self.env["shopify.instance"]
            .sudo()
            .search(
                [
                    ("product_pricelist_id", "in", pricelist_ids),
                    ("company_id", "in", self.env.companies.ids),
                ]
            )
        )
        instances_by_pricelist = {
            instance.product_pricelist_id.id: instance
            for instance in instances
            if instance._is_product_field_owned_by("price", "odoo")
        }
        for item in items:
            instance = instances_by_pricelist.get(item.pricelist_id.id)
            if not instance:
                continue
            template = item.product_id.product_tmpl_id
            binding = (
                self.env["shopify.product.template"]
                .sudo()
                .search(
                    [
                        ("instance_id", "=", instance.id),
                        ("odoo_id", "=", template.id),
                    ],
                    limit=1,
                )
            )
            if binding:
                targets.add((instance.id, template.id))
        return targets

    def _queue_shopify_price_exports(self, previous_targets=None):
        if self.env.context.get("skip_shopify_export"):
            return
        targets = set(previous_targets or ()) | self._shopify_export_targets()
        self._queue_shopify_targets(targets)

    def _queue_shopify_targets(self, targets):
        for instance_id, template_id in targets:
            instance = self.env["shopify.instance"].sudo().browse(instance_id)
            template = self.env["product.template"].browse(template_id)
            self.env["shopify.product.template"].sudo()._enqueue_product_export(
                instance, template
            )


class ProductImage(models.Model):
    _inherit = "product.image"

    shopify_image_binding_ids = fields.One2many(
        "shopify.product.image",
        "odoo_id",
        string="Shopify Image Bindings",
    )

    @api.model_create_multi
    def create(self, vals_list):
        images = super().create(vals_list)
        images._queue_shopify_image_exports()
        return images

    def write(self, values):
        result = super().write(values)
        if {"image_1920", "name", "sequence"} & values.keys():
            self._queue_shopify_image_exports()
        return result

    def unlink(self):
        targets = self.mapped("product_tmpl_id") | self.mapped(
            "product_variant_id.product_tmpl_id"
        )
        instances_by_template = []
        for template in targets:
            bindings = template.sudo().shopify_binding_ids.filtered(
                lambda item: item.instance_id.company_id in self.env.companies
            )
            instances_by_template.append((template, bindings.mapped("instance_id")))
        result = super().unlink()
        if not self.env.context.get("skip_shopify_export"):
            for template, instances in instances_by_template:
                for instance in instances:
                    if instance._is_product_field_owned_by("images", "odoo"):
                        self.env[
                            "shopify.product.template"
                        ].sudo()._enqueue_product_export(instance, template)
        return result

    def _queue_shopify_image_exports(self):
        if self.env.context.get("skip_shopify_export"):
            return
        for image in self:
            template = image.product_tmpl_id or image.product_variant_id.product_tmpl_id
            bindings = template.sudo().shopify_binding_ids.filtered(
                lambda item: item.instance_id.company_id in self.env.companies
            )
            for binding in bindings:
                if binding.instance_id._is_product_field_owned_by("images", "odoo"):
                    self.env["shopify.product.template"].sudo()._enqueue_product_export(
                        binding.instance_id, template
                    )
