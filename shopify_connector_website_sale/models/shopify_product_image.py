from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyProductImage(models.Model):
    _name = "shopify.product.image"
    _description = "Shopify Product Image Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"

    template_binding_id = fields.Many2one(
        "shopify.product.template",
        required=True,
        index=True,
        ondelete="cascade",
    )
    variant_binding_id = fields.Many2one(
        "shopify.product.variant",
        index=True,
        ondelete="set null",
    )
    variant_binding_ids = fields.Many2many(
        "shopify.product.variant",
        "shopify_product_image_variant_rel",
        "image_binding_id",
        "variant_binding_id",
        string="Associated Shopify Variants",
    )
    odoo_id = fields.Many2one(
        "product.image",
        string="Odoo Product Image",
        required=True,
        index=True,
        ondelete="cascade",
    )
    source_url = fields.Char(readonly=True)
    image_checksum = fields.Char(readonly=True, copy=False)

    _instance_odoo_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo image can only be linked once per Shopify instance.",
    )

    @api.constrains(
        "instance_id",
        "template_binding_id",
        "variant_binding_id",
        "variant_binding_ids",
        "odoo_id",
    )
    def _check_image_binding(self):
        for binding in self:
            if binding.instance_id != binding.template_binding_id.instance_id:
                raise ValidationError(
                    self.env._("An image and its product must use the same instance.")
                )
            if (
                binding.variant_binding_id
                and binding.variant_binding_id.template_binding_id
                != binding.template_binding_id
            ) or binding.variant_binding_ids.filtered(
                lambda variant, binding=binding: (
                    variant.template_binding_id != binding.template_binding_id
                )
            ):
                raise ValidationError(
                    self.env._("The image variant must belong to the bound product.")
                )
            image_template = (
                binding.odoo_id.product_tmpl_id
                or binding.odoo_id.product_variant_id.product_tmpl_id
            )
            if image_template != binding.template_binding_id.odoo_id:
                raise ValidationError(
                    self.env._("The Odoo image must belong to the bound product.")
                )
