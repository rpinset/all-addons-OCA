# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.component.core import Component
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError


class MercadoLibreProductImporter(Component):
    _name = "mercadolibre.product.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.product.product"
    _usage = "record.importer"

    def run(self, item_id, item=None):
        if item is None:
            item = self.component(usage="backend.adapter").read_item(item_id)
        variations = item.get("variations") or [None]
        bindings = self.env["mercadolibre.product.product"]
        for variation in variations:
            payload = dict(item)
            if variation:
                payload["_variation"] = variation
            bindings |= self._import_one(payload)
        return bindings

    def _import_one(self, item):
        values = self.component(usage="import.mapper").map_record(item).values()
        binding = self._find_binding(values["external_id"], values["variation_id"])
        product = self._match_or_create(item, values.get("seller_sku"))
        if product:
            values["odoo_id"] = product.id
        category = self._ensure_category(item.get("category_id"))
        if category:
            values["category_id"] = category.id
        try:
            if binding:
                binding.write(values)
            else:
                values["backend_id"] = self.backend_record.id
                binding = self.model.create(values)
            binding.mark_synced()
        except RetryableJobError:
            raise
        except Exception as error:
            if binding:
                binding.mark_error(str(error))
            if isinstance(error, FailedJobError):
                raise
            raise FailedJobError(str(error)) from error
        return binding

    def _find_binding(self, external_id, variation_id):
        return self.component(usage="binder").to_internal(
            external_id, variation_id=variation_id or False
        )

    def _match_or_create(self, item, sku):
        product = self.env["product.product"]
        if sku:
            product = product.search(
                [
                    ("default_code", "=", sku),
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", self.backend_record.company_id.id),
                ],
                limit=1,
            )
        if product or not sku or not self.backend_record.create_missing_products:
            return product
        return (
            self.env["product.product"]
            .with_context(connector_no_export=True)
            .create(
                {
                    "name": item.get("title") or sku,
                    "default_code": sku,
                    "type": "consu",
                    "is_storable": True,
                    "list_price": item.get("price") or 0.0,
                    "company_id": self.backend_record.company_id.id,
                }
            )
        )

    def _ensure_category(self, external_id):
        if not external_id:
            return self.env["mercadolibre.category"]
        category = self.env["mercadolibre.category"].search(
            [
                ("backend_id", "=", self.backend_record.id),
                ("external_id", "=", external_id),
            ],
            limit=1,
        )
        if category:
            return category
        return self.env["mercadolibre.category"].create(
            {
                "backend_id": self.backend_record.id,
                "external_id": external_id,
                "name": external_id,
            }
        )


class MercadoLibreProductBatchImporter(Component):
    _name = "mercadolibre.product.batch.importer"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.product.product"
    _usage = "batch.importer"

    def run(self):
        item_ids = self.component(usage="backend.adapter").search_item_ids()
        backend = self.backend_record
        for item_id in item_ids:
            description = self.env._(
                "Import Mercado Libre item %(item)s",
                item=item_id,
            )
            backend.with_delay(
                identity_key=f"meli:item:{backend.id}:{item_id}:",
                description=description,
            )._job_import_item(item_id)
        backend.last_product_sync_at = fields.Datetime.now()
