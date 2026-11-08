# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import AccessError


class MercadoLibreProduct(models.Model):
    _name = "mercadolibre.product.product"
    _inherit = "mercadolibre.binding"
    _description = "Mercado Libre Listing"
    _order = "id desc"

    odoo_id = fields.Many2one(
        comodel_name="product.product",
        ondelete="cascade",
        index=True,
    )
    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="restrict",
        index=True,
    )
    external_id = fields.Char(required=True, index=True)
    variation_id = fields.Char(index=True)
    user_product_id = fields.Char(index=True)
    seller_sku = fields.Char(string="Seller SKU", index=True)
    listing_status = fields.Selection(
        selection=[
            ("active", "Active"),
            ("paused", "Paused"),
            ("closed", "Closed"),
            ("under_review", "Under review"),
            ("inactive", "Inactive"),
        ],
    )
    category_id = fields.Many2one(comodel_name="mercadolibre.category")
    permalink = fields.Char()
    picture_urls = fields.Json()
    picture_url_text = fields.Text(compute="_compute_picture_url_text")
    marketplace_qty = fields.Float(string="Marketplace quantity")
    fulfillment = fields.Boolean()
    currency_id = fields.Many2one(comodel_name="res.currency")
    default_code = fields.Char(related="odoo_id.default_code")
    lst_price = fields.Float(related="odoo_id.lst_price")

    def init(self):
        result = super().init()
        self.env.cr.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS "
            "mercadolibre_product_product_listing_uniq "
            "ON mercadolibre_product_product "
            "(backend_id, external_id, COALESCE(variation_id, ''))"
        )
        return result

    @api.depends("picture_urls")
    def _compute_picture_url_text(self):
        for binding in self:
            urls = binding.picture_urls or []
            if isinstance(urls, list):
                binding.picture_url_text = "\n".join(str(url) for url in urls)
            else:
                binding.picture_url_text = ""

    def _check_catalog_manager(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can change the catalog.")
            )

    def _match_product(self, sku=None):
        self.ensure_one()
        sku = sku if sku is not None else self.seller_sku
        if not sku:
            return self.env["product.product"]
        return self.env["product.product"].search(
            [
                ("default_code", "=", sku),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.backend_id.company_id.id),
            ],
            limit=1,
        )

    def button_match(self):
        self._check_catalog_manager()
        for binding in self:
            product = binding._match_product()
            if product:
                binding.odoo_id = product

    def button_export_price(self):
        self._check_catalog_manager()
        for binding in self:
            binding._enqueue_price_export()

    def button_export_stock(self):
        self._check_catalog_manager()
        for binding in self:
            mappings = binding.backend_id.warehouse_mapping_ids.filtered(
                lambda mapping: mapping.stock_type != "fulfillment"
            )
            for mapping in mappings:
                binding._enqueue_stock_export(mapping)

    def _enqueue_price_export(self):
        for binding in self:
            description = binding.env._(
                "Export Mercado Libre price for %(item)s",
                item=binding.external_id,
            )
            binding.with_delay(
                identity_key=f"meli:price:{binding.backend_id.id}:{binding.id}",
                description=description,
            )._job_export_price()

    def _enqueue_stock_export(self, mapping):
        self.ensure_one()
        description = self.env._(
            "Export Mercado Libre stock for %(item)s",
            item=self.external_id,
        )
        self.with_delay(
            identity_key=(f"meli:stock:{self.backend_id.id}:{self.id}:{mapping.id}"),
            description=description,
        )._job_export_stock(mapping.id)

    def _job_import(self):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            work.component(usage="record.importer").run(self.external_id)

    def _job_export_price(self):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            work.component(usage="record.exporter").run(self)

    def _job_export_stock(self, mapping_id):
        self.ensure_one()
        mapping = self.env["mercadolibre.warehouse.mapping"].browse(mapping_id).exists()
        if not mapping:
            return
        with self.backend_id.work_on(self._name) as work:
            work.component(usage="stock.exporter").run(self, mapping)
