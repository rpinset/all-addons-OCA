# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from odoo.addons.component.core import AbstractComponent, Component
from odoo.addons.queue_job.exception import FailedJobError, RetryableJobError


class MercadoLibreProductExporter(AbstractComponent):
    _name = "mercadolibre.product.exporter"
    _inherit = "mercadolibre.backend.component"

    def _free_qty(self, binding, mapping):
        product = binding.odoo_id.with_context(warehouse_id=mapping.warehouse_id.id)
        return product.free_qty

    def _guard(self, binding, function):
        try:
            exported = function()
        except RetryableJobError:
            # A retryable response is not a sync. Leave the binding pending
            # so the job can run again without looking successful.
            binding.write({"state": "pending", "error_message": False})
            raise
        except Exception as error:
            binding.mark_error(str(error))
            if isinstance(error, FailedJobError):
                raise
            raise FailedJobError(str(error)) from error
        if exported:
            binding.mark_synced()
        return exported


class MercadoLibrePriceExporter(Component):
    _name = "mercadolibre.product.exporter.price"
    _inherit = "mercadolibre.product.exporter"
    _apply_on = "mercadolibre.product.product"
    _usage = "record.exporter"

    def run(self, binding):
        def export():
            if not binding.backend_id.export_prices or not binding.odoo_id:
                return False
            mapper = self.component(usage="export.mapper")
            payload = mapper.price_payload(binding)
            self.component(usage="backend.adapter").update_prices(
                binding.external_id, payload
            )
            return True

        return self._guard(binding, export)


class MercadoLibreStockExporterLegacy(Component):
    _name = "mercadolibre.product.exporter.stock.legacy"
    _inherit = "mercadolibre.product.exporter"
    _apply_on = "mercadolibre.product.product"
    _usage = "stock.exporter"

    @classmethod
    def _component_match(cls, work, usage=None, model_name=None, **kw):
        return work.collection.versions == "legacy_item"

    def run(self, binding, mapping):
        def export():
            if self._skip(binding, mapping):
                return False
            quantity = self._free_qty(binding, mapping)
            payload = self.component(usage="export.mapper").legacy_stock_payload(
                binding, quantity
            )
            self.component(usage="backend.adapter").update_legacy_stock(
                binding.external_id, payload
            )
            return True

        return self._guard(binding, export)

    def _skip(self, binding, mapping):
        if not binding.backend_id.export_stock or not binding.odoo_id:
            return True
        if binding.fulfillment or mapping.stock_type == "fulfillment":
            return True
        return False


class MercadoLibreStockExporterUserProduct(Component):
    _name = "mercadolibre.product.exporter.stock.user_product"
    _inherit = "mercadolibre.product.exporter.stock.legacy"
    _apply_on = "mercadolibre.product.product"
    _usage = "stock.exporter"

    @classmethod
    def _component_match(cls, work, usage=None, model_name=None, **kw):
        return work.collection.versions == "user_product"

    def run(self, binding, mapping):
        if not binding.user_product_id:
            return super().run(binding, mapping)

        def export():
            if self._skip(binding, mapping):
                return False
            quantity = self._free_qty(binding, mapping)
            payload = self.component(usage="export.mapper").user_product_stock_payload(
                mapping, quantity
            )
            self.component(usage="backend.adapter").update_user_product_stock(
                binding.user_product_id,
                mapping.stock_type,
                payload,
            )
            return True

        return self._guard(binding, export)


class MercadoLibreProductPublisher(Component):
    _name = "mercadolibre.product.publisher"
    _inherit = "mercadolibre.backend.component"
    _apply_on = "mercadolibre.product.product"
    _usage = "product.publisher"

    def run(self, binding):
        raise UserError(self.env._("Listing publication is not installed."))
