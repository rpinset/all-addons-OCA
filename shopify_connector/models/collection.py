from datetime import datetime, timezone

from psycopg2 import IntegrityError

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


def _collection_updated_at(value):
    if not value:
        return False
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


class ShopifyCollection(models.Model):
    _name = "shopify.collection"
    _description = "Shopify Collection"
    _inherit = "shopify.binding.mixin"
    _order = "name"

    name = fields.Char(required=True, index=True)
    handle = fields.Char(index=True)
    collection_type = fields.Selection(
        [("custom", "Custom"), ("smart", "Smart")],
        required=True,
        default="custom",
        index=True,
    )
    product_binding_ids = fields.Many2many(
        "shopify.product.template",
        "shopify_collection_product_rel",
        "collection_id",
        "product_binding_id",
        string="Products",
    )
    active = fields.Boolean(default=True)

    @api.constrains("instance_id", "product_binding_ids")
    def _check_product_instances(self):
        for collection in self:
            if collection.product_binding_ids.filtered(
                lambda binding, collection=collection: (
                    binding.instance_id != collection.instance_id
                )
            ):
                raise ValidationError(
                    self.env._(
                        "Collection products must belong to the same Shopify instance."
                    )
                )

    @api.model
    def _upsert_shopify_collection(self, instance_id, shopify_id, values):
        domain = [
            ("instance_id", "=", instance_id),
            ("shopify_id", "=", shopify_id),
        ]
        collection = self.with_context(active_test=False).search(domain, limit=1)
        if collection:
            collection.with_context(shopify_import=True).write(values)
            return collection
        try:
            with self.env.cr.savepoint():
                return self.with_context(shopify_import=True).create(
                    {
                        **values,
                        "instance_id": instance_id,
                        "shopify_id": shopify_id,
                    }
                )
        except IntegrityError:
            collection = self.with_context(active_test=False).search(domain, limit=1)
            if not collection:
                raise
            collection.with_context(shopify_import=True).write(values)
            return collection

    @api.model
    def _job_import_collection(self, instance_id, payload):
        instance = self.env["shopify.instance"].browse(instance_id).exists()
        if not instance or not instance.active:
            return False
        shopify_id = str(payload.get("id") or "")
        if not shopify_id:
            instance._write_log(
                entity="collection",
                direction="import",
                level="error",
                message=self.env._("Skipped a Shopify collection without an ID."),
            )
            return False
        collection = self.with_context(active_test=False).search(
            [
                ("instance_id", "=", instance_id),
                ("shopify_id", "=", shopify_id),
            ],
            limit=1,
        )
        try:
            with self.env.cr.savepoint():
                values = {
                    "name": payload.get("title") or payload.get("name") or shopify_id,
                    "handle": payload.get("handle") or "",
                    "collection_type": "smart" if payload.get("ruleSet") else "custom",
                    "external_updated_at": _collection_updated_at(
                        payload.get("updatedAt") or payload.get("updated_at")
                    ),
                    "active": True,
                    "state": "synced",
                    "error_message": False,
                    "last_sync_date": fields.Datetime.now(),
                }
                collection = self._upsert_shopify_collection(
                    instance_id, shopify_id, values
                )
        except Exception as exc:
            if collection:
                collection.write({"state": "error", "error_message": str(exc)})
            instance._write_log(
                entity="collection",
                direction="import",
                level="error",
                message=self.env._(
                    "Collection %(gid)s import failed: %(error)s",
                    gid=shopify_id,
                    error=exc,
                ),
                record=collection or None,
            )
            return False
        instance._write_log(
            entity="collection",
            direction="import",
            level="info",
            message=self.env._("Imported Shopify collection %s.", shopify_id),
            record=collection,
        )
        return collection.id

    @api.model
    def _job_archive_collection(self, instance_id, shopify_id):
        collection = self.with_context(active_test=False).search(
            [
                ("instance_id", "=", instance_id),
                ("shopify_id", "=", shopify_id),
            ],
            limit=1,
        )
        if not collection or not collection.instance_id.active:
            return False
        collection.with_context(shopify_import=True).write(
            {
                "active": False,
                "state": "synced",
                "error_message": False,
                "last_sync_date": fields.Datetime.now(),
            }
        )
        collection.instance_id._write_log(
            entity="collection",
            direction="import",
            level="info",
            message=self.env._("Archived missing Shopify collection %s.", shopify_id),
            record=collection,
        )
        return True

    def write(self, values):
        if (
            "product_binding_ids" in values
            and not self.env.context.get("shopify_import")
            and self.filtered(lambda collection: collection.collection_type == "smart")
        ):
            raise UserError(
                self.env._("Smart collection membership is controlled by Shopify.")
            )
        previous_products = (
            self.mapped("product_binding_ids")
            if "product_binding_ids" in values
            else self.env["shopify.product.template"]
        )
        result = super().write(values)
        if "product_binding_ids" in values and not self.env.context.get(
            "shopify_import"
        ):
            affected = previous_products | self.mapped("product_binding_ids")
            for binding in affected:
                self.env["shopify.product.template"]._enqueue_product_export(
                    binding.instance_id, binding.odoo_id
                )
        return result
