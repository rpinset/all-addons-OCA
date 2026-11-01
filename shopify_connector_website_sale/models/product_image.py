from odoo import api, fields, models


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
