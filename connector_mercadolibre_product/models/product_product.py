# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    mercadolibre_bind_ids = fields.One2many(
        comodel_name="mercadolibre.product.product",
        inverse_name="odoo_id",
    )
    mercadolibre_bind_count = fields.Integer(compute="_compute_mercadolibre_bind_count")

    @api.depends("mercadolibre_bind_ids")
    def _compute_mercadolibre_bind_count(self):
        counts = {
            product.id: count
            for product, count in self.env["mercadolibre.product.product"]._read_group(
                domain=[("odoo_id", "in", self.ids)],
                groupby=["odoo_id"],
                aggregates=["__count"],
            )
        }
        for product in self:
            product.mercadolibre_bind_count = counts.get(product.id, 0)

    def action_view_mercadolibre_bindings(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "connector_mercadolibre_product.action_mercadolibre_product"
        )
        action["domain"] = [("odoo_id", "in", self.ids)]
        return action


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mercadolibre_bind_count = fields.Integer(compute="_compute_mercadolibre_bind_count")

    @api.depends("product_variant_ids.mercadolibre_bind_ids")
    def _compute_mercadolibre_bind_count(self):
        variants = self.product_variant_ids
        counts = {
            product.id: count
            for product, count in self.env["mercadolibre.product.product"]._read_group(
                domain=[("odoo_id", "in", variants.ids)],
                groupby=["odoo_id"],
                aggregates=["__count"],
            )
        }
        for template in self:
            template.mercadolibre_bind_count = sum(
                counts.get(variant.id, 0) for variant in template.product_variant_ids
            )

    def action_view_mercadolibre_bindings(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "connector_mercadolibre_product.action_mercadolibre_product"
        )
        action["domain"] = [("odoo_id", "in", self.product_variant_ids.ids)]
        return action
