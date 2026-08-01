# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import UserError

from ..graphql.inventory import (
    INVENTORY_LEVEL_QUERY,
    INVENTORY_LEVELS_BULK_QUERY,
    INVENTORY_SET_QUANTITIES_MUTATION,
    LOCATIONS_QUERY,
)
from ..lib.bulk import ShopifyBulkRunner
from ..lib.client import ShopifyUserError
from ..lib.inventory import (
    apply_negative_policy,
    available_quantity,
    build_inventory_set_payload,
    diff_inventory_levels,
    is_stale_compare_error,
    normalize_inventory_bulk_levels,
    quantity_for_basis,
    should_ignore_echo,
)
from .webhook_event import WEBHOOK_HANDLERS


def _shopify_gid(value, resource):
    if not value:
        return False
    value = str(value)
    if value.startswith("gid://shopify/"):
        return value
    return f"gid://shopify/{resource}/{value}"


class ShopifyInstanceInventorySync(models.Model):
    _inherit = "shopify.instance"

    def action_import_locations(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        self.with_delay(
            description=self.env._("Import Shopify locations for %s", self.name),
            identity_key=f"shopify.inventory.locations.{self.id}",
        )._job_import_locations()
        return self._inventory_notification(
            self.env._("Location import queued"),
            self.env._("Shopify locations will be refreshed in the background."),
        )

    def _job_import_locations(self):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return 0
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        client = self._shopify_client()
        after = None
        imported_ids = set()
        count = 0
        while True:
            data = client.execute(LOCATIONS_QUERY, {"after": after})
            connection = data.get("locations") or {}
            for payload in connection.get("nodes") or []:
                shopify_id = payload.get("id")
                if not shopify_id:
                    continue
                imported_ids.add(shopify_id)
                values = self._shopify_location_values(payload)
                binding = self.env["shopify.location"].search(
                    [
                        ("instance_id", "=", self.id),
                        ("shopify_id", "=", shopify_id),
                    ],
                    limit=1,
                )
                if binding:
                    binding.write(values)
                else:
                    binding = self.env["shopify.location"].create(
                        {
                            **values,
                            "instance_id": self.id,
                            "shopify_id": shopify_id,
                        }
                    )
                if not binding.odoo_location_id:
                    self._write_log(
                        entity="inventory_location",
                        direction="import",
                        level="warning",
                        message=self.env._(
                            "Shopify location %(name)s is not mapped; "
                            "inventory writes are disabled for it.",
                            name=binding.name,
                        ),
                        record=binding,
                    )
                count += 1
            page_info = connection.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            after = page_info.get("endCursor")
            if not after:
                raise UserError(
                    self.env._("Shopify returned an invalid location page cursor.")
                )
        stale = self.env["shopify.location"].search(
            [
                ("instance_id", "=", self.id),
                ("shopify_id", "not in", list(imported_ids)),
                ("active", "=", True),
            ]
        )
        stale.write({"active": False, "state": "synced"})
        self._write_log(
            entity="inventory_location",
            direction="import",
            level="info",
            message=self.env._("Imported %s Shopify locations.", count),
            record=self,
        )
        return count

    def _shopify_location_values(self, payload):
        self.ensure_one()
        address = payload.get("address") or {}
        address_parts = [
            address.get("address1"),
            address.get("address2"),
            address.get("city"),
            address.get("provinceCode"),
            address.get("zip"),
            address.get("countryCode"),
        ]
        return {
            "name": payload.get("name")
            or self.env._("Shopify Location %s", payload["id"].rsplit("/", 1)[-1]),
            "legacy_resource_id": (
                str(payload["legacyResourceId"])
                if payload.get("legacyResourceId") is not None
                else False
            ),
            "active": bool(payload.get("isActive")),
            "fulfills_online_orders": bool(payload.get("fulfillsOnlineOrders")),
            "address": ", ".join(str(part) for part in address_parts if part),
            "state": "synced",
            "error_message": False,
            "last_sync_date": fields.Datetime.now(),
        }

    def action_push_inventory(self):
        self.ensure_one()
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        self.with_delay(
            description=self.env._("Reconcile Shopify inventory for %s", self.name),
            identity_key=f"shopify.inventory.reconcile.{self.id}",
        )._job_reconcile_inventory()
        return self._inventory_notification(
            self.env._("Inventory reconciliation queued"),
            self.env._(
                "Odoo and Shopify inventory will be compared in the background."
            ),
        )

    @api.model
    def _cron_reconcile_inventory(self):
        instances = self.search([("active", "=", True), ("state", "=", "connected")])
        for instance in instances:
            instance.with_delay(
                description=self.env._(
                    "Daily Shopify inventory reconcile for %s", instance.name
                ),
                identity_key=f"shopify.inventory.reconcile.{instance.id}",
            )._job_reconcile_inventory()
            instance._write_log(
                entity="drift_inventory",
                direction="import",
                level="info",
                message=self.env._("Daily inventory drift reconciliation queued."),
                record=instance,
            )

    def _job_reconcile_inventory(self):
        self = self.sudo()
        self.ensure_one()
        if not self.active:
            return 0
        if self.state != "connected":
            raise UserError(self.env._("Connect the Shopify instance first."))
        remote = normalize_inventory_bulk_levels(
            ShopifyBulkRunner(self._shopify_client()).run(INVENTORY_LEVELS_BULK_QUERY)
        )
        for location in self.location_binding_ids.filtered(
            lambda item: item.active and not item.odoo_location_id
        ):
            self._write_log(
                entity="inventory",
                direction="export",
                level="error",
                message=self.env._(
                    "Inventory reconciliation skipped unmapped Shopify location %s.",
                    location.name,
                ),
                record=location,
            )
        desired = {}
        binding_by_key = {}
        mapped_locations = self.location_binding_ids.filtered(
            lambda location: location.active and location.odoo_location_id
        )
        variants = self.env["shopify.product.variant"].search(
            [
                ("instance_id", "=", self.id),
                ("state", "=", "synced"),
                ("inventory_sync_enabled", "=", True),
                ("template_binding_id.inventory_sync_enabled", "=", True),
                ("inventory_tracked", "=", True),
                ("inventory_item_shopify_id", "!=", False),
            ]
        )
        for variant in variants:
            if not variant._is_storable_inventory_product():
                continue
            for location in mapped_locations:
                key = (
                    variant.inventory_item_shopify_id,
                    location.shopify_id,
                )
                desired[key] = variant._odoo_inventory_quantity(location)
                binding_by_key[key] = (variant, location)
        for key in desired.keys() - remote.keys():
            variant, location = binding_by_key[key]
            self._write_log(
                entity="inventory",
                direction="export",
                level="error",
                message=self.env._(
                    "Cannot reconcile %(variant)s at %(location)s because "
                    "Shopify has no active inventory level.",
                    variant=variant.odoo_id.display_name,
                    location=location.name,
                ),
                record=variant,
            )
        corrections = diff_inventory_levels(desired, remote)
        for correction in corrections:
            variant, location = binding_by_key[correction["key"]]
            variant._push_inventory_level(
                location,
                remote_quantity=correction["remote"],
                reason="reconcile",
            )
        self._write_log(
            entity="inventory",
            direction="export",
            level="info",
            message=self.env._(
                "Inventory reconciliation completed with %s corrections.",
                len(corrections),
            ),
            record=self,
        )
        return len(corrections)

    def _inventory_notification(self, title, message):
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


class ShopifyProductVariantInventorySync(models.Model):
    _inherit = "shopify.product.variant"

    def _inventory_mapping_or_log(self, location_binding, *, direction="export"):
        self.ensure_one()
        instance = self.instance_id
        valid = bool(
            location_binding
            and location_binding.instance_id == instance
            and location_binding.active
            and location_binding.odoo_location_id
        )
        if not valid:
            instance._write_log(
                entity="inventory",
                direction=direction,
                level="error",
                message=self.env._(
                    "Inventory write refused because the Shopify location "
                    "is inactive, unmapped, or belongs to another instance."
                ),
                record=self,
            )
            return False
        return location_binding

    def _inventory_sync_eligible(self):
        self.ensure_one()
        return bool(
            self.state == "synced"
            and self.inventory_sync_enabled
            and self.template_binding_id.inventory_sync_enabled
            and self.inventory_tracked
            and self.inventory_item_shopify_id
            and self._is_storable_inventory_product()
            and not self.template_binding_id.remote_deleted
        )

    def _odoo_inventory_quantity(self, location_binding, *, apply_export_policy=True):
        self.ensure_one()
        product = self.odoo_id.with_company(self.instance_id.company_id).with_context(
            location=location_binding.odoo_location_id.id
        )
        quantity = quantity_for_basis(
            product.free_qty,
            product.qty_available,
            self.instance_id.inventory_quantity_basis,
        )
        if not apply_export_policy:
            return quantity
        quantity, clamped = apply_negative_policy(
            quantity, self.instance_id.inventory_allow_negative
        )
        if clamped:
            self.instance_id._write_log(
                entity="inventory",
                direction="export",
                level="warning",
                message=self.env._(
                    "Negative Odoo stock for %(variant)s at %(location)s was "
                    "clamped to zero.",
                    variant=product.display_name,
                    location=location_binding.name,
                ),
                record=self,
            )
        return quantity

    def _job_push_inventory_level(self, location_binding_id):
        self = self.sudo()
        self.ensure_one()
        if not self.instance_id.active:
            return False
        location = self.env["shopify.location"].browse(location_binding_id).exists()
        try:
            return self._push_inventory_level(location, reason="delta")
        except Exception as exc:
            self.instance_id._write_log(
                entity="inventory",
                direction="export",
                level="error",
                message=self.env._("Inventory delta push failed: %s", exc),
                record=self,
            )
            raise

    def _push_inventory_level(
        self, location_binding, *, remote_quantity=None, reason="delta"
    ):
        self.ensure_one()
        location_binding = self._inventory_mapping_or_log(location_binding)
        if not location_binding or not self._inventory_sync_eligible():
            return False
        desired = self._odoo_inventory_quantity(location_binding)
        client = self.instance_id._shopify_client()
        if remote_quantity is None:
            remote_quantity = self._read_shopify_inventory_quantity(
                client, location_binding
            )
        if remote_quantity is None:
            self.instance_id._write_log(
                entity="inventory",
                direction="export",
                level="error",
                message=self.env._(
                    "Inventory write refused because Shopify has no active "
                    "inventory level for %(variant)s at %(location)s.",
                    variant=self.odoo_id.display_name,
                    location=location_binding.name,
                ),
                record=self,
            )
            return False
        state = self._inventory_state(location_binding)
        if desired == remote_quantity:
            state.write(
                {
                    "last_shopify_quantity": remote_quantity,
                    "last_sync_date": fields.Datetime.now(),
                }
            )
            return False
        try:
            self._execute_inventory_set(
                client, location_binding, desired, remote_quantity
            )
        except ShopifyUserError as exc:
            if not is_stale_compare_error(exc):
                raise
            refreshed = self._read_shopify_inventory_quantity(client, location_binding)
            if refreshed is None:
                raise
            if refreshed == desired:
                state.write(
                    {
                        "last_shopify_quantity": desired,
                        "last_sync_date": fields.Datetime.now(),
                    }
                )
                return False
            self._execute_inventory_set(client, location_binding, desired, refreshed)
        pushed_at = fields.Datetime.now()
        state.write(
            {
                "last_pushed_quantity": desired,
                "last_pushed_at": pushed_at,
                "last_shopify_quantity": desired,
                "last_sync_date": pushed_at,
            }
        )
        self.instance_id._write_log(
            entity="inventory",
            direction="export",
            level="info",
            message=self.env._(
                "%(reason)s inventory correction for %(variant)s at "
                "%(location)s: %(old)s → %(new)s.",
                reason=self.env._("Reconcile")
                if reason == "reconcile"
                else self.env._("Delta"),
                variant=self.odoo_id.display_name,
                location=location_binding.name,
                old=remote_quantity,
                new=desired,
            ),
            record=self,
        )
        return True

    def _read_shopify_inventory_quantity(self, client, location_binding):
        self.ensure_one()
        data = client.execute(
            INVENTORY_LEVEL_QUERY,
            {
                "inventoryItemId": self.inventory_item_shopify_id,
                "locationId": location_binding.shopify_id,
            },
        )
        item = data.get("inventoryItem")
        if not item:
            return None
        if not item.get("tracked"):
            self.inventory_tracked = False
            return None
        level = item.get("inventoryLevel")
        if not level or not level.get("isActive"):
            return None
        return available_quantity(level)

    def _execute_inventory_set(
        self, client, location_binding, desired, compare_quantity
    ):
        self.ensure_one()
        database_uuid = (
            self.env["ir.config_parameter"].sudo().get_param("database.uuid")
            or self.env.cr.dbname
        )
        reference = (
            f"odoo://shopify-inventory/{database_uuid}/"
            f"{self.instance_id.id}/{self.id}/{location_binding.id}"
        )
        return client.execute(
            INVENTORY_SET_QUANTITIES_MUTATION,
            {
                "input": build_inventory_set_payload(
                    self.inventory_item_shopify_id,
                    location_binding.shopify_id,
                    desired,
                    compare_quantity,
                    reference_document_uri=reference,
                )
            },
        )

    def _inventory_state(self, location_binding):
        self.ensure_one()
        state = self.env["shopify.inventory.state"].search(
            [
                ("instance_id", "=", self.instance_id.id),
                ("variant_binding_id", "=", self.id),
                ("location_binding_id", "=", location_binding.id),
            ],
            limit=1,
        )
        if not state:
            state = self.env["shopify.inventory.state"].create(
                {
                    "instance_id": self.instance_id.id,
                    "variant_binding_id": self.id,
                    "location_binding_id": location_binding.id,
                }
            )
        return state


class StockQuantShopifyInventory(models.Model):
    _inherit = "stock.quant"

    @api.model_create_multi
    def create(self, vals_list):
        quants = super().create(vals_list)
        quants._enqueue_shopify_inventory_delta()
        return quants

    def write(self, values):
        watched = {
            "quantity",
            "reserved_quantity",
            "inventory_quantity",
            "location_id",
            "product_id",
        }
        before = [(quant.product_id, quant.location_id) for quant in self]
        result = super().write(values)
        if watched & values.keys():
            self._enqueue_shopify_inventory_pairs(before)
            self._enqueue_shopify_inventory_delta()
        return result

    def unlink(self):
        self._enqueue_shopify_inventory_delta()
        return super().unlink()

    def _enqueue_shopify_inventory_delta(self):
        if self.env.context.get("skip_shopify_inventory_export"):
            return
        self._enqueue_shopify_inventory_pairs(
            [(quant.product_id, quant.location_id) for quant in self]
        )

    def _enqueue_shopify_inventory_pairs(self, pairs):
        if self.env.context.get("skip_shopify_inventory_export"):
            return
        location_model = self.env["shopify.location"].sudo()
        variant_model = self.env["shopify.product.variant"].sudo()
        seen = set()
        for product, quant_location in pairs:
            pair_key = (product.id, quant_location.id)
            if not all(pair_key) or pair_key in seen:
                continue
            seen.add(pair_key)
            locations = location_model.search(
                [
                    ("active", "=", True),
                    ("odoo_location_id", "parent_of", quant_location.id),
                    ("instance_id.company_id", "in", self.env.companies.ids),
                ]
            )
            for location in locations:
                bindings = variant_model.search(
                    [
                        ("instance_id", "=", location.instance_id.id),
                        ("odoo_id", "=", product.id),
                        ("state", "=", "synced"),
                        ("inventory_sync_enabled", "=", True),
                        (
                            "template_binding_id.inventory_sync_enabled",
                            "=",
                            True,
                        ),
                        ("inventory_tracked", "=", True),
                        ("inventory_item_shopify_id", "!=", False),
                    ]
                )
                for binding in bindings.filtered(
                    lambda item: item._is_storable_inventory_product()
                ):
                    binding.with_delay(
                        description=self.env._(
                            "Push Shopify inventory for %(variant)s at %(location)s",
                            variant=product.display_name,
                            location=location.name,
                        ),
                        identity_key=(
                            f"shopify.inventory.delta."
                            f"{binding.instance_id.id}.{binding.id}."
                            f"{location.id}"
                        ),
                    )._job_push_inventory_level(location.id)


class ShopifyWebhookInventoryHandlers(models.Model):
    _inherit = "shopify.webhook.event"

    def _handle_inventory_level_update(self):
        self.ensure_one()
        instance = self.instance_id
        if not instance.inventory_import_enabled:
            return
        inventory_item_id = _shopify_gid(
            self.payload.get("inventory_item_id"), "InventoryItem"
        )
        location_id = _shopify_gid(self.payload.get("location_id"), "Location")
        quantity = self.payload.get("available")
        if not inventory_item_id or not location_id or quantity is None:
            instance._write_log(
                entity="inventory",
                direction="import",
                level="error",
                message=self.env._(
                    "Inventory webhook is missing item, location, or quantity."
                ),
                record=self,
            )
            return
        variant = self.env["shopify.product.variant"].search(
            [
                ("instance_id", "=", instance.id),
                ("inventory_item_shopify_id", "=", inventory_item_id),
            ],
            limit=1,
        )
        location = self.env["shopify.location"].search(
            [
                ("instance_id", "=", instance.id),
                "|",
                ("shopify_id", "=", location_id),
                (
                    "legacy_resource_id",
                    "=",
                    str(self.payload.get("location_id")),
                ),
            ],
            limit=1,
        )
        if not variant or not variant._inventory_sync_eligible():
            instance._write_log(
                entity="inventory",
                direction="import",
                level="warning",
                message=self.env._(
                    "Inventory webhook skipped because the variant is unbound, "
                    "untracked, opted out, or not storable."
                ),
                record=self,
            )
            return
        location = variant._inventory_mapping_or_log(location, direction="import")
        if not location:
            return
        state = variant._inventory_state(location)
        if should_ignore_echo(
            int(quantity),
            state.last_pushed_quantity if state.last_pushed_at else None,
            state.last_pushed_at,
            window_seconds=instance.inventory_echo_window_seconds,
        ):
            state.write(
                {
                    "last_shopify_quantity": int(quantity),
                    "last_sync_date": fields.Datetime.now(),
                }
            )
            instance._write_log(
                entity="inventory",
                direction="import",
                level="info",
                message=self.env._("Ignored matching Shopify inventory webhook echo."),
                record=variant,
            )
            return
        current = variant._odoo_inventory_quantity(location, apply_export_policy=False)
        delta = int(quantity) - current
        if delta:
            self.env["stock.quant"].with_company(instance.company_id).with_context(
                skip_shopify_inventory_export=True,
                inventory_mode=True,
            )._update_available_quantity(
                variant.odoo_id,
                location.odoo_location_id,
                delta,
            )
        state.write(
            {
                "last_shopify_quantity": int(quantity),
                "last_sync_date": fields.Datetime.now(),
            }
        )
        instance._write_log(
            entity="inventory",
            direction="import",
            level="info",
            message=self.env._(
                "Applied Shopify inventory %(quantity)s for %(variant)s at "
                "%(location)s.",
                quantity=int(quantity),
                variant=variant.odoo_id.display_name,
                location=location.name,
            ),
            record=variant,
        )


WEBHOOK_HANDLERS["inventory_levels/update"] = "_handle_inventory_level_update"
