# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import AccessError


class MercadoLibreBackend(models.Model):
    _inherit = "mercadolibre.backend"

    import_products = fields.Boolean(default=True)
    export_prices = fields.Boolean(default=True)
    export_stock = fields.Boolean(default=False)
    create_missing_products = fields.Boolean(default=False)
    warehouse_mapping_ids = fields.One2many(
        comodel_name="mercadolibre.warehouse.mapping",
        inverse_name="backend_id",
    )
    product_binding_ids = fields.One2many(
        comodel_name="mercadolibre.product.product",
        inverse_name="backend_id",
    )
    product_binding_count = fields.Integer(compute="_compute_product_binding_count")
    last_product_sync_at = fields.Datetime(readonly=True, copy=False)

    @api.depends("product_binding_ids")
    def _compute_product_binding_count(self):
        counts = {
            backend.id: count
            for backend, count in self.env["mercadolibre.product.product"]._read_group(
                domain=[("backend_id", "in", self.ids)],
                groupby=["backend_id"],
                aggregates=["__count"],
            )
        }
        for backend in self:
            backend.product_binding_count = counts.get(backend.id, 0)

    def _check_catalog_manager(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can change the catalog.")
            )

    def button_import_listings(self):
        self._check_catalog_manager()
        for backend in self:
            description = self.env._(
                "Import Mercado Libre listings for %(name)s",
                name=backend.display_name,
            )
            backend.with_delay(
                identity_key=f"meli:listings:{backend.id}",
                description=description,
            )._job_import_listings()

    def button_refresh_categories(self):
        self._check_catalog_manager()
        for backend in self:
            description = self.env._(
                "Refresh Mercado Libre categories for %(name)s",
                name=backend.display_name,
            )
            backend.with_delay(
                identity_key=f"meli:categories:{backend.id}",
                description=description,
            )._job_refresh_categories()

    def action_view_products(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "connector_mercadolibre_product.action_mercadolibre_product"
        )
        action["domain"] = [("backend_id", "=", self.id)]
        action["context"] = {"default_backend_id": self.id}
        return action

    def _job_import_listings(self):
        """Enqueue one import job per listing and stamp the sync date."""
        self.ensure_one()
        if not self.import_products:
            return
        with self.work_on("mercadolibre.product.product") as work:
            work.component(usage="batch.importer").run()

    def _job_import_item(self, item_id):
        self.ensure_one()
        with self.work_on("mercadolibre.product.product") as work:
            work.component(usage="record.importer").run(item_id)

    def _job_refresh_categories(self):
        self.ensure_one()
        adapter = self._component_usage_backend("backend.adapter")
        roots = adapter.read(f"/sites/{self.site_id}/categories")
        if isinstance(roots, dict):
            roots = roots.get("categories") or roots.get("results") or []
        self.env["mercadolibre.category"]._sync_nodes(self, roots, adapter)

    @api.model
    def cron_import_listings(self):
        backends = self.search([("import_products", "=", True)])
        for backend in backends:
            description = self.env._(
                "Import Mercado Libre listings for %(name)s",
                name=backend.display_name,
            )
            backend.with_delay(
                identity_key=f"meli:listings:{backend.id}",
                description=description,
            )._job_import_listings()
